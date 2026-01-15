"""
Self-Supervised Learning Enhanced SCGU for Multi-Modal Factor Analysis
=======================================================================

This module integrates self-supervised learning and synesthesia algorithms
to enhance SCGU's performance in multi-modal scenarios.

Key Innovations:
1. Contrastive Learning for cross-modal alignment
2. Synesthesia-inspired cross-modal generation
3. Self-supervised pretraining for better representations
4. Multi-view consistency learning

Author: PandaQuantFlow Team
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import RGCNConv
from typing import Dict, List, Tuple, Optional
import numpy as np


class ContrastiveLoss(nn.Module):
    """
    InfoNCE Loss for contrastive learning
    
    Aligns representations from different modalities by maximizing
    agreement between positive pairs and minimizing for negative pairs.
    """
    
    def __init__(self, temperature: float = 0.07):
        super().__init__()
        self.temperature = temperature
    
    def forward(self, z1: torch.Tensor, z2: torch.Tensor) -> torch.Tensor:
        """
        Compute contrastive loss between two views
        
        Args:
            z1: Embeddings from modality 1 [N, D]
            z2: Embeddings from modality 2 [N, D]
        
        Returns:
            Contrastive loss
        """
        # Normalize embeddings
        z1 = F.normalize(z1, dim=1)
        z2 = F.normalize(z2, dim=1)
        
        # Compute similarity matrix
        logits = torch.matmul(z1, z2.t()) / self.temperature
        
        # Labels: diagonal elements are positive pairs
        labels = torch.arange(z1.size(0), device=z1.device)
        
        # Symmetric loss
        loss_1 = F.cross_entropy(logits, labels)
        loss_2 = F.cross_entropy(logits.t(), labels)
        
        return (loss_1 + loss_2) / 2


class SynesthesiaModule(nn.Module):
    """
    Synesthesia-Inspired Cross-Modal Translation
    
    Inspired by human synesthesia (cross-sensory perception), this module
    learns to translate between different modalities, enabling:
    - Visual → Graph translation (chart patterns to factor relationships)
    - Text → Graph translation (news sentiment to market structure)
    - Graph → Visual translation (factor networks to heatmaps)
    """
    
    def __init__(self, input_dim: int, output_dim: int, hidden_dim: int = 256):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, output_dim)
        )
        
        # Attention mechanism for selective translation
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4, batch_first=True)
    
    def forward(self, x_source: torch.Tensor, 
                x_target: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Translate from source modality to target modality
        
        Args:
            x_source: Source modality features [N, D_in]
            x_target: Target modality features for attention (optional) [N, D_in]
        
        Returns:
            Translated features [N, D_out]
        """
        # Encode source
        h = self.encoder(x_source)
        
        # Apply attention if target is provided
        if x_target is not None:
            h_target = self.encoder(x_target)
            h, _ = self.attention(
                h.unsqueeze(1), 
                h_target.unsqueeze(1), 
                h_target.unsqueeze(1)
            )
            h = h.squeeze(1)
        
        # Decode to target modality
        output = self.decoder(h)
        
        return output


class MultiViewConsistencyLoss(nn.Module):
    """
    Multi-View Consistency Loss
    
    Ensures that different views (modalities) of the same entity
    produce consistent predictions after unlearning.
    """
    
    def __init__(self, consistency_weight: float = 1.0):
        super().__init__()
        self.consistency_weight = consistency_weight
    
    def forward(self, predictions: List[torch.Tensor]) -> torch.Tensor:
        """
        Compute consistency loss across multiple views
        
        Args:
            predictions: List of predictions from different modalities
        
        Returns:
            Consistency loss
        """
        if len(predictions) < 2:
            return torch.tensor(0.0, device=predictions[0].device)
        
        # Compute pairwise consistency
        loss = 0
        count = 0
        
        for i in range(len(predictions)):
            for j in range(i + 1, len(predictions)):
                # MSE between predictions
                loss += F.mse_loss(predictions[i], predictions[j])
                count += 1
        
        return self.consistency_weight * loss / count if count > 0 else torch.tensor(0.0)


