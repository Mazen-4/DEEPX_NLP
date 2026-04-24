# Aspect-Based Sentiment Analysis (ABSA) Pipeline

A production-ready, modular Python package for performing Aspect-Based Sentiment Analysis on reviews and feedback with automatic language detection and multilingual support.

## Features

✨ **Core Features:**
- **Automatic Language Detection**: Detects Arabic, English, French, Spanish, and other languages
- **Multilingual Support**: 
  - Arabic text → MARBERT model
  - Other languages → XLM-RoBERTa model
- **Aspect Extraction**: Automatically extracts predefined aspects (service, price, quality, food, etc.)
- **Sentiment Classification**: Classifies sentiment as positive, negative, or neutral for each aspect
- **Modular Architecture**: Clean, extensible design with separate components
- **Batch Processing**: Efficient processing of multiple texts
- **Franco-Arabic Detection**: Handles Arabic text written in Latin characters
- **Multiple Output Formats**: JSON and CSV export

## Project Structure

```
absa_pipeline/
├── __init__.py                 # Package initialization
├── config.py                   # Configuration management
├── data_loader.py             # Load CSV/JSON datasets
├── language_detector.py       # Language detection & routing
├── preprocessor.py            # Text preprocessing
├── model_router.py            # Route to appropriate model
├── aspect_extractor.py        # Extract aspects from text
├── sentiment_classifier.py    # Classify sentiment
├── pipeline.py                # Main orchestrator
└── utils.py                   # Utility functions

Supporting Files:
├── requirements.txt           # Python dependencies
├── example_dataset.json       # Sample data
├── demo.py                    # Demonstration script
├── PIPELINE_README.md         # This file
```

## Installation

### 1. Clone/Download the Project
```bash
cd /Users/omarkhalifa/Downloads/DeepX_NLP
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python -c "from absa_pipeline import ABSAPipeline; print('Installation successful!')"
```

## Quick Start

### Example 1: Process Single Text

```python
from absa_pipeline import ABSAPipeline

# Initialize pipeline
pipeline = ABSAPipeline()

# Process text
text = "The food was delicious but the service was slow."
result = pipeline.process_text(text)

# View results
print(f"Language: {result['language']}")
print(f"Aspects: {result['aspects']}")

# Output:
# Language: en
# Aspects: [
#   {'aspect': 'food', 'sentiment': 'positive', 'confidence': 0.85},
#   {'aspect': 'service', 'sentiment': 'negative', 'confidence': 0.88}
# ]
```

### Example 2: Process File

```python
from absa_pipeline import ABSAPipeline

pipeline = ABSAPipeline()

# Process JSON or CSV file
results = pipeline.process_file('example_dataset.json')

# Save results
pipeline.save_results(results, format='json')

# Get statistics
stats = pipeline.get_statistics(results)
print(stats)
```

### Example 3: Batch Processing

```python
texts = [
    "Great atmosphere, friendly staff, reasonable prices",
    "الخدمة سيئة جداً والطعام بارد",
    "Excellent quality but very expensive"
]

results = pipeline.process_batch(texts)
```

### Example 4: Custom Aspects

```python
# Add custom aspect with keywords
pipeline.aspect_extractor.add_custom_aspect(
    "wifi",
    ["wifi", "internet", "connection", "network", "bandwidth"]
)

# Now the pipeline will detect "wifi" aspect
text = "Great food but the wifi connection is terrible"
result = pipeline.process_text(text)
```

## Usage Guide

### Configuration

Customize the pipeline with `PipelineConfig`:

```python
from absa_pipeline import ABSAPipeline, PipelineConfig

# Create custom configuration
config = PipelineConfig(
    BATCH_SIZE=64,
    DEVICE="cuda",  # "cpu", "cuda", or "mps"
    MAX_LENGTH=256,
    LOGGING_LEVEL="DEBUG"
)

pipeline = ABSAPipeline(config=config)
```

### Configuration Options

```python
# Model configuration
config.ARABIC_MODEL_NAME = "UBC-NLP/MARBERT"      # Arabic model
config.MULTILINGUAL_MODEL_NAME = "xlm-roberta-base"  # Multilingual model

# Aspect keywords (customize as needed)
config.ASPECT_KEYWORDS = {
    "service": ["service", "staff", "waiter", ...],
    "price": ["price", "cost", "expensive", ...],
    # ... more aspects
}

# Processing
config.BATCH_SIZE = 32
config.MAX_LENGTH = 512
config.DEVICE = "cpu"  # or "cuda", "mps"

# Output
config.SAVE_RESULTS = True
config.OUTPUT_FORMAT = "json"  # or "csv"
config.OUTPUT_DIR = "./results"

# Logging
config.LOGGING_LEVEL = "INFO"  # or "DEBUG", "WARNING"
config.LOG_FILE = "./logs/absa_pipeline.log"
```

### Data Format

#### Input: JSON Format
```json
[
  {
    "text": "The food was delicious but service was slow",
    "language": "en"  // Optional
  },
  {
    "text": "الطعام رائع جداً",
    "language": "ar"  // Optional
  }
]
```

