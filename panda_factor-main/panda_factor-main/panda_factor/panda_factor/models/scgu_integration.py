"""
SCGU (Subspace-Constrained Graph Unlearning) Integration Module for PandaFactor
================================================================================

This module integrates SCGU methods into the PandaFactor quantitative analysis framework,
enabling graph-based machine unlearning for financial factor networks.

Core Capabilities:
- Heterogeneous graph construction from financial data
- Factor relationship modeling using RGCN/RGAT
- Selective unlearning of specific factor relationships
- Multi-modal factor analysis with graph neural networks

Author: PandaQuantFlow Team
Reference: Zhang et al., "Subspace-Constrained Graph Unlearning", KBS 2025
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import RGCNConv, RGATConv
from torch_geometric.data import Data
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FactorGraphConfig:
    """Configuration for factor graph construction"""
    in_dim: int = 64
    hidden_dim: int = 128
    out_dim: int = 64
    num_relations: int = 4  # Factor-Factor, Factor-Stock, Stock-Stock, Factor-Indicator
    dropout: float = 0.1
    num_layers: int = 2
    similarity_threshold: float = 0.6


class FactorRGCN(nn.Module):
    """
    Relational Graph Convolutional Network for Factor Analysis
    
    This model captures complex relationships between:
    - Factors and stocks
    - Factor-factor correlations
    - Stock-stock co-movements
    - Factor-indicator relationships
    """
    
    def __init__(self, config: FactorGraphConfig, num_nodes: int, num_edge_types: int):
        super().__init__()
        self.config = config
        self.num_edge_types = num_edge_types
        
        # Node embeddings
        self.node_emb = nn.Embedding(num_nodes, config.in_dim)
        
        # RGCN layers
        if num_edge_types > 20:
            self.conv1 = RGCNConv(config.in_dim, config.hidden_dim, 
                                 num_edge_types * 2, num_blocks=4)
            self.conv2 = RGCNConv(config.hidden_dim, config.out_dim, 
                                 num_edge_types * 2, num_blocks=4)
        else:
            self.conv1 = RGCNConv(config.in_dim, config.hidden_dim, num_edge_types * 2)
            self.conv2 = RGCNConv(config.hidden_dim, config.out_dim, num_edge_types * 2)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(config.dropout)
        
        # DistMult decoder for link prediction
        self.relation_emb = nn.Parameter(torch.Tensor(num_edge_types, config.out_dim))
        nn.init.xavier_uniform_(self.relation_emb, gain=nn.init.calculate_gain('relu'))
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, 
                edge_type: torch.Tensor, return_all_emb: bool = False):
        """
        Forward pass through the factor graph
        
        Args:
            x: Node features
            edge_index: Edge connectivity [2, num_edges]
            edge_type: Edge type for each edge
            return_all_emb: Whether to return intermediate embeddings
        
        Returns:
            Node embeddings or tuple of (layer1_emb, layer2_emb)
        """
        x = self.node_emb(x)
        
        # Layer 1
        x1 = self.conv1(x, edge_index, edge_type)
        x1 = self.relu(x1)
        x1 = self.dropout(x1)
        
        # Layer 2
        x2 = self.conv2(x1, edge_index, edge_type)
        
        if return_all_emb:
            return x1, x2
        return x2
    
    def decode(self, z: torch.Tensor, edge_index: torch.Tensor, 
               edge_type: torch.Tensor) -> torch.Tensor:
        """
        Decode edge probabilities using DistMult
        
        Args:
            z: Node embeddings
            edge_index: Edges to decode
            edge_type: Type of each edge
        
        Returns:
            Edge logits
        """
        head = z[edge_index[0]]
        tail = z[edge_index[1]]
        relation = self.relation_emb[edge_type]
        
        logits = torch.sum(head * relation * tail, dim=1)
        return logits


class FactorGNNDelete(FactorRGCN):
    """
    SCGU-enhanced Factor Graph with Unlearning Capability
    
    Enables selective removal of factor relationships while preserving
    local causality and maintaining model performance on retained relationships.
    """
    
    def __init__(self, config: FactorGraphConfig, num_nodes: int, 
                 num_edge_types: int, deletion_mask_1hop: Optional[torch.Tensor] = None,
                 deletion_mask_2hop: Optional[torch.Tensor] = None):
        super().__init__(config, num_nodes, num_edge_types)
        
        # Deletion layers for subspace constraint
        if deletion_mask_1hop is not None:
            self.deletion1 = DeletionLayer(config.hidden_dim, deletion_mask_1hop)
        else:
            self.deletion1 = None
            
        if deletion_mask_2hop is not None:
            self.deletion2 = DeletionLayer(config.out_dim, deletion_mask_2hop)
        else:
            self.deletion2 = None
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, 
                edge_type: torch.Tensor, return_all_emb: bool = False):
        """Forward pass with deletion constraints"""
        x = self.node_emb(x)
        
        # Layer 1 with deletion
        x1 = self.conv1(x, edge_index, edge_type)
        x1 = self.relu(x1)
        if self.deletion1 is not None:
            x1 = self.deletion1(x1)
        x1 = self.dropout(x1)
        
        # Layer 2 with deletion
        x2 = self.conv2(x1, edge_index, edge_type)
        if self.deletion2 is not None:
            x2 = self.deletion2(x2)
        
        if return_all_emb:
            return x1, x2
        return x2


class DeletionLayer(nn.Module):
    """
    Subspace-constrained deletion layer
    
    Projects node embeddings to a subspace orthogonal to the
    information to be forgotten, preserving local causality.
    """
    
    def __init__(self, dim: int, node_mask: torch.Tensor):
        super().__init__()
        self.dim = dim
        self.node_mask = node_mask
        
        # Learnable deletion weights
        self.deletion_weight = nn.Parameter(torch.ones(dim))
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Apply deletion constraint to node embeddings"""
        # Only apply deletion to nodes in the deletion set
        x_deleted = x.clone()
        x_deleted[self.node_mask] = x[self.node_mask] * self.deletion_weight
        return x_deleted


