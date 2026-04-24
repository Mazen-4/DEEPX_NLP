"""
Main ABSA Pipeline orchestrator
Combines all components for end-to-end processing
"""

import logging
from typing import List, Dict, Optional, Union
from pathlib import Path

from .config import PipelineConfig
from .data_loader import DataLoader
from .language_detector import LanguageDetector
from .preprocessor import TextPreprocessor
from .model_router import ModelRouter
from .aspect_extractor import AspectExtractor
from .sentiment_classifier import SentimentClassifier
from .utils import setup_logging, save_json_file, save_csv_file, Timer


class ABSAPipeline:
    """Complete ABSA Pipeline"""
    
    def __init__(self, config: Optional[PipelineConfig] = None):
        """
        Initialize ABSA Pipeline
        
        Args:
            config: Pipeline configuration
        """
        self.config = config or PipelineConfig()
        self.logger = setup_logging(
            self.config.LOG_FILE,
            self.config.LOGGING_LEVEL
        )
        
        # Initialize components
        self.logger.info("Initializing ABSA Pipeline components...")
        self.data_loader = DataLoader(logger=self.logger)
        self.language_detector = LanguageDetector(logger=self.logger)
        self.preprocessor = TextPreprocessor(logger=self.logger)
        self.model_router = ModelRouter(logger=self.logger)
        self.aspect_extractor = AspectExtractor(
            aspect_keywords=self.config.ASPECT_KEYWORDS,
            logger=self.logger
        )
        
        # Sentiment classifier - will be initialized on demand
        self.sentiment_classifier = None
        self.models_loaded = {}
        
        self.logger.info("ABSA Pipeline initialized successfully")
    
    def process_file(self, file_path: str) -> List[Dict]:
        """
        Process entire file
        
        Args:
            file_path: Path to input file (CSV or JSON)
            
        Returns:
            List of processed results
        """
        with Timer(f"Processing file: {file_path}"):
            # Load data
            data = self.data_loader.load_file(file_path)
            self.logger.info(f"Loaded {len(data)} records from file")
            
            # Process records
            results = []
            for i, record in enumerate(data):
                result = self.process_record(record)
                results.append(result)
                
                if (i + 1) % 10 == 0:
                    self.logger.info(f"Processed {i + 1}/{len(data)} records")
            
            return results
    
    def process_record(self, record: Dict) -> Dict:
        """
        Process single record through full pipeline
        
        Args:
            record: Input record with 'text' field
            
        Returns:
            Processed result with aspects and sentiments
        """
        try:
            text = record.get('text', '')
            if not text:
                return {
                    'text': text,
                    'language': 'unknown',
                    'aspects': [],
                    'error': 'Empty text'
                }
            
            # Step 1: Language detection
            lang_code, lang_confidence = self.language_detector.detect_language(text)
            if 'language' in record:
                lang_code = record['language']  # Use provided language if available
            
            self.logger.debug(f"Detected language: {lang_code} (confidence: {lang_confidence:.2f})")
            
            # Step 2: Text preprocessing
            processed_text = self.preprocessor.preprocess(text, lang_code)
            
            # Step 3: Route to model
            route = self.language_detector.route_to_model(lang_code)
            
            # Step 4: Extract aspects
            aspects_list = self.aspect_extractor.extract_aspects(processed_text)
            
            # Step 5: Classify sentiment for each aspect
            aspect_sentiments = []
            if aspects_list:
                aspect_sentiments = self._classify_aspect_sentiments(
                    processed_text,
                    aspects_list,
                    route
                )
            
            # Prepare result
            result = {
                'text': text,
                'processed_text': processed_text,
                'language': lang_code,
                'language_confidence': float(lang_confidence),
                'model_route': route,
                'aspects': aspect_sentiments,
                'aspect_count': len(aspect_sentiments)
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing record: {e}")
            return {
                'text': record.get('text', ''),
                'language': 'unknown',
                'aspects': [],
                'error': str(e)
            }
    
    def process_text(self, text: str, language: Optional[str] = None) -> Dict:
        """
        Process single text
        
        Args:
            text: Input text
            language: Optional language code
            
        Returns:
            Processing result
        """
        record = {'text': text}
        if language:
            record['language'] = language
        
        return self.process_record(record)
    
    def _classify_aspect_sentiments(
        self,
        text: str,
        aspects: List[str],
        route: str
    ) -> List[Dict]:
        """
        Classify sentiment for each aspect
        
        Args:
            text: Input text
            aspects: List of aspects
            route: Model route
            
        Returns:
            List of aspect-sentiment pairs
        """
        results = []
        
        for aspect in aspects:
            # Simple heuristic: check if aspect appears with positive/negative words
            aspect_sentiment = self._get_aspect_sentiment(text, aspect)
            
            results.append({
                'aspect': aspect,
                'sentiment': aspect_sentiment['sentiment'],
                'confidence': aspect_sentiment['confidence']
            })
        
        return results
    
    def _get_aspect_sentiment(self, text: str, aspect: str) -> Dict:
        """
        Get sentiment for aspect using heuristic method
        
        Args:
            text: Input text
            aspect: Aspect name
            
        Returns:
            Sentiment result
        """
        # Sentiment words
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'delicious', 'fresh', 'clean', 'friendly', 'fast', 'affordable',
            'best', 'perfect', 'awesome', 'nice', 'lovely', 'brilliant'
        }
        negative_words = {
            'bad', 'poor', 'terrible', 'horrible', 'awful', 'disgusting',
            'slow', 'expensive', 'dirty', 'rude', 'worst', 'disappointing',
            'awful', 'mediocre', 'unpleasant', 'cold', 'bland'
        }
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Find aspect context
        aspect_keywords = self.config.ASPECT_KEYWORDS.get(aspect, [aspect])
        
        positive_count = 0
        negative_count = 0
        
        for keyword in aspect_keywords:
            if keyword in text_lower:
                # Look at surrounding words
                idx = text_lower.find(keyword)
                context_start = max(0, idx - 50)
                context_end = min(len(text_lower), idx + len(keyword) + 50)
                context = text_lower[context_start:context_end]
                
                # Count sentiment words
                for word in positive_words:
                    if word in context:
                        positive_count += 1
                
                for word in negative_words:
                    if word in context:
                        negative_count += 1
        
        # Determine sentiment
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(positive_count / max(positive_count + negative_count, 1), 1.0)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(negative_count / max(positive_count + negative_count, 1), 1.0)
        else:
            sentiment = 'neutral'
            confidence = 0.5
        
        return {'sentiment': sentiment, 'confidence': float(confidence)}
    
    def process_batch(
        self,
        texts: List[str],
        languages: Optional[List[str]] = None,
        batch_size: int = 32
    ) -> List[Dict]:
        """
        Process batch of texts
        
        Args:
            texts: List of texts
            languages: Optional list of languages
            batch_size: Batch size
            
        Returns:
            List of results
        """
        results = []
        
        for i, text in enumerate(texts):
            record = {'text': text}
            if languages and i < len(languages):
                record['language'] = languages[i]
            
            result = self.process_record(record)
            results.append(result)
        
        return results
    
    def save_results(
        self,
        results: List[Dict],
        output_path: Optional[str] = None,
        format: str = "json"
    ) -> str:
        """
        Save results to file
        
        Args:
            results: Results to save
            output_path: Output file path
            format: Output format (json or csv)
            
        Returns:
            Path to saved file
        """
        if output_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self.config.OUTPUT_DIR}/absa_results_{timestamp}.{format}"
        
        try:
            if format.lower() == "json":
                save_json_file(results, output_path)
            elif format.lower() == "csv":
                # Flatten results for CSV
                flattened = self._flatten_for_csv(results)
                save_csv_file(flattened, output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Saved results to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
            raise
    
    def _flatten_for_csv(self, results: List[Dict]) -> List[Dict]:
        """
        Flatten results for CSV export
        
        Args:
            results: Results to flatten
            
        Returns:
            Flattened results
        """
        flattened = []
        
        for result in results:
            if result['aspects']:
                for aspect in result['aspects']:
                    row = {
                        'text': result['text'],
                        'language': result['language'],
                        'aspect': aspect['aspect'],
                        'sentiment': aspect['sentiment'],
                        'confidence': aspect['confidence']
                    }
                    flattened.append(row)
            else:
                row = {
                    'text': result['text'],
                    'language': result['language'],
                    'aspect': 'N/A',
                    'sentiment': 'N/A',
                    'confidence': 0.0
                }
                flattened.append(row)
        
        return flattened
    
    def get_statistics(self, results: List[Dict]) -> Dict:
        """
        Get statistics about results
        
        Args:
            results: Processing results
            
        Returns:
            Statistics dictionary
        """
        total = len(results)
        languages = {}
        aspects_count = {}
        sentiments = {}
        
        for result in results:
            # Language statistics
            lang = result.get('language', 'unknown')
            languages[lang] = languages.get(lang, 0) + 1
            
            # Aspect statistics
            for aspect in result.get('aspects', []):
                aspect_name = aspect.get('aspect', 'unknown')
                aspects_count[aspect_name] = aspects_count.get(aspect_name, 0) + 1
                
                # Sentiment statistics
                sentiment = aspect.get('sentiment', 'unknown')
                sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
        
        return {
            'total_samples': total,
            'languages': languages,
            'aspects_found': aspects_count,
            'sentiment_distribution': sentiments,
            'average_aspects_per_sample': sum(len(r['aspects']) for r in results) / max(total, 1)
        }