#### Input: CSV Format
```csv
text,language
"The food was excellent",en
"الخدمة سيئة",ar
```

#### Output: JSON Format
```json
{
  "text": "The food was delicious but service was slow",
  "processed_text": "the food was delicious but service was slow",
  "language": "en",
  "language_confidence": 0.95,
  "model_route": "multilingual",
  "aspects": [
    {
      "aspect": "food",
      "sentiment": "positive",
      "confidence": 0.85
    },
    {
      "aspect": "service",
      "sentiment": "negative",
      "confidence": 0.88
    }
  ],
  "aspect_count": 2
}
```

#### Output: CSV Format
```csv
text,language,aspect,sentiment,confidence
"The food was delicious but service was slow",en,food,positive,0.85
"The food was delicious but service was slow",en,service,negative,0.88
```

### Available Aspects

Default aspects that the pipeline detects:
- **service** - Staff, waiters, hospitality
- **price** - Cost, affordability
- **quality** - Overall quality, freshness
- **food** - Dishes, meals, cuisine
- **atmosphere** - Ambiance, decor, environment
- **cleanliness** - Hygiene, sanitation
- **parking** - Parking availability/quality
- **delivery** - Delivery speed, timeliness
- **packaging** - Package condition, wrapping
- **taste** - Flavor, taste profile

### Advanced Usage

#### Language Detection
```python
# Detect language of text
lang, confidence = pipeline.language_detector.detect_language(text)
print(f"Language: {lang}, Confidence: {confidence}")

# Route to appropriate model
route = pipeline.language_detector.route_to_model(lang)
print(f"Model route: {route}")
```

#### Aspect Extraction
```python
# Extract aspects
aspects = pipeline.aspect_extractor.extract_aspects(text)
print(f"Aspects: {aspects}")

# Extract with context
aspects_context = pipeline.aspect_extractor.extract_aspects_with_context(text)

# Get aspect frequency
texts = ["...", "...", "..."]
frequency = pipeline.aspect_extractor.get_aspect_frequency(texts)
```

#### Text Preprocessing
```python
# Preprocess text
processed = pipeline.preprocessor.preprocess(text, language="ar")

# Tokenize
tokens = pipeline.preprocessor.tokenize(text)

# Remove stopwords
filtered_tokens = pipeline.preprocessor.remove_stopwords(tokens, language="en")
```

## Running the Demo

The package includes comprehensive demo scripts:

```bash
# Run all demonstrations
python demo.py
```

This will run:
1. **Language Detection Demo** - Shows language detection capabilities
2. **Single Text Processing** - Process individual texts
3. **Batch Processing** - Process multiple texts efficiently
4. **Custom Aspects** - Add and use custom aspect definitions
5. **File Processing** - Process datasets from JSON/CSV

## Command Line Usage

### Process a file and save results
```bash
python -c "
from absa_pipeline import ABSAPipeline
pipeline = ABSAPipeline()
results = pipeline.process_file('example_dataset.json')
pipeline.save_results(results)
"
```

### Process single text
```bash
python -c "
from absa_pipeline import ABSAPipeline
pipeline = ABSAPipeline()
result = pipeline.process_text('The food was amazing!')
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
"
```

## Language Support

### Supported Languages
| Language | Code | Model | Detection |
|----------|------|-------|-----------|
| Arabic | ar | MARBERT | ✓ |
| English | en | XLM-R | ✓ |
| French | fr | XLM-R | ✓ |
| Spanish | es | XLM-R | ✓ |
| German | de | XLM-R | ✓ |
| Portuguese | pt | XLM-R | ✓ |
| Italian | it | XLM-R | ✓ |
| Other | - | XLM-R | ✓ |

### Franco-Arabic Detection
The pipeline automatically detects Franco-Arabic (Arabic written in Latin characters):
- Example: "khoya zaki" (خوya زاكي) 
- Route: Detected as Arabic, uses MARBERT model

## Performance Tips

1. **GPU Acceleration**: Use `config.DEVICE = "cuda"` for faster processing
2. **Batch Processing**: Process multiple texts together using `process_batch()`
3. **Batch Size**: Adjust `BATCH_SIZE` based on available memory
4. **Model Caching**: Models are cached after first load for efficiency
5. **Preprocessing**: Text preprocessing is optimized for both Arabic and Latin scripts

## Troubleshooting

### Issue: Model download fails
```python
# Pre-download models
from transformers import AutoModel, AutoTokenizer

# Download MARBERT
AutoTokenizer.from_pretrained("UBC-NLP/MARBERT")
AutoModel.from_pretrained("UBC-NLP/MARBERT")

# Download XLM-R
AutoTokenizer.from_pretrained("xlm-roberta-base")
AutoModel.from_pretrained("xlm-roberta-base")
```

### Issue: Out of memory error
```python
# Reduce batch size and max length
config = PipelineConfig(
    BATCH_SIZE=8,
    MAX_LENGTH=256,
    DEVICE="cpu"
)
```