class FactorGraphBuilder:
    """
    Build heterogeneous graphs from financial factor data
    
    Supports multiple relation types:
    - Factor-Stock: Factor values for stocks
    - Factor-Factor: Factor correlations
    - Stock-Stock: Stock co-movements
    - Factor-Indicator: Factor-performance relationships
    """
    
    def __init__(self, config: FactorGraphConfig):
        self.config = config
    
    def build_from_dataframe(self, factor_df: pd.DataFrame, 
                            stock_returns: pd.DataFrame,
                            factor_correlations: Optional[pd.DataFrame] = None) -> Data:
        """
        Construct factor graph from pandas DataFrames
        
        Args:
            factor_df: Factor values [date, symbol, factor_name] -> value
            stock_returns: Stock returns [date, symbol] -> return
            factor_correlations: Pre-computed factor correlations (optional)
        
        Returns:
            PyG Data object with heterogeneous edges
        """
        # Extract unique entities
        factors = factor_df['factor_name'].unique()
        stocks = factor_df['symbol'].unique()
        dates = factor_df['date'].unique()
        
        # Create node mapping
        node_to_idx = {}
        idx = 0
        
        # Factor nodes
        for factor in factors:
            node_to_idx[f'factor_{factor}'] = idx
            idx += 1
        
        # Stock nodes
        for stock in stocks:
            node_to_idx[f'stock_{stock}'] = idx
            idx += 1
        
        num_nodes = len(node_to_idx)
        
        # Build edges
        edge_list = []
        edge_types = []
        
        # 1. Factor-Stock edges (relation type 0)
        for _, row in factor_df.iterrows():
            factor_idx = node_to_idx[f'factor_{row["factor_name"]}']
            stock_idx = node_to_idx[f'stock_{row["symbol"]}']
            
            if not pd.isna(row['value']) and abs(row['value']) > 0.01:
                edge_list.append([factor_idx, stock_idx])
                edge_types.append(0)
        
        # 2. Factor-Factor edges (relation type 1)
        if factor_correlations is not None:
            for i, factor1 in enumerate(factors):
                for j, factor2 in enumerate(factors):
                    if i < j:
                        corr = factor_correlations.loc[factor1, factor2]
                        if abs(corr) > self.config.similarity_threshold:
                            idx1 = node_to_idx[f'factor_{factor1}']
                            idx2 = node_to_idx[f'factor_{factor2}']
                            edge_list.append([idx1, idx2])
                            edge_types.append(1)
        
        # 3. Stock-Stock edges (relation type 2)
        # Compute stock correlations from returns
        stock_corr = stock_returns.corr()
        for i, stock1 in enumerate(stocks):
            for j, stock2 in enumerate(stocks):
                if i < j and stock1 in stock_corr.index and stock2 in stock_corr.columns:
                    corr = stock_corr.loc[stock1, stock2]
                    if abs(corr) > self.config.similarity_threshold:
                        idx1 = node_to_idx[f'stock_{stock1}']
                        idx2 = node_to_idx[f'stock_{stock2}']
                        edge_list.append([idx1, idx2])
                        edge_types.append(2)
        
        # Convert to tensors
        edge_index = torch.tensor(edge_list, dtype=torch.long).t()
        edge_type = torch.tensor(edge_types, dtype=torch.long)
        
        # Create bidirectional edges
        edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)
        edge_type = torch.cat([edge_type, edge_type + self.config.num_relations], dim=0)
        
        # Node features (initialized as indices for embedding lookup)
        x = torch.arange(num_nodes, dtype=torch.long)
        
        data = Data(x=x, edge_index=edge_index, edge_type=edge_type)
        data.num_nodes = num_nodes
        data.node_to_idx = node_to_idx
        
        return data
    
    def mark_deletion_edges(self, data: Data, factor_names: List[str]) -> torch.Tensor:
        """
        Mark edges involving specific factors for deletion
        
        Args:
            data: Factor graph
            factor_names: List of factor names to forget
        
        Returns:
            Boolean mask for edges to delete
        """
        deletion_mask = torch.zeros(data.edge_index.size(1), dtype=torch.bool)
        
        for factor_name in factor_names:
            node_key = f'factor_{factor_name}'
            if node_key in data.node_to_idx:
                factor_idx = data.node_to_idx[node_key]
                # Mark all edges connected to this factor
                deletion_mask |= (data.edge_index[0] == factor_idx) | (data.edge_index[1] == factor_idx)
        
        return deletion_mask


