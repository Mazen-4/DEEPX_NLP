"""
Aspect-Based Sentiment Analysis (ABSA) Pipeline
Supports Arabic (MARBERT) and Multilingual (XLM-R) models
"""

from .pipeline import ABSAPipeline
from .config import PipelineConfig

__version__ = "1.0.0"
__author__ = "DeepX NLP"

__all__ = ["ABSAPipeline", "PipelineConfig"]