### Issue: Slow processing
```python
# Use GPU if available
import torch
config = PipelineConfig(
    DEVICE="cuda" if torch.cuda.is_available() else "cpu"
)
```

### Issue: Aspect not detected
```python
# Add custom aspect or keywords
pipeline.aspect_extractor.add_custom_aspect(
    "my_aspect",
    ["keyword1", "keyword2", "keyword3"]
)
```

## API Reference

### ABSAPipeline

**Main class for ABSA operations**

```python
class ABSAPipeline:
    def __init__(config: PipelineConfig = None)
    def process_file(file_path: str) -> List[Dict]
    def process_record(record: Dict) -> Dict
    def process_text(text: str, language: str = None) -> Dict
    def process_batch(texts: List[str], languages: List[str] = None) -> List[Dict]
    def save_results(results: List[Dict], output_path: str = None, format: str = "json") -> str
    def get_statistics(results: List[Dict]) -> Dict
```

### LanguageDetector

```python
class LanguageDetector:
    def detect_language(text: str) -> Tuple[str, float]
    def route_to_model(lang_code: str) -> str
    def is_arabic(lang_code: str) -> bool
```

### AspectExtractor

```python
class AspectExtractor:
    def extract_aspects(text: str) -> List[str]
    def extract_aspects_with_context(text: str, context_window: int = 20) -> Dict
    def add_custom_aspect(aspect_name: str, keywords: List[str])
    def remove_aspect(aspect_name: str)
    def get_available_aspects() -> List[str]
```

### TextPreprocessor

```python
class TextPreprocessor:
    def preprocess(text: str, language: str = "en") -> str
    def tokenize(text: str) -> List[str]
    def remove_stopwords(tokens: List[str], language: str = "en") -> List[str]
```

## Example Dataset

The package includes `example_dataset.json` with 10 sample reviews:
- 6 English reviews
- 4 Arabic reviews
- Mix of positive, negative, and neutral sentiments
- Multiple aspects discussed in each review

Use it for testing:
```bash
python demo.py
```

## Output Examples

### Single Review Processing
```json
{
  "text": "The food was absolutely delicious and fresh, but the service was painfully slow",
  "language": "en",
  "aspects": [
    {
      "aspect": "food",
      "sentiment": "positive",
      "confidence": 0.92
    },
    {
      "aspect": "service",
      "sentiment": "negative",
      "confidence": 0.88
    }
  ]
}
```

### Arabic Review
```json
{
  "text": "الطعام كان رائع جدا والجودة ممتازة، لكن السعر مرتفع جداً",
  "language": "ar",
  "aspects": [
    {
      "aspect": "food",
      "sentiment": "positive",
      "confidence": 0.90
    },
    {
      "aspect": "quality",
      "sentiment": "positive",
      "confidence": 0.89
    },
    {
      "aspect": "price",
      "sentiment": "negative",
      "confidence": 0.85
    }
  ]
}
```

### Statistics
```json
{
  "total_samples": 10,
  "languages": {
    "en": 6,
    "ar": 4
  },
  "aspects_found": {
    "food": 8,
    "service": 5,
    "price": 4,
    "quality": 3,
    "atmosphere": 2,
    "cleanliness": 1
  },
  "sentiment_distribution": {
    "positive": 15,
    "negative": 12,
    "neutral": 8
  },
  "average_aspects_per_sample": 3.5
}
```

## Customization

### Add New Aspect
```python
pipeline.aspect_extractor.add_custom_aspect(
    "delivery_time",
    ["delivery", "fast", "slow", "on-time", "delay"]
)
```

### Change Models
```python
config.ARABIC_MODEL_NAME = "CAMeL-Lab/bert-base-arabic-camelbert-da"
config.MULTILINGUAL_MODEL_NAME = "microsoft/xlm-roberta-large"
```

### Custom Sentiment Labels
```python
from absa_pipeline.sentiment_classifier import SentimentClassifier
classifier = SentimentClassifier()
classifier.set_labels(["negative", "neutral", "positive"])
```

## Requirements

- Python 3.8+
- transformers >= 4.36.0
- torch >= 2.1.0
- numpy >= 1.24.0
- langdetect >= 1.0.9
- pandas >= 2.0.0

## License

This project is provided as-is for educational and commercial use.

## Support

For issues, questions, or improvements:
1. Check the troubleshooting section
2. Review the example dataset and demo
3. Check the API reference
4. Review the code comments and docstrings

## Contributing

Contributions are welcome! Please:
1. Follow the existing code style
2. Add docstrings to new functions
3. Test with both Arabic and English text
4. Update documentation

## Acknowledgments

- MARBERT: UBC NLP Lab
- XLM-RoBERTa: Meta AI
- Hugging Face Transformers library

## Version History

### v1.0.0 (Current)
- Initial release
- Language detection and routing
- Aspect extraction
- Sentiment classification
- Batch processing
- Multiple output formats