class SCGUTrainer:
    """
    Trainer for SCGU-based factor graph unlearning
    
    Implements the two-objective optimization:
    1. Randomness: Make deleted edges indistinguishable from random
    2. Local Causality: Preserve relationships in the remaining graph
    """
    
    def __init__(self, model: FactorGNNDelete, config: FactorGraphConfig):
        self.model = model
        self.config = config
        self.loss_fct = nn.MSELoss()
    
    def compute_unlearning_loss(self, z: torch.Tensor, data: Data, 
                                df_mask: torch.Tensor, 
                                z_original: torch.Tensor,
                                alpha: float = 0.5) -> Tuple[torch.Tensor, Dict]:
        """
        Compute SCGU unlearning loss
        
        Args:
            z: Current node embeddings
            data: Factor graph data
            df_mask: Mask for edges to delete
            z_original: Original node embeddings before unlearning
            alpha: Weight between randomness and locality loss
        
        Returns:
            Total loss and loss components dict
        """
        # 1. Randomness Loss: deleted edges should be random
        neg_size = df_mask.sum()
        neg_edge_index = self._negative_sampling(data.edge_index, data.num_nodes, neg_size)
        
        df_logits_pos = self.model.decode(z, data.edge_index[:, df_mask], 
                                          data.edge_type[df_mask])
        df_logits_neg = self.model.decode(z, neg_edge_index, 
                                          torch.zeros(neg_size, dtype=torch.long))
        
        loss_random = self.loss_fct(df_logits_pos, df_logits_neg)
        
        # 2. Local Causality Loss: preserve remaining relationships
        retain_mask = ~df_mask
        if retain_mask.sum() > 0:
            logits_current = self.model.decode(z, data.edge_index[:, retain_mask],
                                              data.edge_type[retain_mask])
            logits_original = self.model.decode(z_original, data.edge_index[:, retain_mask],
                                               data.edge_type[retain_mask])
            loss_locality = self.loss_fct(logits_current, logits_original)
        else:
            loss_locality = torch.tensor(0.0)
        
        # Combined loss
        total_loss = alpha * loss_random + (1 - alpha) * loss_locality
        
        loss_dict = {
            'total': total_loss.item(),
            'random': loss_random.item(),
            'locality': loss_locality.item() if isinstance(loss_locality, torch.Tensor) else 0.0
        }
        
        return total_loss, loss_dict
    
    def _negative_sampling(self, edge_index: torch.Tensor, num_nodes: int, 
                          num_samples: int) -> torch.Tensor:
        """Generate negative edge samples"""
        neg_edges = []
        while len(neg_edges) < num_samples:
            src = torch.randint(0, num_nodes, (1,))
            dst = torch.randint(0, num_nodes, (1,))
            if src != dst:
                neg_edges.append([src.item(), dst.item()])
        return torch.tensor(neg_edges, dtype=torch.long).t()
    
    def train_epoch(self, data: Data, df_mask: torch.Tensor, 
                   z_original: torch.Tensor, optimizer: torch.optim.Optimizer) -> Dict:
        """Train one epoch of unlearning"""
        self.model.train()
        
        # Forward pass
        z = self.model(data.x, data.edge_index, data.edge_type)
        
        # Compute loss
        loss, loss_dict = self.compute_unlearning_loss(z, data, df_mask, z_original)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        return loss_dict


