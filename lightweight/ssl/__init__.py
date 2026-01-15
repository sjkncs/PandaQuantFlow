"""
Lightweight Self-Supervised Learning Framework
"""

from .contrastive import SimpleContrastiveLearning
from .masked_ae import SimpleMaskedAutoencoder
from .temporal import SimpleTemporalPrediction

__all__ = [
    'SimpleContrastiveLearning',
    'SimpleMaskedAutoencoder',
    'SimpleTemporalPrediction'
]
