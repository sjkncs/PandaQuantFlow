"""
Brain-Inspired Emotion-Cognition Example for Financial Trading Robots
======================================================================

This example demonstrates how to use brain-inspired emotion-cognition graphs
with SCGU unlearning for robust financial trading.

Usage:
    python brain_emotion_example.py --mode train
    python brain_emotion_example.py --mode test --enable-control
    python brain_emotion_example.py --mode unlearn --target fear
"""

import sys
import os
import argparse
import numpy as np
import torch
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'panda_factor-main', 'panda_factor-main', 'panda_factor', 'panda_factor'))

from models.brain_emotion_scgu import (
    BrainInspiredEmotionGraph,
    EmotionUnlearning,
    CognitiveControlSystem,
    create_brain_emotion_graph,
    simulate_trading_with_emotion_control
)


def generate_market_scenarios():
    """
    Generate various market scenarios for testing
    
    Returns:
        List of market signal dicts
    """
    scenarios = []
    
    # 1. Market crash scenario (high fear)
    scenarios.append({
        'name': 'Market Crash',
        'signals': {
            'price_crash': 0.9,
            'volume_spike': 0.8,
            'news_negative': 0.9,
            'volatility_high': 0.9
        }
    })
    
    # 2. Bull market scenario (high greed)
    scenarios.append({
        'name': 'Bull Market',
        'signals': {
            'price_surge': 0.9,
            'volume_spike': 0.7,
            'news_positive': 0.8,
            'volatility_high': 0.5
        }
    })
    
    # 3. Calm market scenario (rational)
    scenarios.append({
        'name': 'Calm Market',
        'signals': {
            'price_surge': 0.3,
            'price_crash': 0.2,
            'volume_spike': 0.3,
            'news_positive': 0.5,
            'volatility_high': 0.2
        }
    })
    
    # 4. Flash crash scenario (extreme fear)
    scenarios.append({
        'name': 'Flash Crash',
        'signals': {
            'price_crash': 1.0,
            'volume_spike': 1.0,
            'news_negative': 0.7,
            'volatility_high': 1.0
        }
    })
    
    # 5. FOMO scenario (extreme greed)
    scenarios.append({
        'name': 'FOMO Rally',
        'signals': {
            'price_surge': 1.0,
            'volume_spike': 0.9,
            'news_positive': 1.0,
            'volatility_high': 0.8
        }
    })
    
    return scenarios


