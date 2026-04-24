"""
Configuration module for ABSA pipeline
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class PipelineConfig:
    """Configuration for ABSA pipeline"""
    
    # Model configurations
    ARABIC_MODEL_NAME: str = "UBC-NLP/MARBERT"
    MULTILINGUAL_MODEL_NAME: str = "xlm-roberta-base"
    
    # Language detection
    LANGUAGE_DETECTION_METHOD: str = "langdetect"  # Options: "langdetect", "textblob"
    ARABIC_LANG_CODES: List[str] = None
    
    # Aspect extraction configuration
    ASPECTS_TO_EXTRACT: List[str] = None
    ASPECT_KEYWORDS: Dict[str, List[str]] = None
    
    # Sentiment labels
    SENTIMENT_LABELS: List[str] = None
    
    # Processing
    BATCH_SIZE: int = 32
    MAX_LENGTH: int = 512
    DEVICE: str = "cpu"  # Options: "cpu", "cuda", "mps"
    
    # Output
    SAVE_RESULTS: bool = True
    OUTPUT_FORMAT: str = "json"  # Options: "json", "csv"
    OUTPUT_DIR: str = "./results"
    
    # Logging
    LOGGING_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/absa_pipeline.log"
    
    def __post_init__(self):
        """Initialize defaults"""
        if self.ARABIC_LANG_CODES is None:
            self.ARABIC_LANG_CODES = ["ar"]
        
        if self.SENTIMENT_LABELS is None:
            self.SENTIMENT_LABELS = ["positive", "neutral", "negative"]
        
        if self.ASPECTS_TO_EXTRACT is None:
            self.ASPECTS_TO_EXTRACT = [
                "service", "price", "quality", "food", "atmosphere",
                "cleanliness", "parking", "delivery", "packaging", "taste"
            ]
        
        if self.ASPECT_KEYWORDS is None:
            self.ASPECT_KEYWORDS = {
                "service": ["service", "staff", "waiter", "waitress", "server", "host"],
                "price": ["price", "cost", "expensive", "cheap", "affordable", "rate"],
                "quality": ["quality", "fresh", "good", "bad", "excellent", "poor"],
                "food": ["food", "dish", "meal", "burger", "pizza", "salad"],
                "atmosphere": ["atmosphere", "ambiance", "environment", "decor", "music"],
                "cleanliness": ["clean", "dirty", "hygiene", "sanitary", "neat"],
                "parking": ["parking", "lot", "space"],
                "delivery": ["delivery", "fast", "slow", "on-time"],
                "packaging": ["packaging", "box", "bag", "wrapped"],
                "taste": ["taste", "flavor", "delicious", "bland", "spicy"]
            }
        
        # Create output directories
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.LOG_FILE) or "./logs", exist_ok=True)


# Default configuration instance
DEFAULT_CONFIG = PipelineConfig()
