"""
Language detection module for ABSA pipeline
"""

import logging
import re
from typing import Optional, Tuple
from enum import Enum


class Language(Enum):
    """Supported languages"""
    ARABIC = "ar"
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    MULTILINGUAL = "multilingual"


class LanguageDetector:
    """Detect language and route to appropriate model"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize language detector
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("LanguageDetector")
        self.detector_method = None
        self._init_detector()
    
    def _init_detector(self):
        """Initialize the detection method"""
        try:
            import langdetect
            self.detector_method = "langdetect"
            self.logger.info("Using langdetect for language detection")
        except ImportError:
            self.logger.warning(
                "langdetect not available, using fallback method"
            )
            self.detector_method = "fallback"
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of input text
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        if not text or len(text.strip()) == 0:
            self.logger.warning("Empty text provided for language detection")
            return "unknown", 0.0
        
        try:
            if self.detector_method == "langdetect":
                return self._detect_langdetect(text)
            else:
                return self._detect_fallback(text)
        except Exception as e:
            self.logger.error(f"Error detecting language: {e}")
            return "unknown", 0.0
    
    def _detect_langdetect(self, text: str) -> Tuple[str, float]:
        """
        Detect using langdetect library
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        try:
            from langdetect import detect, detect_langs
            
            # Get all probabilities
            langs = detect_langs(text)
            if langs:
                best = langs[0]
                return best.lang, best.prob
            return "unknown", 0.0
        except Exception as e:
            self.logger.debug(f"langdetect error: {e}")
            return self._detect_fallback(text)
    
    def _detect_fallback(self, text: str) -> Tuple[str, float]:
        """
        Fallback language detection using character patterns
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        # Arabic character range: U+0600 to U+06FF
        arabic_pattern = re.compile(r'[\u0600-\u06FF]')
        arabic_chars = len(arabic_pattern.findall(text))
        
        # Latin characters
        latin_pattern = re.compile(r'[a-zA-Z]')
        latin_chars = len(latin_pattern.findall(text))
        
        total_chars = arabic_chars + latin_chars
        
        if total_chars == 0:
            return "unknown", 0.0
        
        arabic_ratio = arabic_chars / total_chars
        
        # Determine language based on character ratio
        if arabic_ratio > 0.5:
            # Check for Franco-Arabic
            if self._is_franco_arabic(text):
                return "ar", arabic_ratio
            return "ar", arabic_ratio
        elif arabic_ratio > 0.1:
            # Mixed content, likely Arabic with some Latin
            return "ar", arabic_ratio
        else:
            # Likely Latin-based language
            return "en", latin_chars / max(total_chars, 1)
    
    def _is_franco_arabic(self, text: str) -> bool:
        """
        Detect Franco-Arabic text (Arabic written in Latin characters)
        
        Args:
            text: Input text
            
        Returns:
            True if likely Franco-Arabic
        """
        franco_patterns = [
            r'\b(khoya|khoua|khayya|akhoya)\b',  # brother
            r'\b(yak|yex)\b',  # meaning
            r'\b(7abibi|7abibti)\b',  # dear
            r'\b(ra7|ray7)\b',  # go
            r'\b(3ad|3adak)\b',  # already
            r'\d+[o3a2]',  # Numbers replacing letters
        ]
        
        text_lower = text.lower()
        
        for pattern in franco_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def is_arabic(self, lang_code: str) -> bool:
        """
        Check if language is Arabic
        
        Args:
            lang_code: Language code
            
        Returns:
            True if Arabic
        """
        return lang_code.lower() in ["ar", "arabic"]
    
    def route_to_model(self, lang_code: str) -> str:
        """
        Route language to appropriate model
        
        Args:
            lang_code: Language code
            
        Returns:
            Model identifier
        """
        if self.is_arabic(lang_code):
            return "arabic"  # Will use MARBERT
        else:
            return "multilingual"  # Will use XLM-R
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get human-readable language name
        
        Args:
            lang_code: Language code
            
        Returns:
            Language name
        """
        names = {
            "ar": "Arabic",
            "en": "English",
            "fr": "French",
            "es": "Spanish",
            "de": "German",
            "pt": "Portuguese",
            "it": "Italian",
        }
        return names.get(lang_code, "Unknown")
