"""
Sentiment classification module for ABSA pipeline
Classifies sentiment for aspects in text
"""

import logging
import torch
import numpy as np
from typing import Optional, List, Dict, Tuple
from transformers import Pipeline


class SentimentClassifier:
    """Classify sentiment using transformer models"""
    
    def __init__(
        self,
        model_name: str = "xlm-roberta-base",
        device: str = "cpu",
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize sentiment classifier
        
        Args:
            model_name: Hugging Face model name
            device: Device to use (cpu, cuda, mps)
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("SentimentClassifier")
        self.model_name = model_name
        self.device = device
        self.pipeline = None
        self.sentiment_labels = ["negative", "neutral", "positive"]
        self.label_to_sentiment = {
            0: "negative",
            1: "neutral",
            2: "positive"
        }
    
    def initialize_pipeline(self) -> Pipeline:
        """
        Initialize the classification pipeline
        
        Returns:
            Transformers Pipeline
        """
        try:
            from transformers import pipeline
            
            self.logger.info(
                f"Initializing sentiment pipeline with {self.model_name} on {self.device}"
            )
            
            # For ABSA, we typically use zero-shot classification
            # This allows classifying any text without fine-tuning
            pipeline_obj = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=0 if self.device == "cuda" else -1 if self.device == "cpu" else 0
            )
            
            self.pipeline = pipeline_obj
            self.logger.info("Sentiment pipeline initialized successfully")
            return pipeline_obj
            
        except Exception as e:
            self.logger.error(f"Error initializing pipeline: {e}")
            raise
    
    def classify_sentiment(self, text: str, aspect: Optional[str] = None) -> Dict:
        """
        Classify sentiment of text (optionally for specific aspect)
        
        Args:
            text: Input text
            aspect: Specific aspect to focus on (optional)
            
        Returns:
            Dictionary with sentiment and confidence
        """
        if not self.pipeline:
            self.initialize_pipeline()
        
        try:
            # Prepare input text
            if aspect:
                input_text = f"{text} [ASPECT: {aspect}]"
            else:
                input_text = text
            
            # Classify
            result = self.pipeline(
                input_text,
                self.sentiment_labels,
                multi_class=False
            )
            
            # Extract results
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            
            return {
                'text': text,
                'aspect': aspect,
                'sentiment': top_label,
                'confidence': float(top_score),
                'all_scores': {
                    label: float(score)
                    for label, score in zip(result['labels'], result['scores'])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error classifying sentiment: {e}")
            return {
                'text': text,
                'aspect': aspect,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'all_scores': {},
                'error': str(e)
            }
    
    def classify_batch(
        self,
        texts: List[str],
        aspects: Optional[List[str]] = None,
        batch_size: int = 32
    ) -> List[Dict]:
        """
        Classify sentiment for batch of texts
        
        Args:
            texts: List of input texts
            aspects: List of aspects (optional)
            batch_size: Batch size for processing
            
        Returns:
            List of classification results
        """
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_aspects = aspects[i:i + batch_size] if aspects else [None] * len(batch_texts)
            
            for text, aspect in zip(batch_texts, batch_aspects):
                result = self.classify_sentiment(text, aspect)
                results.append(result)
            
            self.logger.debug(f"Processed batch {i//batch_size + 1}")
        
        return results
    
    def classify_aspect_sentiments(
        self,
        text: str,
        aspects: List[str]
    ) -> List[Dict]:
        """
        Classify sentiment for multiple aspects in same text
        
        Args:
            text: Input text
            aspects: List of aspects to classify
            
        Returns:
            List of aspect-sentiment pairs
        """
        results = []
        
        for aspect in aspects:
            result = self.classify_sentiment(text, aspect)
            results.append(result)
        
        return results
    
    def set_labels(self, labels: List[str]):
        """
        Set custom sentiment labels
        
        Args:
            labels: List of sentiment labels
        """
        self.sentiment_labels = labels
        self.label_to_sentiment = {i: label for i, label in enumerate(labels)}
        self.logger.info(f"Set custom sentiment labels: {labels}")
    
    def get_sentiment_intensity(self, confidence: float) -> str:
        """
        Convert confidence to intensity level
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Intensity level
        """
        if confidence >= 0.8:
            return "strong"
        elif confidence >= 0.6:
            return "moderate"
        elif confidence >= 0.4:
            return "weak"
        else:
            return "neutral"
    
    def aggregate_sentiments(self, results: List[Dict]) -> Dict:
        """
        Aggregate sentiment results
        
        Args:
            results: List of classification results
            
        Returns:
            Aggregated statistics
        """
        if not results:
            return {}
        
        sentiments = [r['sentiment'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        sentiment_counts = {}
        for sentiment in sentiments:
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        return {
            'total_samples': len(results),
            'sentiment_distribution': sentiment_counts,
            'average_confidence': float(np.mean(confidences)),
            'max_confidence': float(np.max(confidences)),
            'min_confidence': float(np.min(confidences)),
            'std_confidence': float(np.std(confidences))
        }
    
    def get_model_info(self) -> Dict:
        """
        Get information about the model
        
        Returns:
            Model information
        """
        return {
            'model_name': self.model_name,
            'device': self.device,
            'sentiment_labels': self.sentiment_labels,
            'pipeline_initialized': self.pipeline is not None
        }
