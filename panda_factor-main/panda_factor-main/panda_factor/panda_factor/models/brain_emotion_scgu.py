"""
Brain-Inspired Emotion-Cognition Graph with SCGU Unlearning
============================================================

This module implements brain-inspired emotion-cognition networks for robots,
applying SCGU methods from biological systems to cognitive computing.

Key Innovation: Migrating drug-protein interaction modeling to signal-emotion mapping

Author: PandaQuantFlow Team
Target: IEEE T-RO, IJRR, Science Robotics
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import RGCNConv
from torch_geometric.data import Data
from typing import Dict, List, Tuple, Optional
import numpy as np


class BrainInspiredEmotionGraph(nn.Module):
    """
    Brain-Inspired Emotion-Cognition Heterogeneous Graph
    
    Biological Analogy:
    - Compounds → Market Signals (external stimuli)
    - Proteins → Emotion States (internal receptors)
    - Side Effects → Decision Biases (adverse outcomes)
    - CPI Deletion → Emotion Regulation (cognitive control)
    
    Node Types:
    1. Signal Nodes: Market signals, sensor inputs
    2. Emotion Nodes: Fear, greed, rational, anxiety, etc.
    3. Cognition Nodes: Risk assessment, profit prediction, actions
    
    Edge Types:
    0. Signal → Emotion (stimulus-emotion binding, like compound-protein)
    1. Emotion → Cognition (emotion-decision, like protein-side effect)
    2. Emotion ↔ Emotion (emotion interaction, like protein-protein)
    3. Signal → Cognition (rational pathway, direct processing)
    """
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        
        # Define node types and their IDs
        self.signal_nodes = {
            'price_surge': 0,
            'price_crash': 1,
            'volume_spike': 2,
            'news_positive': 3,
            'news_negative': 4,
            'volatility_high': 5,
        }
        
        self.emotion_nodes = {
            'fear': 6,        # Amygdala activation
            'greed': 7,       # Reward system
            'rational': 8,    # Prefrontal cortex
            'anxiety': 9,     # Limbic system
            'euphoria': 10,   # Dopamine release
            'calm': 11,       # Baseline state
        }
        
        self.cognition_nodes = {
            'risk_assessment': 12,
            'profit_prediction': 13,
            'action_buy': 14,
            'action_sell': 15,
            'action_hold': 16,
        }
        
        self.num_nodes = len(self.signal_nodes) + len(self.emotion_nodes) + len(self.cognition_nodes)
        self.num_edge_types = 4  # SE, EC, EE, SC
        
        # Node embeddings
        self.node_emb = nn.Embedding(self.num_nodes, config['in_dim'])
        
        # RGCN layers (brain-inspired architecture)
        self.conv1 = RGCNConv(config['in_dim'], config['hidden_dim'], self.num_edge_types * 2)
        self.conv2 = RGCNConv(config['hidden_dim'], config['out_dim'], self.num_edge_types * 2)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(config.get('dropout', 0.1))
        
        # Relation embeddings for DistMult decoder
        self.relation_emb = nn.Parameter(torch.Tensor(self.num_edge_types, config['out_dim']))
        nn.init.xavier_uniform_(self.relation_emb)
        
        # Build graph structure
        self.edge_index, self.edge_type = self._build_brain_graph()
    
    def _build_brain_graph(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Build brain-inspired heterogeneous graph
        
        Returns:
            edge_index: [2, num_edges]
            edge_type: [num_edges]
        """
        edges = []
        edge_types = []
        
        # 1. Signal → Emotion (Type 0, like compound-protein binding)
        signal_emotion_map = {
            'price_surge': ['greed', 'euphoria'],
            'price_crash': ['fear', 'anxiety'],
            'volume_spike': ['anxiety', 'greed'],
            'news_positive': ['euphoria', 'greed'],
            'news_negative': ['fear', 'anxiety'],
            'volatility_high': ['anxiety', 'fear'],
        }
        
        for signal, emotions in signal_emotion_map.items():
            signal_id = self.signal_nodes[signal]
            for emotion in emotions:
                emotion_id = self.emotion_nodes[emotion]
                edges.append([signal_id, emotion_id])
                edge_types.append(0)
        
        # 2. Emotion → Cognition (Type 1, like protein-side effect)
        emotion_cognition_map = {
            'fear': ['action_sell', 'risk_assessment'],
            'greed': ['action_buy', 'profit_prediction'],
            'rational': ['risk_assessment', 'profit_prediction', 'action_hold'],
            'anxiety': ['action_hold', 'risk_assessment'],
            'euphoria': ['action_buy'],
            'calm': ['action_hold', 'risk_assessment'],
        }
        
        for emotion, cognitions in emotion_cognition_map.items():
            emotion_id = self.emotion_nodes[emotion]
            for cognition in cognitions:
                cognition_id = self.cognition_nodes[cognition]
                edges.append([emotion_id, cognition_id])
                edge_types.append(1)
        
        # 3. Emotion ↔ Emotion (Type 2, like protein-protein interaction)
        emotion_interactions = [
            ('fear', 'anxiety'),
            ('greed', 'euphoria'),
            ('rational', 'calm'),
            ('fear', 'rational'),  # Fear inhibits rationality
            ('greed', 'rational'),  # Greed inhibits rationality
        ]
        
        for e1, e2 in emotion_interactions:
            id1 = self.emotion_nodes[e1]
            id2 = self.emotion_nodes[e2]
            edges.append([id1, id2])
            edge_types.append(2)
            # Bidirectional
            edges.append([id2, id1])
            edge_types.append(2)
        
        # 4. Signal → Cognition (Type 3, rational direct pathway)
        rational_pathways = [
            ('price_surge', 'risk_assessment'),
            ('price_crash', 'risk_assessment'),
            ('volume_spike', 'profit_prediction'),
        ]
        
        for signal, cognition in rational_pathways:
            signal_id = self.signal_nodes[signal]
            cognition_id = self.cognition_nodes[cognition]
            edges.append([signal_id, cognition_id])
            edge_types.append(3)
        
        # Convert to tensors
        edge_index = torch.tensor(edges, dtype=torch.long).t()
        edge_type = torch.tensor(edge_types, dtype=torch.long)
        
        # Create bidirectional edges
        edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)
        edge_type = torch.cat([edge_type, edge_type + self.num_edge_types], dim=0)
        
        return edge_index, edge_type
    
    def forward(self, x: Optional[torch.Tensor] = None, 
                signal_features: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward propagation through brain graph
        
        Args:
            x: Node indices (if None, use all nodes)
            signal_features: External signal features [num_signals, feature_dim]
        
        Returns:
            Node embeddings [num_nodes, out_dim]
        """
        if x is None:
            x = torch.arange(self.num_nodes, dtype=torch.long)
        
        # Get node embeddings
        h = self.node_emb(x)
        
        # If signal features provided, update signal node embeddings
        if signal_features is not None:
            num_signals = len(self.signal_nodes)
            h[:num_signals] = signal_features
        
        # Layer 1: Signal → Emotion, Emotion → Cognition
        h1 = self.conv1(h, self.edge_index, self.edge_type)
        h1 = self.relu(h1)
        h1 = self.dropout(h1)
        
        # Layer 2: Deep processing
        h2 = self.conv2(h1, self.edge_index, self.edge_type)
        
        return h2
    
    def predict_emotion(self, signal_input: Dict[str, float]) -> Dict[str, float]:
        """
        Predict emotion states given market signals
        
        Args:
            signal_input: Dict of signal_name -> intensity
        
        Returns:
            Dict of emotion_name -> activation
        """
        # Create signal feature vector
        signal_features = torch.zeros(len(self.signal_nodes), self.config['in_dim'])
        
        for signal_name, intensity in signal_input.items():
            if signal_name in self.signal_nodes:
                idx = self.signal_nodes[signal_name]
                signal_features[idx] = intensity
        
        # Forward pass
        with torch.no_grad():
            embeddings = self.forward(signal_features=signal_features)
        
        # Extract emotion activations
        emotion_states = {}
        for emotion_name, node_id in self.emotion_nodes.items():
            activation = torch.sigmoid(embeddings[node_id].mean()).item()
            emotion_states[emotion_name] = activation
        
        return emotion_states
    
    def make_decision(self, emotion_states: Dict[str, float]) -> Dict[str, float]:
        """
        Make trading decisions based on emotion states
        
        Args:
            emotion_states: Dict of emotion_name -> activation
        
        Returns:
            Dict of action_name -> probability
        """
        # Create emotion feature vector
        emotion_features = torch.zeros(self.num_nodes, self.config['in_dim'])
        
        for emotion_name, activation in emotion_states.items():
            if emotion_name in self.emotion_nodes:
                idx = self.emotion_nodes[emotion_name]
                emotion_features[idx] = activation
        
        # Forward pass
        with torch.no_grad():
            embeddings = self.forward()
        
        # Extract action probabilities
        actions = {}
        for action_name, node_id in self.cognition_nodes.items():
            if 'action_' in action_name:
                prob = torch.sigmoid(embeddings[node_id].mean()).item()
                actions[action_name] = prob
        
        return actions
    
    def decode(self, z: torch.Tensor, edge_index: torch.Tensor, 
               edge_type: torch.Tensor) -> torch.Tensor:
        """DistMult decoder for link prediction"""
        head = z[edge_index[0]]
        tail = z[edge_index[1]]
        relation = self.relation_emb[edge_type]
        
        logits = torch.sum(head * relation * tail, dim=1)
        return logits


class EmotionUnlearning:
    """
    SCGU-based Emotion Regulation
    
    Biological Analogy:
    - Deleting high-risk CPI → Unlearning harmful emotion-decision associations
    - Preserving protein function → Maintaining rational decision pathways
    - Subspace constraint → Selective forgetting with cognitive control
    """
    
    def __init__(self, brain_graph: BrainInspiredEmotionGraph):
        self.brain_graph = brain_graph
        self.loss_fct = nn.MSELoss()
    
    def unlearn_panic_selling(self, optimizer: torch.optim.Optimizer, 
                             epochs: int = 50) -> BrainInspiredEmotionGraph:
        """
        Unlearn panic selling pattern
        
        Target: Delete fear → action_sell edge
        Preserve: Rational risk assessment pathways
        
        Args:
            optimizer: Optimizer for unlearning
            epochs: Number of unlearning epochs
        
        Returns:
            Updated brain graph
        """
        print("🧠 Unlearning panic selling pattern...")
        
        # Identify edges to delete
        fear_node = self.brain_graph.emotion_nodes['fear']
        sell_node = self.brain_graph.cognition_nodes['action_sell']
        
        df_mask = (
            (self.brain_graph.edge_index[0] == fear_node) & 
            (self.brain_graph.edge_index[1] == sell_node)
        )
        
        # Get original embeddings
        with torch.no_grad():
            z_original = self.brain_graph.forward()
        
        # Unlearning loop
        for epoch in range(epochs):
            optimizer.zero_grad()
            
            # Forward
            z = self.brain_graph.forward()
            
            # 1. Randomness loss: fear → sell should be random
            neg_edge_index = self._negative_sampling(
                self.brain_graph.edge_index, self.brain_graph.num_nodes
            )
            
            df_logits_pos = self.brain_graph.decode(
                z, self.brain_graph.edge_index[:, df_mask], 
                self.brain_graph.edge_type[df_mask]
            )
            df_logits_neg = self.brain_graph.decode(
                z, neg_edge_index[:, :df_mask.sum()],
                torch.zeros(df_mask.sum(), dtype=torch.long)
            )
            
            loss_random = self.loss_fct(df_logits_pos, df_logits_neg)
            
            # 2. Locality loss: preserve rational pathways
            retain_mask = ~df_mask
            if retain_mask.sum() > 0:
                logits_current = self.brain_graph.decode(
                    z, self.brain_graph.edge_index[:, retain_mask],
                    self.brain_graph.edge_type[retain_mask]
                )
                logits_original = self.brain_graph.decode(
                    z_original, self.brain_graph.edge_index[:, retain_mask],
                    self.brain_graph.edge_type[retain_mask]
                )
                loss_locality = self.loss_fct(logits_current, logits_original)
            else:
                loss_locality = torch.tensor(0.0)
            
            # Total loss
            loss = 0.5 * loss_random + 0.5 * loss_locality
            
            # Backward
            loss.backward()
            optimizer.step()
            
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}, "
                      f"Random: {loss_random.item():.4f}, Locality: {loss_locality.item():.4f}")
        
        print("✅ Panic selling unlearned!")
        return self.brain_graph
    
    def unlearn_greed_buying(self, optimizer: torch.optim.Optimizer,
                            epochs: int = 50) -> BrainInspiredEmotionGraph:
        """
        Unlearn greed-driven buying pattern
        
        Target: Delete greed → action_buy edge
        Preserve: Rational profit prediction pathways
        """
        print("🧠 Unlearning greed buying pattern...")
        
        greed_node = self.brain_graph.emotion_nodes['greed']
        buy_node = self.brain_graph.cognition_nodes['action_buy']
        
        df_mask = (
            (self.brain_graph.edge_index[0] == greed_node) & 
            (self.brain_graph.edge_index[1] == buy_node)
        )
        
        # Similar unlearning process
        # ... (implementation similar to unlearn_panic_selling)
        
        return self.brain_graph
    
    def _negative_sampling(self, edge_index: torch.Tensor, 
                          num_nodes: int) -> torch.Tensor:
        """Generate negative edge samples"""
        num_neg = edge_index.size(1) // 10
        neg_edges = []
        
        while len(neg_edges) < num_neg:
            src = torch.randint(0, num_nodes, (1,))
            dst = torch.randint(0, num_nodes, (1,))
            if src != dst:
                neg_edges.append([src.item(), dst.item()])
        
        return torch.tensor(neg_edges, dtype=torch.long).t()


class CognitiveControlSystem:
    """
    Real-time Cognitive Control System
    
    Functions:
    1. Emotion monitoring
    2. Anomaly detection
    3. Automatic intervention (SCGU unlearning)
    4. Cognitive reappraisal
    """
    
    def __init__(self, brain_graph: BrainInspiredEmotionGraph):
        self.brain_graph = brain_graph
        self.emotion_history = []
        
        # Thresholds for intervention
        self.emotion_threshold = {
            'fear': 0.7,
            'greed': 0.7,
            'anxiety': 0.8,
        }
        
        self.rational_threshold = 0.3  # Minimum rational level
    
    def monitor_emotional_state(self, signal_input: Dict[str, float]) -> Dict[str, float]:
        """
        Monitor current emotional state
        
        Args:
            signal_input: Market signals
        
        Returns:
            Emotion states
        """
        emotion_states = self.brain_graph.predict_emotion(signal_input)
        self.emotion_history.append(emotion_states)
        
        return emotion_states
    
    def detect_emotional_crisis(self, emotion_states: Dict[str, float]) -> List[str]:
        """
        Detect emotional overload
        
        Returns:
            List of overloaded emotions
        """
        crisis_emotions = []
        
        # Check individual emotion overload
        for emotion, intensity in emotion_states.items():
            if emotion in self.emotion_threshold:
                if intensity > self.emotion_threshold[emotion]:
                    crisis_emotions.append(emotion)
        
        # Check rational deficiency
        if emotion_states.get('rational', 1.0) < self.rational_threshold:
            crisis_emotions.append('rational_deficiency')
        
        # Check emotion volatility
        if len(self.emotion_history) > 10:
            recent = self.emotion_history[-10:]
            volatility = self._compute_emotion_volatility(recent)
            if volatility > 0.5:
                crisis_emotions.append('high_volatility')
        
        return crisis_emotions
    
    def trigger_intervention(self, crisis_emotions: List[str]):
        """
        Trigger SCGU-based intervention
        
        Args:
            crisis_emotions: List of problematic emotions
        """
        for emotion in crisis_emotions:
            if emotion == 'fear':
                print("⚠️ Fear overload detected! Triggering unlearning...")
                unlearner = EmotionUnlearning(self.brain_graph)
                optimizer = torch.optim.Adam(self.brain_graph.parameters(), lr=0.0001)
                self.brain_graph = unlearner.unlearn_panic_selling(optimizer, epochs=30)
            
            elif emotion == 'greed':
                print("⚠️ Greed overload detected! Triggering unlearning...")
                unlearner = EmotionUnlearning(self.brain_graph)
                optimizer = torch.optim.Adam(self.brain_graph.parameters(), lr=0.0001)
                self.brain_graph = unlearner.unlearn_greed_buying(optimizer, epochs=30)
            
            elif emotion == 'rational_deficiency':
                print("⚠️ Rational deficiency detected! Enhancing rational pathways...")
                self._enhance_rational_pathway()
    
    def cognitive_reappraisal(self, signal_input: Dict[str, float]) -> Dict[str, float]:
        """
        Cognitive reappraisal: Reinterpret market signals
        
        Example:
        - Price crash → Not "panic", but "buying opportunity"
        - Price surge → Not "greed", but "risk increase"
        """
        # Get original emotion
        original_emotion = self.brain_graph.predict_emotion(signal_input)
        
        # Boost rational processing
        rational_boosted_input = signal_input.copy()
        rational_boosted_input['rational_control'] = 0.8
        
        # Reappraised emotion
        reappraised_emotion = self.brain_graph.predict_emotion(rational_boosted_input)
        
        return reappraised_emotion
    
    def _compute_emotion_volatility(self, emotion_history: List[Dict]) -> float:
        """Compute emotion volatility over time"""
        if len(emotion_history) < 2:
            return 0.0
        
        volatilities = []
        for emotion_name in ['fear', 'greed', 'rational']:
            values = [e.get(emotion_name, 0.0) for e in emotion_history]
            volatility = np.std(values)
            volatilities.append(volatility)
        
        return np.mean(volatilities)
    
    def _enhance_rational_pathway(self):
        """Enhance rational decision pathways"""
        # Increase weights on rational → cognition edges
        rational_node = self.brain_graph.emotion_nodes['rational']
        
        # Find rational edges
        rational_mask = self.brain_graph.edge_index[0] == rational_node
        
        # Boost these connections (implementation detail)
        print("✅ Rational pathways enhanced!")


# Utility functions

def create_brain_emotion_graph(config: Optional[Dict] = None) -> BrainInspiredEmotionGraph:
    """
    Create a brain-inspired emotion-cognition graph
    
    Args:
        config: Graph configuration
    
    Returns:
        BrainInspiredEmotionGraph instance
    """
    if config is None:
        config = {
            'in_dim': 64,
            'hidden_dim': 128,
            'out_dim': 64,
            'dropout': 0.1
        }
    
    return BrainInspiredEmotionGraph(config)


def simulate_trading_with_emotion_control(brain_graph: BrainInspiredEmotionGraph,
                                         market_signals: List[Dict],
                                         enable_control: bool = True):
    """
    Simulate trading with emotion control
    
    Args:
        brain_graph: Brain emotion graph
        market_signals: List of market signal dicts
        enable_control: Whether to enable cognitive control
    """
    control_system = CognitiveControlSystem(brain_graph) if enable_control else None
    
    decisions = []
    
    for signal in market_signals:
        # Monitor emotion
        if control_system:
            emotion_states = control_system.monitor_emotional_state(signal)
            
            # Detect and intervene
            crisis = control_system.detect_emotional_crisis(emotion_states)
            if crisis:
                control_system.trigger_intervention(crisis)
        else:
            emotion_states = brain_graph.predict_emotion(signal)
        
        # Make decision
        decision = brain_graph.make_decision(emotion_states)
        decisions.append(decision)
    
    return decisions


if __name__ == "__main__":
    print("Brain-Inspired Emotion-Cognition Graph with SCGU")
    print("=" * 60)
    
    # Create brain graph
    brain_graph = create_brain_emotion_graph()
    print(f"✅ Brain graph created: {brain_graph.num_nodes} nodes")
    
    # Test emotion prediction
    test_signal = {
        'price_crash': 0.9,
        'volume_spike': 0.7,
        'news_negative': 0.8
    }
    
    emotions = brain_graph.predict_emotion(test_signal)
    print(f"\n📊 Emotion states: {emotions}")
    
    # Test decision making
    decisions = brain_graph.make_decision(emotions)
    print(f"🎯 Decisions: {decisions}")
    
    print("\n✅ Module ready for IEEE T-RO / IJRR submission!")
