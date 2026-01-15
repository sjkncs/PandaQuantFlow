"""
SCGU-PandaFactor Integration Example
=====================================

This example demonstrates how to use SCGU methods for factor graph analysis
and selective factor unlearning in the PandaFactor system.

Usage:
    python scgu_factor_example.py --mode train
    python scgu_factor_example.py --mode unlearn --factors "factor1,factor2"
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np
import torch
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'panda_factor-main', 'panda_factor-main'))

# Import PandaFactor modules
try:
    import panda_data
    panda_data.init()
except ImportError:
    print("Warning: panda_data not available, using synthetic data")
    panda_data = None

# Import SCGU integration module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'panda_factor-main', 'panda_factor-main', 'panda_factor', 'panda_factor'))
from models.scgu_integration import (
    FactorGraphConfig, FactorRGCN, FactorGNNDelete,
    FactorGraphBuilder, SCGUTrainer, create_factor_graph_from_panda
)


def generate_synthetic_factor_data(num_stocks=100, num_factors=20, num_days=252):
    """
    Generate synthetic factor data for demonstration
    
    Args:
        num_stocks: Number of stocks
        num_factors: Number of factors
        num_days: Number of trading days
    
    Returns:
        DataFrame with columns ['date', 'symbol', 'factor_name', 'value']
    """
    print(f"Generating synthetic data: {num_stocks} stocks, {num_factors} factors, {num_days} days")
    
    dates = pd.date_range(end=datetime.now(), periods=num_days, freq='D')
    stocks = [f'STOCK_{i:03d}' for i in range(num_stocks)]
    factors = [f'FACTOR_{i:02d}' for i in range(num_factors)]
    
    data = []
    for date in dates:
        for stock in stocks:
            for factor in factors:
                # Generate correlated factor values
                value = np.random.randn() * 0.1 + np.sin(hash(factor) % 100) * 0.05
                data.append({
                    'date': date,
                    'symbol': stock,
                    'factor_name': factor,
                    'value': value
                })
    
    df = pd.DataFrame(data)
    print(f"Generated {len(df)} factor observations")
    return df


def load_factor_data_from_panda(factor_names=None, start_date=None, end_date=None):
    """
    Load factor data from PandaFactor system
    
    Args:
        factor_names: List of factor names to load (None for all)
        start_date: Start date (str or datetime)
        end_date: End date (str or datetime)
    
    Returns:
        DataFrame with factor data
    """
    if panda_data is None:
        print("PandaData not available, using synthetic data")
        return generate_synthetic_factor_data()
    
    print("Loading factor data from PandaFactor...")
    
    # Get available factors
    if factor_names is None:
        # Load a sample of factors
        factor_names = ['VH03cc651']  # Example factor from README
    
    all_data = []
    for factor_name in factor_names:
        try:
            factor_df = panda_data.get_factor_by_name(
                factor_name=factor_name,
                start_date=start_date or '20230101',
                end_date=end_date or '20240101'
            )
            
            if factor_df is not None and not factor_df.empty:
                # Reshape to standard format
                factor_df = factor_df.reset_index()
                if 'value' not in factor_df.columns:
                    factor_df['value'] = factor_df.iloc[:, -1]
                factor_df['factor_name'] = factor_name
                all_data.append(factor_df)
                print(f"Loaded factor {factor_name}: {len(factor_df)} observations")
        except Exception as e:
            print(f"Error loading factor {factor_name}: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"Total loaded: {len(combined_df)} observations")
        return combined_df
    else:
        print("No data loaded, using synthetic data")
        return generate_synthetic_factor_data()


def train_factor_graph_model(data, config=None, epochs=100):
    """
    Train a factor graph model using RGCN
    
    Args:
        data: Factor data DataFrame
        config: FactorGraphConfig (uses defaults if None)
        epochs: Number of training epochs
    
    Returns:
        Trained model and graph data
    """
    print("\n" + "="*60)
    print("Training Factor Graph Model")
    print("="*60)
    
    # Create graph
    if config is None:
        config = FactorGraphConfig(
            in_dim=64,
            hidden_dim=128,
            out_dim=64,
            num_relations=4,
            dropout=0.1
        )
    
    print("\nBuilding factor graph...")
    graph_data = create_factor_graph_from_panda(data, config)
    print(f"Graph created: {graph_data.num_nodes} nodes, {graph_data.edge_index.size(1)} edges")
    
    # Initialize model
    print("\nInitializing RGCN model...")
    model = FactorRGCN(
        config=config,
        num_nodes=graph_data.num_nodes,
        num_edge_types=config.num_relations
    )
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    model = model.to(device)
    graph_data = graph_data.to(device)
    
    # Training setup
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    print(f"\nTraining for {epochs} epochs...")
    model.train()
    
    for epoch in range(epochs):
        optimizer.zero_grad()
        
        # Forward pass
        z = model(graph_data.x, graph_data.edge_index, graph_data.edge_type)
        
        # Link prediction loss
        pos_edge_index = graph_data.edge_index[:, :graph_data.edge_index.size(1)//2]
        pos_edge_type = graph_data.edge_type[:graph_data.edge_type.size(0)//2]
        
        pos_logits = model.decode(z, pos_edge_index, pos_edge_type)
        
        # Negative sampling
        neg_edge_index = torch.randint(0, graph_data.num_nodes, pos_edge_index.size(), device=device)
        neg_logits = model.decode(z, neg_edge_index, pos_edge_type)
        
        # Binary cross entropy loss
        pos_loss = -torch.log(torch.sigmoid(pos_logits) + 1e-15).mean()
        neg_loss = -torch.log(1 - torch.sigmoid(neg_logits) + 1e-15).mean()
        loss = pos_loss + neg_loss
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
    
    print("\nTraining completed!")
    
    # Save model
    checkpoint_path = 'factor_graph_model.pt'
    torch.save({
        'model_state_dict': model.state_dict(),
        'config': config,
        'graph_data': graph_data.to('cpu')
    }, checkpoint_path)
    print(f"Model saved to {checkpoint_path}")
    
    return model, graph_data


def unlearn_factors(model, graph_data, factors_to_forget, config=None, epochs=50):
    """
    Unlearn specific factors using SCGU
    
    Args:
        model: Trained factor graph model
        graph_data: Factor graph data
        factors_to_forget: List of factor names to forget
        config: FactorGraphConfig
        epochs: Number of unlearning epochs
    
    Returns:
        Updated model
    """
    print("\n" + "="*60)
    print("Unlearning Factors using SCGU")
    print("="*60)
    print(f"Factors to forget: {factors_to_forget}")
    
    device = next(model.parameters()).device
    
    # Mark deletion edges
    builder = FactorGraphBuilder(config or FactorGraphConfig())
    df_mask = builder.mark_deletion_edges(graph_data, factors_to_forget)
    print(f"Marked {df_mask.sum().item()} edges for deletion")
    
    # Get original embeddings
    print("\nComputing original embeddings...")
    model.eval()
    with torch.no_grad():
        z_original = model(graph_data.x, graph_data.edge_index, graph_data.edge_type)
    
    # Convert to deletion model
    print("\nConverting to deletion model...")
    deletion_model = FactorGNNDelete(
        config=config or FactorGraphConfig(),
        num_nodes=graph_data.num_nodes,
        num_edge_types=config.num_relations if config else 4
    )
    deletion_model.load_state_dict(model.state_dict(), strict=False)
    deletion_model = deletion_model.to(device)
    
    # Train unlearning
    print(f"\nUnlearning for {epochs} epochs...")
    trainer = SCGUTrainer(deletion_model, config or FactorGraphConfig())
    optimizer = torch.optim.Adam(deletion_model.parameters(), lr=0.0001)
    
    for epoch in range(epochs):
        loss_dict = trainer.train_epoch(graph_data, df_mask, z_original, optimizer)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, "
                  f"Total Loss: {loss_dict['total']:.4f}, "
                  f"Random Loss: {loss_dict['random']:.4f}, "
                  f"Locality Loss: {loss_dict['locality']:.4f}")
    
    print("\nUnlearning completed!")
    
    # Save unlearned model
    checkpoint_path = 'factor_graph_model_unlearned.pt'
    torch.save({
        'model_state_dict': deletion_model.state_dict(),
        'config': config,
        'graph_data': graph_data.to('cpu'),
        'forgotten_factors': factors_to_forget
    }, checkpoint_path)
    print(f"Unlearned model saved to {checkpoint_path}")
    
    return deletion_model


def evaluate_model(model, graph_data, test_edges=None):
    """
    Evaluate model performance on link prediction
    
    Args:
        model: Factor graph model
        graph_data: Factor graph data
        test_edges: Test edge indices (optional)
    
    Returns:
        Evaluation metrics
    """
    print("\n" + "="*60)
    print("Evaluating Model")
    print("="*60)
    
    model.eval()
    device = next(model.parameters()).device
    
    with torch.no_grad():
        z = model(graph_data.x, graph_data.edge_index, graph_data.edge_type)
        
        # Use all edges if test_edges not provided
        if test_edges is None:
            test_edges = graph_data.edge_index[:, :graph_data.edge_index.size(1)//2]
            test_edge_types = graph_data.edge_type[:graph_data.edge_type.size(0)//2]
        else:
            test_edge_types = torch.zeros(test_edges.size(1), dtype=torch.long, device=device)
        
        # Positive edges
        pos_logits = model.decode(z, test_edges, test_edge_types)
        pos_scores = torch.sigmoid(pos_logits)
        
        # Negative edges
        neg_edges = torch.randint(0, graph_data.num_nodes, test_edges.size(), device=device)
        neg_logits = model.decode(z, neg_edges, test_edge_types)
        neg_scores = torch.sigmoid(neg_logits)
        
        # Compute metrics
        pos_mean = pos_scores.mean().item()
        neg_mean = neg_scores.mean().item()
        
        print(f"Positive edge score (mean): {pos_mean:.4f}")
        print(f"Negative edge score (mean): {neg_mean:.4f}")
        print(f"Score difference: {pos_mean - neg_mean:.4f}")
        
        # Simple accuracy
        correct = (pos_scores > 0.5).sum() + (neg_scores < 0.5).sum()
        total = pos_scores.size(0) + neg_scores.size(0)
        accuracy = correct.item() / total
        print(f"Accuracy: {accuracy:.4f}")
    
    return {
        'pos_score': pos_mean,
        'neg_score': neg_mean,
        'accuracy': accuracy
    }


def main():
    parser = argparse.ArgumentParser(description='SCGU-PandaFactor Integration Example')
    parser.add_argument('--mode', type=str, default='train', 
                       choices=['train', 'unlearn', 'evaluate'],
                       help='Operation mode')
    parser.add_argument('--data-source', type=str, default='synthetic',
                       choices=['synthetic', 'panda'],
                       help='Data source')
    parser.add_argument('--factors', type=str, default=None,
                       help='Comma-separated list of factors to unlearn')
    parser.add_argument('--model-path', type=str, default='factor_graph_model.pt',
                       help='Path to model checkpoint')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs')
    parser.add_argument('--unlearn-epochs', type=int, default=50,
                       help='Number of unlearning epochs')
    
    args = parser.parse_args()
    
    print("="*60)
    print("SCGU-PandaFactor Integration Example")
    print("="*60)
    print(f"Mode: {args.mode}")
    print(f"Data Source: {args.data_source}")
    
    # Load data
    if args.data_source == 'synthetic':
        data = generate_synthetic_factor_data()
    else:
        data = load_factor_data_from_panda()
    
    if args.mode == 'train':
        # Train new model
        model, graph_data = train_factor_graph_model(data, epochs=args.epochs)
        evaluate_model(model, graph_data)
        
    elif args.mode == 'unlearn':
        # Load existing model and unlearn
        if not os.path.exists(args.model_path):
            print(f"Model not found at {args.model_path}, training new model first...")
            model, graph_data = train_factor_graph_model(data, epochs=args.epochs)
        else:
            print(f"Loading model from {args.model_path}...")
            checkpoint = torch.load(args.model_path)
            config = checkpoint['config']
            graph_data = checkpoint['graph_data']
            
            model = FactorRGCN(
                config=config,
                num_nodes=graph_data.num_nodes,
                num_edge_types=config.num_relations
            )
            model.load_state_dict(checkpoint['model_state_dict'])
            
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model = model.to(device)
            graph_data = graph_data.to(device)
        
        # Evaluate before unlearning
        print("\nBefore Unlearning:")
        evaluate_model(model, graph_data)
        
        # Unlearn factors
        if args.factors is None:
            factors_to_forget = ['FACTOR_00', 'FACTOR_01']  # Default
        else:
            factors_to_forget = args.factors.split(',')
        
        unlearned_model = unlearn_factors(
            model, graph_data, factors_to_forget,
            config=checkpoint.get('config') if os.path.exists(args.model_path) else None,
            epochs=args.unlearn_epochs
        )
        
        # Evaluate after unlearning
        print("\nAfter Unlearning:")
        evaluate_model(unlearned_model, graph_data)
        
    elif args.mode == 'evaluate':
        # Load and evaluate model
        if not os.path.exists(args.model_path):
            print(f"Model not found at {args.model_path}")
            return
        
        print(f"Loading model from {args.model_path}...")
        checkpoint = torch.load(args.model_path)
        config = checkpoint['config']
        graph_data = checkpoint['graph_data']
        
        model = FactorRGCN(
            config=config,
            num_nodes=graph_data.num_nodes,
            num_edge_types=config.num_relations
        )
        model.load_state_dict(checkpoint['model_state_dict'])
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        graph_data = graph_data.to(device)
        
        evaluate_model(model, graph_data)
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60)


if __name__ == '__main__':
    main()
