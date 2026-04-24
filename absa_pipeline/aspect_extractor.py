"""
Aspect extraction module for ABSA pipeline
Extracts aspects (service, price, quality, etc.) from reviews
"""

import re
import logging
from typing import Optional, List, Dict, Set
from collections import defaultdict


class AspectExtractor:
    """Extract aspects from text"""
    
    def __init__(
        self,
        aspect_keywords: Optional[Dict[str, List[str]]] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize aspect extractor
        
        Args:
            aspect_keywords: Dictionary mapping aspects to keywords
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("AspectExtractor")
        
        # Default aspect keywords
        self.aspect_keywords = aspect_keywords or {
            "service": ["service", "staff", "waiter", "waitress", "server", "host", "hospitality"],
            "price": ["price", "cost", "expensive", "cheap", "affordable", "rate", "charge"],
            "quality": ["quality", "fresh", "good", "bad", "excellent", "poor", "standard"],
            "food": ["food", "dish", "meal", "burger", "pizza", "salad", "cuisine"],
            "atmosphere": ["atmosphere", "ambiance", "environment", "decor", "music", "vibe"],
            "cleanliness": ["clean", "dirty", "hygiene", "sanitary", "neat", "tidy"],
            "parking": ["parking", "lot", "space", "valet"],
            "delivery": ["delivery", "fast", "slow", "on-time", "courier"],
            "packaging": ["packaging", "box", "bag", "wrapped", "container"],
            "taste": ["taste", "flavor", "delicious", "bland", "spicy", "savory"]
        }
        
        # Precompile patterns
        self.aspect_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for aspects"""
        patterns = {}
        for aspect, keywords in self.aspect_keywords.items():
            # Create pattern that matches any keyword
            keyword_pattern = '|'.join(re.escape(kw) for kw in keywords)
            patterns[aspect] = re.compile(keyword_pattern, re.IGNORECASE)
        return patterns
    
    def extract_aspects(self, text: str) -> List[str]:
        """
        Extract aspects from text
        
        Args:
            text: Input text
            
        Returns:
            List of unique aspects found
        """
        if not text:
            return []
        
        found_aspects = set()
        
        for aspect, pattern in self.aspect_patterns.items():
            if pattern.search(text):
                found_aspects.add(aspect)
        
        return sorted(list(found_aspects))
    
    def extract_aspects_with_context(self, text: str, context_window: int = 20) -> Dict[str, List[str]]:
        """
        Extract aspects with surrounding context
        
        Args:
            text: Input text
            context_window: Number of characters around match for context
            
        Returns:
            Dictionary mapping aspects to context snippets
        """
        aspects_context = defaultdict(list)
        text_lower = text.lower()
        
        for aspect, pattern in self.aspect_patterns.items():
            for match in pattern.finditer(text_lower):
                start = max(0, match.start() - context_window)
                end = min(len(text), match.end() + context_window)
                context = text[start:end].strip()
                aspects_context[aspect].append(context)
        
        return dict(aspects_context)
    
    def extract_aspect_opinion_pairs(self, text: str, max_distance: int = 20) -> List[Dict[str, str]]:
        """
        Extract aspect-opinion pairs
        
        Args:
            text: Input text
            max_distance: Maximum word distance between aspect and opinion
            
        Returns:
            List of aspect-opinion pairs
        """
        pairs = []
        words = text.lower().split()
        
        # Opinion words
        positive_words = {
            'good', 'excellent', 'amazing', 'wonderful', 'fantastic', 'great',
            'lovely', 'delicious', 'fresh', 'clean', 'friendly', 'fast',
            'affordable', 'best', 'perfect', 'awesome'
        }
        negative_words = {
            'bad', 'poor', 'terrible', 'horrible', 'awful', 'disgusting',
            'slow', 'expensive', 'dirty', 'rude', 'worst', 'disappointing'
        }
        
        for i, word in enumerate(words):
            # Check if word is an opinion word
            if word in positive_words or word in negative_words:
                opinion_polarity = 'positive' if word in positive_words else 'negative'
                
                # Look for nearby aspects
                start_idx = max(0, i - max_distance)
                end_idx = min(len(words), i + max_distance + 1)
                context_words = words[start_idx:end_idx]
                context_text = ' '.join(context_words)
                
                # Check for aspects
                for aspect, keywords in self.aspect_keywords.items():
                    for keyword in keywords:
                        if keyword in context_text:
                            pairs.append({
                                'aspect': aspect,
                                'opinion': word,
                                'polarity': opinion_polarity,
                                'context': context_text
                            })
        
        return pairs
    
    def get_aspect_frequency(self, texts: List[str]) -> Dict[str, int]:
        """
        Get frequency of aspects across multiple texts
        
        Args:
            texts: List of texts
            
        Returns:
            Dictionary with aspect frequencies
        """
        frequency = defaultdict(int)
        
        for text in texts:
            aspects = self.extract_aspects(text)
            for aspect in aspects:
                frequency[aspect] += 1
        
        return dict(frequency)
    
    def add_custom_aspect(self, aspect_name: str, keywords: List[str]):
        """
        Add custom aspect with keywords
        
        Args:
            aspect_name: Name of aspect
            keywords: List of keywords for this aspect
        """
        self.aspect_keywords[aspect_name] = keywords
        # Recompile patterns
        self.aspect_patterns = self._compile_patterns()
        self.logger.info(f"Added custom aspect: {aspect_name}")
    
    def remove_aspect(self, aspect_name: str):
        """
        Remove aspect
        
        Args:
            aspect_name: Name of aspect to remove
        """
        if aspect_name in self.aspect_keywords:
            del self.aspect_keywords[aspect_name]
            self.aspect_patterns = self._compile_patterns()
            self.logger.info(f"Removed aspect: {aspect_name}")
    
    def get_available_aspects(self) -> List[str]:
        """
        Get list of available aspects
        
        Returns:
            List of aspect names
        """
        return sorted(list(self.aspect_keywords.keys()))
    
    def get_aspect_info(self, aspect_name: str) -> Dict:
        """
        Get information about an aspect
        
        Args:
            aspect_name: Name of aspect
            
        Returns:
            Aspect information
        """
        return {
            'name': aspect_name,
            'keywords': self.aspect_keywords.get(aspect_name, []),
            'num_keywords': len(self.aspect_keywords.get(aspect_name, []))
        }