class SelfSupervisedRGCN(nn.Module):
    """
    Self-Supervised RGCN with Multi-Modal Support
    
    Combines:
    - Graph structure learning (self-supervised)
    - Contrastive learning across modalities
    - Synesthesia-based cross-modal translation
    """
    
    def __init__(self, config: Dict, num_nodes: int, num_edge_types: int,
                 modality_dims: Optional[Dict[str, int]] = None):
        super().__init__()
        self.config = config
        self.num_edge_types = num_edge_types
        
        # Node embeddings
        self.node_emb = nn.Embedding(num_nodes, config['in_dim'])
        
        # RGCN layers
        self.conv1 = RGCNConv(config['in_dim'], config['hidden_dim'], num_edge_types * 2)
        self.conv2 = RGCNConv(config['hidden_dim'], config['out_dim'], num_edge_types * 2)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(config.get('dropout', 0.1))
        
        # Relation embeddings for DistMult decoder
        self.relation_emb = nn.Parameter(torch.Tensor(num_edge_types, config['out_dim']))
        nn.init.xavier_uniform_(self.relation_emb)
        
        # Multi-modal encoders (if modalities provided)
        self.modality_encoders = nn.ModuleDict()
        if modality_dims:
            for modality, dim in modality_dims.items():
                self.modality_encoders[modality] = nn.Sequential(
                    nn.Linear(dim, config['hidden_dim']),
                    nn.ReLU(),
                    nn.Linear(config['hidden_dim'], config['out_dim'])
                )
        
        # Synesthesia modules for cross-modal translation
        self.synesthesia_modules = nn.ModuleDict()
        if modality_dims:
            for mod1 in modality_dims:
                for mod2 in modality_dims:
                    if mod1 != mod2:
                        key = f"{mod1}_to_{mod2}"
                        self.synesthesia_modules[key] = SynesthesiaModule(
                            config['out_dim'], config['out_dim'], config['hidden_dim']
                        )
        
        # Contrastive learning
        self.contrastive_loss = ContrastiveLoss(temperature=0.07)
        
        # Multi-view consistency
        self.consistency_loss = MultiViewConsistencyLoss(consistency_weight=1.0)
        
        # Projection heads for contrastive learning
        self.projection_head = nn.Sequential(
            nn.Linear(config['out_dim'], config['out_dim']),
            nn.ReLU(),
            nn.Linear(config['out_dim'], config['out_dim'] // 2)
        )
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, 
                edge_type: torch.Tensor, 
                modality_features: Optional[Dict[str, torch.Tensor]] = None,
                return_all: bool = False) -> Dict[str, torch.Tensor]:
        """
        Forward pass with multi-modal support
        
        Args:
            x: Node indices
            edge_index: Edge connectivity
            edge_type: Edge types
            modality_features: Optional dict of modality-specific features
            return_all: Whether to return all intermediate representations
        
        Returns:
            Dict containing embeddings and optional modality-specific outputs
        """
        # Graph-based embeddings
        x_graph = self.node_emb(x)
        h1 = self.conv1(x_graph, edge_index, edge_type)
        h1 = self.relu(h1)
        h1 = self.dropout(h1)
        
        h2 = self.conv2(h1, edge_index, edge_type)
        
        outputs = {
            'graph_emb': h2,
            'graph_emb_l1': h1
        }
        
        # Process modality-specific features
        if modality_features:
            for modality, features in modality_features.items():
                if modality in self.modality_encoders:
                    mod_emb = self.modality_encoders[modality](features)
                    outputs[f'{modality}_emb'] = mod_emb
        
        if return_all:
            return outputs
        else:
            return h2
    
    def compute_self_supervised_loss(self, outputs: Dict[str, torch.Tensor],
                                     edge_index: torch.Tensor,
                                     edge_type: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Compute self-supervised learning losses
        
        Args:
            outputs: Forward pass outputs
            edge_index: Edge connectivity
            edge_type: Edge types
        
        Returns:
            Dict of losses
        """
        losses = {}
        
        # 1. Graph reconstruction loss (self-supervised)
        z = outputs['graph_emb']
        pos_logits = self.decode(z, edge_index, edge_type)
        
        # Negative sampling
        neg_edge_index = self._negative_sampling(edge_index, z.size(0))
        neg_edge_type = torch.zeros(neg_edge_index.size(1), dtype=torch.long, device=z.device)
        neg_logits = self.decode(z, neg_edge_index, neg_edge_type)
        
        pos_loss = -torch.log(torch.sigmoid(pos_logits) + 1e-15).mean()
        neg_loss = -torch.log(1 - torch.sigmoid(neg_logits) + 1e-15).mean()
        losses['reconstruction'] = pos_loss + neg_loss
        
        # 2. Contrastive loss across modalities
        modality_embs = [v for k, v in outputs.items() if k.endswith('_emb') and k != 'graph_emb']
        
        if len(modality_embs) > 0:
            # Project embeddings
            z_proj = self.projection_head(z)
            
            contrastive_losses = []
            for mod_emb in modality_embs:
                mod_proj = self.projection_head(mod_emb)
                contrastive_losses.append(self.contrastive_loss(z_proj, mod_proj))
            
            losses['contrastive'] = torch.stack(contrastive_losses).mean()
        
        # 3. Synesthesia translation loss
        if len(modality_embs) > 1:
            translation_losses = []
            modality_names = [k.replace('_emb', '') for k in outputs.keys() 
                            if k.endswith('_emb') and k != 'graph_emb']
            
            for i, mod1 in enumerate(modality_names):
                for j, mod2 in enumerate(modality_names):
                    if i < j:
                        key = f"{mod1}_to_{mod2}"
                        if key in self.synesthesia_modules:
                            # Translate mod1 to mod2
                            translated = self.synesthesia_modules[key](
                                outputs[f'{mod1}_emb'],
                                outputs[f'{mod2}_emb']
                            )
                            # Compare with actual mod2
                            translation_losses.append(
                                F.mse_loss(translated, outputs[f'{mod2}_emb'])
                            )
            
            if translation_losses:
                losses['synesthesia'] = torch.stack(translation_losses).mean()
        
        # 4. Multi-view consistency
        all_predictions = []
        for emb_key in outputs.keys():
            if emb_key.endswith('_emb'):
                # Make predictions from each modality
                pred = self.decode(outputs[emb_key], edge_index, edge_type)
                all_predictions.append(pred)
        
        if len(all_predictions) > 1:
            losses['consistency'] = self.consistency_loss(all_predictions)
        
        return losses
    
    def decode(self, z: torch.Tensor, edge_index: torch.Tensor, 
               edge_type: torch.Tensor) -> torch.Tensor:
        """DistMult decoder for link prediction"""
        head = z[edge_index[0]]
        tail = z[edge_index[1]]
        relation = self.relation_emb[edge_type]
        
        logits = torch.sum(head * relation * tail, dim=1)
        return logits
    
    def _negative_sampling(self, edge_index: torch.Tensor, 
                          num_nodes: int) -> torch.Tensor:
        """Generate negative edge samples"""
        num_neg = edge_index.size(1)
        neg_edges = []
        
        while len(neg_edges) < num_neg:
            src = torch.randint(0, num_nodes, (1,), device=edge_index.device)
            dst = torch.randint(0, num_nodes, (1,), device=edge_index.device)
            if src != dst:
                neg_edges.append([src.item(), dst.item()])
        
        return torch.tensor(neg_edges, dtype=torch.long, device=edge_index.device).t()


class SelfSupervisedGNNDelete(SelfSupervisedRGCN):
    """
    Self-Supervised GNN with Unlearning Capability
    
    Extends SelfSupervisedRGCN with SCGU unlearning while maintaining
    self-supervised learning benefits.
    """
    
    def __init__(self, config: Dict, num_nodes: int, num_edge_types: int,
                 modality_dims: Optional[Dict[str, int]] = None,
                 deletion_mask_1hop: Optional[torch.Tensor] = None,
                 deletion_mask_2hop: Optional[torch.Tensor] = None):
        super().__init__(config, num_nodes, num_edge_types, modality_dims)
        
        # Deletion layers
        if deletion_mask_1hop is not None:
            self.deletion1 = DeletionLayer(config['hidden_dim'], deletion_mask_1hop)
        else:
            self.deletion1 = None
        
        if deletion_mask_2hop is not None:
            self.deletion2 = DeletionLayer(config['out_dim'], deletion_mask_2hop)
        else:
            self.deletion2 = None
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, 
                edge_type: torch.Tensor,
                modality_features: Optional[Dict[str, torch.Tensor]] = None,
                return_all: bool = False) -> Dict[str, torch.Tensor]:
        """Forward with deletion constraints"""
        # Graph embeddings with deletion
        x_graph = self.node_emb(x)
        h1 = self.conv1(x_graph, edge_index, edge_type)
        h1 = self.relu(h1)
        
        if self.deletion1 is not None:
            h1 = self.deletion1(h1)
        
        h1 = self.dropout(h1)
        
        h2 = self.conv2(h1, edge_index, edge_type)
        
        if self.deletion2 is not None:
            h2 = self.deletion2(h2)
        
        outputs = {
            'graph_emb': h2,
            'graph_emb_l1': h1
        }
        
        # Process modality features
        if modality_features:
            for modality, features in modality_features.items():
                if modality in self.modality_encoders:
                    mod_emb = self.modality_encoders[modality](features)
                    outputs[f'{modality}_emb'] = mod_emb
        
        if return_all:
            return outputs
        else:
            return h2
    
    def compute_unlearning_loss(self, outputs: Dict[str, torch.Tensor],
                               outputs_original: Dict[str, torch.Tensor],
                               edge_index: torch.Tensor,
                               edge_type: torch.Tensor,
                               df_mask: torch.Tensor,
                               alpha: float = 0.5) -> Dict[str, torch.Tensor]:
        """
        Compute unlearning loss with self-supervised regularization
        
        Args:
            outputs: Current model outputs
            outputs_original: Original model outputs (before unlearning)
            edge_index: Edge connectivity
            edge_type: Edge types
            df_mask: Deletion mask
            alpha: Weight between randomness and locality
        
        Returns:
            Dict of losses
        """
        losses = {}
        
        # 1. SCGU randomness loss
        z = outputs['graph_emb']
        neg_size = df_mask.sum()
        neg_edge_index = self._negative_sampling(edge_index, z.size(0))
        
        df_logits_pos = self.decode(z, edge_index[:, df_mask], edge_type[df_mask])
        df_logits_neg = self.decode(z, neg_edge_index[:, :neg_size], 
                                    torch.zeros(neg_size, dtype=torch.long, device=z.device))
        
        losses['random'] = F.mse_loss(df_logits_pos, df_logits_neg)
        
        # 2. SCGU locality loss
        retain_mask = ~df_mask
        if retain_mask.sum() > 0:
            z_orig = outputs_original['graph_emb']
            logits_current = self.decode(z, edge_index[:, retain_mask], edge_type[retain_mask])
            logits_original = self.decode(z_orig, edge_index[:, retain_mask], edge_type[retain_mask])
            losses['locality'] = F.mse_loss(logits_current, logits_original)
        else:
            losses['locality'] = torch.tensor(0.0, device=z.device)
        
        # 3. Self-supervised regularization (prevent catastrophic forgetting)
        ssl_losses = self.compute_self_supervised_loss(outputs, edge_index, edge_type)
        losses.update({f'ssl_{k}': v for k, v in ssl_losses.items()})
        
        # 4. Cross-modal consistency during unlearning
        if len([k for k in outputs.keys() if k.endswith('_emb')]) > 1:
            # Ensure all modalities forget consistently
            modality_embs = [outputs[k] for k in outputs.keys() if k.endswith('_emb')]
            
            forget_consistency = []
            for emb in modality_embs:
                logits = self.decode(emb, edge_index[:, df_mask], edge_type[df_mask])
                forget_consistency.append(logits)
            
            # All modalities should produce similar (random) predictions on deleted edges
            losses['modal_forget_consistency'] = self.consistency_loss(forget_consistency)
        
        # Total loss
        losses['total'] = (
            alpha * losses['random'] + 
            (1 - alpha) * losses['locality'] +
            0.1 * losses.get('ssl_reconstruction', torch.tensor(0.0)) +
            0.1 * losses.get('ssl_contrastive', torch.tensor(0.0)) +
            0.05 * losses.get('modal_forget_consistency', torch.tensor(0.0))
        )
        
        return losses


class DeletionLayer(nn.Module):
    """Subspace-constrained deletion layer"""
    
    def __init__(self, dim: int, node_mask: torch.Tensor):
        super().__init__()
        self.dim = dim
        self.node_mask = node_mask
        self.deletion_weight = nn.Parameter(torch.ones(dim))
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_deleted = x.clone()
        x_deleted[self.node_mask] = x[self.node_mask] * self.deletion_weight
        return x_deleted


# Utility functions

def pretrain_self_supervised(model: SelfSupervisedRGCN,
                            data: Dict,
                            epochs: int = 100,
                            lr: float = 0.001) -> SelfSupervisedRGCN:
    """
    Pretrain model using self-supervised learning
    
    Args:
        model: Self-supervised RGCN model
        data: Graph data with optional modality features
        epochs: Number of pretraining epochs
        lr: Learning rate
    
    Returns:
        Pretrained model
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    print("Self-supervised pretraining...")
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(
            data['x'], 
            data['edge_index'], 
            data['edge_type'],
            modality_features=data.get('modality_features'),
            return_all=True
        )
        
        # Compute losses
        losses = model.compute_self_supervised_loss(
            outputs, 
            data['edge_index'], 
            data['edge_type']
        )
        
        total_loss = sum(losses.values())
        
        # Backward
        total_loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            loss_str = ', '.join([f'{k}: {v.item():.4f}' for k, v in losses.items()])
            print(f"Epoch {epoch+1}/{epochs}, {loss_str}")
    
    print("Pretraining completed!")
    return model


if __name__ == "__main__":
    print("Self-Supervised SCGU Module")
    print("=" * 60)
    print("Features:")
    print("- Contrastive learning for cross-modal alignment")
    print("- Synesthesia-inspired cross-modal translation")
    print("- Multi-view consistency learning")
    print("- Self-supervised pretraining")
    print("- Enhanced unlearning with SSL regularization")