def train_brain_graph(epochs=100):
    """
    Train brain-inspired emotion-cognition graph
    
    Args:
        epochs: Number of training epochs
    
    Returns:
        Trained brain graph
    """
    print("\n" + "="*60)
    print("Training Brain-Inspired Emotion-Cognition Graph")
    print("="*60)
    
    # Create brain graph
    config = {
        'in_dim': 64,
        'hidden_dim': 128,
        'out_dim': 64,
        'dropout': 0.1
    }
    
    brain_graph = create_brain_emotion_graph(config)
    print(f"✅ Brain graph created: {brain_graph.num_nodes} nodes, "
          f"{brain_graph.edge_index.size(1)} edges")
    
    # Training setup
    optimizer = torch.optim.Adam(brain_graph.parameters(), lr=0.001)
    
    print(f"\n🧠 Training for {epochs} epochs...")
    
    for epoch in range(epochs):
        brain_graph.train()
        optimizer.zero_grad()
        
        # Forward pass
        z = brain_graph.forward()
        
        # Link prediction loss
        pos_logits = brain_graph.decode(
            z, 
            brain_graph.edge_index[:, :brain_graph.edge_index.size(1)//2],
            brain_graph.edge_type[:brain_graph.edge_type.size(0)//2]
        )
        
        # Negative sampling
        neg_edge_index = torch.randint(
            0, brain_graph.num_nodes, 
            (2, pos_logits.size(0))
        )
        neg_logits = brain_graph.decode(
            z, neg_edge_index,
            torch.zeros(pos_logits.size(0), dtype=torch.long)
        )
        
        # Binary cross entropy
        pos_loss = -torch.log(torch.sigmoid(pos_logits) + 1e-15).mean()
        neg_loss = -torch.log(1 - torch.sigmoid(neg_logits) + 1e-15).mean()
        loss = pos_loss + neg_loss
        
        # Backward
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
    
    print("\n✅ Training completed!")
    
    # Save model
    torch.save({
        'model_state_dict': brain_graph.state_dict(),
        'config': config
    }, 'brain_emotion_graph.pt')
    print("💾 Model saved to brain_emotion_graph.pt")
    
    return brain_graph


def test_emotion_prediction(brain_graph):
    """
    Test emotion prediction on various market scenarios
    
    Args:
        brain_graph: Trained brain graph
    """
    print("\n" + "="*60)
    print("Testing Emotion Prediction")
    print("="*60)
    
    scenarios = generate_market_scenarios()
    
    for scenario in scenarios:
        print(f"\n📊 Scenario: {scenario['name']}")
        print(f"   Signals: {scenario['signals']}")
        
        # Predict emotions
        emotions = brain_graph.predict_emotion(scenario['signals'])
        
        print(f"   Emotions:")
        for emotion, intensity in sorted(emotions.items(), key=lambda x: -x[1]):
            bar = '█' * int(intensity * 20)
            print(f"      {emotion:12s}: {bar} {intensity:.3f}")
        
        # Predict decisions
        decisions = brain_graph.make_decision(emotions)
        
        print(f"   Decisions:")
        for action, prob in sorted(decisions.items(), key=lambda x: -x[1]):
            bar = '█' * int(prob * 20)
            print(f"      {action:20s}: {bar} {prob:.3f}")


def test_with_cognitive_control(brain_graph):
    """
    Test trading with cognitive control system
    
    Args:
        brain_graph: Trained brain graph
    """
    print("\n" + "="*60)
    print("Testing with Cognitive Control System")
    print("="*60)
    
    scenarios = generate_market_scenarios()
    
    # Create control system
    control_system = CognitiveControlSystem(brain_graph)
    
    print("\n🧠 Monitoring emotional states...")
    
    for i, scenario in enumerate(scenarios):
        print(f"\n--- Time {i+1}: {scenario['name']} ---")
        
        # Monitor emotion
        emotions = control_system.monitor_emotional_state(scenario['signals'])
        
        print(f"Emotions: fear={emotions['fear']:.3f}, "
              f"greed={emotions['greed']:.3f}, "
              f"rational={emotions['rational']:.3f}")
        
        # Detect crisis
        crisis = control_system.detect_emotional_crisis(emotions)
        
        if crisis:
            print(f"⚠️  Crisis detected: {crisis}")
            print("🧠 Triggering intervention...")
            control_system.trigger_intervention(crisis)
        else:
            print("✅ Emotional state normal")
        
        # Make decision
        decisions = brain_graph.make_decision(emotions)
        action = max(decisions, key=decisions.get)
        print(f"🎯 Decision: {action} (prob={decisions[action]:.3f})")


def unlearn_emotion_pattern(brain_graph, target_emotion='fear'):
    """
    Unlearn specific emotion-decision pattern
    
    Args:
        brain_graph: Trained brain graph
        target_emotion: Emotion to unlearn ('fear' or 'greed')
    """
    print("\n" + "="*60)
    print(f"Unlearning {target_emotion.upper()} Pattern")
    print("="*60)
    
    # Test before unlearning
    print("\n📊 Before Unlearning:")
    
    if target_emotion == 'fear':
        test_signal = {
            'price_crash': 0.9,
            'news_negative': 0.8,
            'volatility_high': 0.9
        }
    else:  # greed
        test_signal = {
            'price_surge': 0.9,
            'news_positive': 0.8,
            'volume_spike': 0.8
        }
    
    emotions_before = brain_graph.predict_emotion(test_signal)
    decisions_before = brain_graph.make_decision(emotions_before)
    
    print(f"   {target_emotion}: {emotions_before[target_emotion]:.3f}")
    if target_emotion == 'fear':
        print(f"   action_sell: {decisions_before['action_sell']:.3f}")
    else:
        print(f"   action_buy: {decisions_before['action_buy']:.3f}")
    
    # Unlearn
    print(f"\n🧠 Starting SCGU unlearning...")
    unlearner = EmotionUnlearning(brain_graph)
    optimizer = torch.optim.Adam(brain_graph.parameters(), lr=0.0001)
    
    if target_emotion == 'fear':
        brain_graph = unlearner.unlearn_panic_selling(optimizer, epochs=50)
    else:
        brain_graph = unlearner.unlearn_greed_buying(optimizer, epochs=50)
    
    # Test after unlearning
    print("\n📊 After Unlearning:")
    
    emotions_after = brain_graph.predict_emotion(test_signal)
    decisions_after = brain_graph.make_decision(emotions_after)
    
    print(f"   {target_emotion}: {emotions_after[target_emotion]:.3f}")
    if target_emotion == 'fear':
        print(f"   action_sell: {decisions_after['action_sell']:.3f}")
    else:
        print(f"   action_buy: {decisions_after['action_buy']:.3f}")
    
    # Compare
    print("\n📈 Change:")
    emotion_change = emotions_after[target_emotion] - emotions_before[target_emotion]
    if target_emotion == 'fear':
        decision_change = decisions_after['action_sell'] - decisions_before['action_sell']
        action_name = 'action_sell'
    else:
        decision_change = decisions_after['action_buy'] - decisions_before['action_buy']
        action_name = 'action_buy'
    
    print(f"   {target_emotion}: {emotion_change:+.3f}")
    print(f"   {action_name}: {decision_change:+.3f}")
    
    if abs(decision_change) > 0.1:
        print(f"\n✅ Successfully unlearned {target_emotion}-driven {action_name}!")
    else:
        print(f"\n⚠️  Unlearning effect limited, may need more epochs")
    
    # Save unlearned model
    torch.save({
        'model_state_dict': brain_graph.state_dict(),
        'unlearned_emotion': target_emotion
    }, f'brain_emotion_graph_unlearned_{target_emotion}.pt')
    print(f"💾 Unlearned model saved")


def visualize_brain_graph(brain_graph):
    """
    Visualize brain graph structure and activations
    
    Args:
        brain_graph: Brain graph to visualize
    """
    print("\n" + "="*60)
    print("Visualizing Brain Graph")
    print("="*60)
    
    try:
        import networkx as nx
        
        # Create NetworkX graph
        G = nx.DiGraph()
        
        # Add nodes
        for node_type, nodes in [
            ('signal', brain_graph.signal_nodes),
            ('emotion', brain_graph.emotion_nodes),
            ('cognition', brain_graph.cognition_nodes)
        ]:
            for name, idx in nodes.items():
                G.add_node(idx, label=name, type=node_type)
        
        # Add edges
        edge_index = brain_graph.edge_index.numpy()
        for i in range(edge_index.shape[1]):
            src, dst = edge_index[0, i], edge_index[1, i]
            G.add_edge(src, dst)
        
        # Layout
        pos = {}
        y_offset = 0
        for node_type, nodes in [
            ('signal', brain_graph.signal_nodes),
            ('emotion', brain_graph.emotion_nodes),
            ('cognition', brain_graph.cognition_nodes)
        ]:
            x_spacing = 2.0 / max(len(nodes), 1)
            for i, (name, idx) in enumerate(nodes.items()):
                pos[idx] = (i * x_spacing - 1.0, y_offset)
            y_offset -= 1.0
        
        # Draw
        plt.figure(figsize=(15, 10))
        
        # Node colors
        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node]['type']
            if node_type == 'signal':
                node_colors.append('lightblue')
            elif node_type == 'emotion':
                node_colors.append('lightcoral')
            else:
                node_colors.append('lightgreen')
        
        nx.draw(G, pos, node_color=node_colors, 
                with_labels=True,
                labels={n: G.nodes[n]['label'] for n in G.nodes()},
                node_size=2000, font_size=8, 
                arrows=True, edge_color='gray', alpha=0.6)
        
        plt.title("Brain-Inspired Emotion-Cognition Graph", fontsize=16)
        plt.tight_layout()
        plt.savefig('brain_emotion_graph.png', dpi=300, bbox_inches='tight')
        print("✅ Graph visualization saved to brain_emotion_graph.png")
        
    except ImportError:
        print("⚠️  NetworkX not installed, skipping visualization")


def main():
    parser = argparse.ArgumentParser(
        description='Brain-Inspired Emotion-Cognition Example'
    )
    parser.add_argument('--mode', type=str, default='train',
                       choices=['train', 'test', 'unlearn', 'visualize'],
                       help='Operation mode')
    parser.add_argument('--enable-control', action='store_true',
                       help='Enable cognitive control system')
    parser.add_argument('--target', type=str, default='fear',
                       choices=['fear', 'greed'],
                       help='Target emotion to unlearn')
    parser.add_argument('--model-path', type=str, default='brain_emotion_graph.pt',
                       help='Path to model checkpoint')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Number of training epochs')
    
    args = parser.parse_args()
    
    print("="*60)
    print("Brain-Inspired Emotion-Cognition for Trading Robots")
    print("="*60)
    print(f"Mode: {args.mode}")
    
    if args.mode == 'train':
        # Train new model
        brain_graph = train_brain_graph(epochs=args.epochs)
        
        # Test on scenarios
        test_emotion_prediction(brain_graph)
        
    elif args.mode == 'test':
        # Load existing model
        if not os.path.exists(args.model_path):
            print(f"Model not found at {args.model_path}, training new model...")
            brain_graph = train_brain_graph(epochs=args.epochs)
        else:
            print(f"Loading model from {args.model_path}...")
            checkpoint = torch.load(args.model_path)
            brain_graph = create_brain_emotion_graph(checkpoint['config'])
            brain_graph.load_state_dict(checkpoint['model_state_dict'])
            print("✅ Model loaded")
        
        # Test
        if args.enable_control:
            test_with_cognitive_control(brain_graph)
        else:
            test_emotion_prediction(brain_graph)
    
    elif args.mode == 'unlearn':
        # Load model
        if not os.path.exists(args.model_path):
            print(f"Model not found at {args.model_path}, training new model...")
            brain_graph = train_brain_graph(epochs=args.epochs)
        else:
            print(f"Loading model from {args.model_path}...")
            checkpoint = torch.load(args.model_path)
            brain_graph = create_brain_emotion_graph(checkpoint['config'])
            brain_graph.load_state_dict(checkpoint['model_state_dict'])
            print("✅ Model loaded")
        
        # Unlearn
        unlearn_emotion_pattern(brain_graph, target_emotion=args.target)
    
    elif args.mode == 'visualize':
        # Load model
        if not os.path.exists(args.model_path):
            print(f"Model not found at {args.model_path}, creating new model...")
            brain_graph = create_brain_emotion_graph()
        else:
            print(f"Loading model from {args.model_path}...")
            checkpoint = torch.load(args.model_path)
            brain_graph = create_brain_emotion_graph(checkpoint['config'])
            brain_graph.load_state_dict(checkpoint['model_state_dict'])
            print("✅ Model loaded")
        
        # Visualize
        visualize_brain_graph(brain_graph)
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60)
    print("\n📝 Next steps:")
    print("1. Train: python brain_emotion_example.py --mode train")
    print("2. Test: python brain_emotion_example.py --mode test --enable-control")
    print("3. Unlearn: python brain_emotion_example.py --mode unlearn --target fear")
    print("4. Visualize: python brain_emotion_example.py --mode visualize")


if __name__ == '__main__':
    main()
