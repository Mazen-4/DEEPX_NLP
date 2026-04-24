"""
Text preprocessing module for ABSA pipeline
"""

import re
import logging
from typing import Optional, List


class TextPreprocessor:
    """Preprocess and normalize text"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize text preprocessor
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("TextPreprocessor")
        
        # Arabic diacritics
        self.arabic_diacritics = [
            '\u064B',  # FATHATAN
            '\u064C',  # DAMMATAN
            '\u064D',  # FATHATAN
            '\u064E',  # FATHA
            '\u064F',  # DAMMA
            '\u0650',  # KASRA
            '\u0651',  # SHADDA
            '\u0652',  # SUKUN
            '\u0653',  # MADDAH
            '\u0654',  # HAMZA ABOVE
            '\u0655',  # HAMZA BELOW
            '\u0656',  # SUBSCRIPT ALEF
            '\u0657',  # INVERTED DAMMA
            '\u0658',  # MARK NOON GHUNNA
            '\u0670',  # SUPERSCRIPT ALEF
        ]
    
    def preprocess(self, text: str, language: str = "en") -> str:
        """
        Apply full preprocessing pipeline
        
        Args:
            text: Input text
            language: Language code
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Step 1: Remove URLs
        text = self._remove_urls(text)
        
        # Step 2: Remove emails
        text = self._remove_emails(text)
        
        # Step 3: Remove extra whitespace
        text = self._normalize_whitespace(text)
        
        # Step 4: Language-specific preprocessing
        if language.lower() in ["ar", "arabic"]:
            text = self._preprocess_arabic(text)
        else:
            text = self._preprocess_latin(text)
        
        # Step 5: Remove extra whitespace again
        text = self._normalize_whitespace(text)
        
        return text.strip()
    
    def _remove_urls(self, text: str) -> str:
        """Remove URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    def _remove_emails(self, text: str) -> str:
        """Remove email addresses from text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
        return re.sub(email_pattern, '', text)
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace"""
        # Remove leading/trailing whitespace
        text = text.strip()
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _preprocess_arabic(self, text: str) -> str:
        """
        Arabic-specific preprocessing
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # Remove diacritics
        for diacritic in self.arabic_diacritics:
            text = text.replace(diacritic, '')
        
        # Normalize Arabic characters
        text = self._normalize_arabic_characters(text)
        
        # Remove Arabic numbers
        text = self._remove_arabic_numbers(text)
        
        return text
    
    def _normalize_arabic_characters(self, text: str) -> str:
        """Normalize Arabic characters"""
        # Alef variants to single Alef
        text = re.sub(r'[إأآ]', 'ا', text)
        
        # Hamza to nothing
        text = text.replace('ء', '')
        
        # Teh variants
        text = re.sub(r'ة', 'ه', text)
        
        # Yeh variants
        text = re.sub(r'[ىي]', 'ي', text)
        
        return text
    
    def _remove_arabic_numbers(self, text: str) -> str:
        """Remove Arabic-Indic numerals"""
        arabic_numbers = '٠١٢٣٤٥٦٧٨٩'
        for i, num in enumerate(arabic_numbers):
            text = text.replace(num, str(i))
        return text
    
    def _preprocess_latin(self, text: str) -> str:
        """
        Latin-based language preprocessing
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep punctuation and spaces
        text = re.sub(r'[^a-z0-9\s\.\,\!\?\-\:]', '', text)
        
        # Remove extra punctuation
        text = re.sub(r'[\.!?,;:]{2,}', '.', text)
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Split on whitespace
        tokens = text.split()
        return [t for t in tokens if t]
    
    def remove_stopwords(self, tokens: List[str], language: str = "en") -> List[str]:
        """
        Remove stopwords
        
        Args:
            tokens: List of tokens
            language: Language code
            
        Returns:
            Filtered tokens
        """
        # Simple stopword lists
        stopwords = {
            "en": {
                "the", "a", "an", "and", "or", "but", "in", "on", "at",
                "to", "for", "of", "with", "by", "from", "is", "are",
                "was", "were", "be", "been", "being"
            },
            "ar": {
                "في", "من", "إلى", "هذا", "هذه", "ذلك", "تلك", "التي",
                "الذي", "ما", "هو", "هي", "كل", "بعض", "أو", "و", "إذا",
                "لا", "نعم"
            }
        }
        
        stop_set = stopwords.get(language.lower(), set())
        return [t for t in tokens if t.lower() not in stop_set]