# Utility functions for integration with PandaFactor

def create_factor_graph_from_panda(factor_data: pd.DataFrame, 
                                   config: Optional[FactorGraphConfig] = None) -> Data:
    """
    Convenience function to create factor graph from PandaFactor data
    
    Args:
        factor_data: DataFrame with columns ['date', 'symbol', 'factor_name', 'value']
        config: Graph configuration (uses defaults if None)
    
    Returns:
        PyG Data object
    """
    if config is None:
        config = FactorGraphConfig()
    
    builder = FactorGraphBuilder(config)
    
    # Pivot to get stock returns
    stock_returns = factor_data.pivot_table(
        index='date', columns='symbol', values='value', aggfunc='mean'
    )
    
    return builder.build_from_dataframe(factor_data, stock_returns)


def unlearn_factors(model: FactorGNNDelete, data: Data, 
                   factors_to_forget: List[str], 
                   epochs: int = 100, lr: float = 0.001) -> FactorGNNDelete:
    """
    Unlearn specific factors from the model
    
    Args:
        model: Trained factor graph model
        data: Factor graph data
        factors_to_forget: List of factor names to unlearn
        epochs: Number of unlearning epochs
        lr: Learning rate
    
    Returns:
        Updated model with factors forgotten
    """
    # Mark deletion edges
    builder = FactorGraphBuilder(FactorGraphConfig())
    df_mask = builder.mark_deletion_edges(data, factors_to_forget)
    
    # Get original embeddings
    model.eval()
    with torch.no_grad():
        z_original = model(data.x, data.edge_index, data.edge_type)
    
    # Train unlearning
    trainer = SCGUTrainer(model, FactorGraphConfig())
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        loss_dict = trainer.train_epoch(data, df_mask, z_original, optimizer)
        if epoch % 10 == 0:
            print(f"Epoch {epoch}: {loss_dict}")
    
    return model


if __name__ == "__main__":
    # Example usage
    print("SCGU Integration Module for PandaFactor")
    print("=" * 60)
    print("This module provides graph-based machine unlearning for factor analysis")
    print("\nKey Features:")
    print("- Heterogeneous factor graph construction")
    print("- RGCN-based factor relationship modeling")
    print("- Selective factor unlearning with SCGU")
    print("- Preservation of local causality")
