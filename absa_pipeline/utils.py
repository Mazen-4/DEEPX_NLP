"""
Utility functions for ABSA pipeline
"""

import logging
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Union
from datetime import datetime


def setup_logging(log_file: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    os.makedirs(os.path.dirname(log_file) or "./logs", exist_ok=True)
    
    logger = logging.getLogger("ABSA_Pipeline")
    logger.setLevel(getattr(logging, level))
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setLevel(getattr(logging, level))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def load_json_file(file_path: str) -> Union[List, Dict]:
    """
    Load JSON file
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: Union[List, Dict], file_path: str) -> None:
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        file_path: Path to save file
    """
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv_file(data: List[Dict], file_path: str) -> None:
    """
    Save data to CSV file
    
    Args:
        data: List of dictionaries
        file_path: Path to save file
    """
    import csv
    
    if not data:
        return
    
    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def batch_generator(items: List, batch_size: int = 32):
    """
    Generate batches from list
    
    Args:
        items: List of items
        batch_size: Size of each batch
        
    Yields:
        Batch of items
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def is_franco_arabic(text: str) -> bool:
    """
    Detect Franco-Arabic text (Arabic text written in Latin characters)
    
    Args:
        text: Input text
        
    Returns:
        True if text appears to be Franco-Arabic
    """
    franco_patterns = ['7', '3', '2', 'khora', 'akhoya', 'yak', 'zaki', 'akhoya']
    text_lower = text.lower()
    
    # Check for common Franco-Arabic patterns
    count = sum(1 for pattern in franco_patterns if pattern in text_lower)
    
    # Simple heuristic: if multiple patterns found, likely Franco-Arabic
    return count > 0


def normalize_text(text: str) -> str:
    """
    Normalize text (basic cleaning)
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep punctuation
    import re
    text = re.sub(r'[^\w\s\.\,\!\?\-\؟\،]', '', text)
    
    return text.strip()


def extract_words(text: str) -> List[str]:
    """
    Extract words from text
    
    Args:
        text: Input text
        
    Returns:
        List of words
    """
    import re
    return re.findall(r'\w+', text.lower())


class Timer:
    """Context manager for measuring execution time"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, *args):
        self.end_time = datetime.now()
        self.elapsed = (self.end_time - self.start_time).total_seconds()
        print(f"{self.name} took {self.elapsed:.2f} seconds")


def flatten_list(nested_list: List[List]) -> List:
    """
    Flatten nested list
    
    Args:
        nested_list: Nested list
        
    Returns:
        Flattened list
    """
    return [item for sublist in nested_list for item in sublist]


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Merge multiple dictionaries
    
    Args:
        dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result
