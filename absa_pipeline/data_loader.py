"""
Data loader module for ABSA pipeline
"""

import json
import csv
import logging
from typing import List, Dict, Union, Optional
from pathlib import Path


class DataLoader:
    """Load and parse input datasets"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize data loader
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or logging.getLogger("DataLoader")
    
    def load_file(self, file_path: str) -> List[Dict]:
        """
        Load data from CSV or JSON file
        
        Args:
            file_path: Path to input file
            
        Returns:
            List of dictionaries with text and optional language
            
        Raises:
            ValueError: If file format is not supported
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == '.json':
            return self._load_json(file_path)
        elif suffix == '.csv':
            return self._load_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """
        Load JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of dictionaries
        """
        self.logger.info(f"Loading JSON file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both list and single object
        if isinstance(data, dict):
            data = [data]
        
        self.logger.info(f"Loaded {len(data)} records from JSON")
        return self._validate_data(data)
    
    def _load_csv(self, file_path: Path) -> List[Dict]:
        """
        Load CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of dictionaries
        """
        self.logger.info(f"Loading CSV file: {file_path}")
        
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        self.logger.info(f"Loaded {len(data)} records from CSV")
        return self._validate_data(data)
    
    def _validate_data(self, data: List[Dict]) -> List[Dict]:
        """
        Validate data structure
        
        Args:
            data: Input data
            
        Returns:
            Validated data
            
        Raises:
            ValueError: If data structure is invalid
        """
        if not data:
            raise ValueError("Input data is empty")
        
        # Check for required 'text' field
        for i, record in enumerate(data):
            if 'text' not in record:
                self.logger.warning(
                    f"Record {i} missing 'text' field. Fields: {record.keys()}"
                )
            else:
                # Ensure text is string
                if not isinstance(record['text'], str):
                    record['text'] = str(record['text'])
        
        self.logger.info(f"Validated {len(data)} records")
        return data
    
    def prepare_batch(self, data: List[Dict], batch_size: int = 32):
        """
        Create batches from data
        
        Args:
            data: Input data
            batch_size: Size of each batch
            
        Yields:
            Batch of data
        """
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]
    
    @staticmethod
    def create_sample_data() -> List[Dict]:
        """
        Create sample data for testing
        
        Returns:
            Sample dataset
        """
        return [
            {
                "text": "The food was absolutely delicious but the service was terrible",
                "language": "en"
            },
            {
                "text": "الطعام كان رائع جدا والسعر معقول جدا",
                "language": "ar"
            },
            {
                "text": "Excellent quality and fair price, but the delivery was slow",
                "language": "en"
            },
            {
                "text": "الجودة عالية جداً لكن الموقف انتظار طويل جداً",
                "language": "ar"
            },
            {
                "text": "Great atmosphere, friendly staff, prices could be lower",
                "language": "en"
            }
        ]
