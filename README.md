# DeepX NLP - Aspect-Based Sentiment Analysis Pipeline

This repository contains a complete, production-ready **Aspect-Based Sentiment Analysis (ABSA) Pipeline** for analyzing reviews and feedback with automatic language detection and multilingual support.

## Quick Overview

The ABSA pipeline automatically:
- ✅ Detects language (Arabic, English, French, Spanish, etc.)
- ✅ Routes to appropriate model (MARBERT for Arabic, XLM-R for multilingual)
- ✅ Extracts aspects (service, price, quality, food, atmosphere, etc.)
- ✅ Classifies sentiment (positive, negative, neutral) for each aspect
- ✅ Produces structured output in JSON or CSV format

## Quick Start (< 2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Try It Now
```bash
python quick_start.py
```

### 3. Basic Usage
```python
from absa_pipeline import ABSAPipeline

pipeline = ABSAPipeline()

# Single text
result = pipeline.process_text("The food was delicious but service was slow.")

# Multiple texts
results = pipeline.process_batch([
    "Great food, friendly staff",
    "Terrible delivery, amazing quality"
])

# From file
results = pipeline.process_file('example_dataset.json')

# Save results
pipeline.save_results(results, format='json')
```

## Key Features

🎯 **Core Features:**
- Automatic language detection with confidence scores
- Dynamic model routing based on language
- Multi-aspect extraction from reviews
- Sentiment polarity classification
- Batch processing for efficiency
- Franco-Arabic text handling
- Multiple output formats (JSON, CSV)
- Comprehensive logging

🌍 **Language Support:**
- Arabic (عربي) - Uses MARBERT
- English - Uses XLM-RoBERTa
- French, Spanish, German, Portuguese, Italian - Uses XLM-RoBERTa
- Auto-detection of language

## Project Structure

```
├── absa_pipeline/              # Main package
│   ├── __init__.py
│   ├── config.py               # Configuration
│   ├── pipeline.py             # Main orchestrator
│   ├── language_detector.py    # Language detection & routing
│   ├── preprocessor.py         # Text preprocessing
│   ├── data_loader.py          # Load datasets
│   ├── aspect_extractor.py     # Extract aspects
│   ├── sentiment_classifier.py # Classify sentiment
│   ├── model_router.py         # Model routing
│   └── utils.py                # Helper functions
│
├── demo.py                     # Full demonstration
├── quick_start.py              # Quick start guide
├── advanced_examples.py        # Advanced usage examples
├── example_dataset.json        # Sample data
├── requirements.txt            # Dependencies
├── PIPELINE_README.md          # Full documentation
└── README.md                   # This file
```

## Usage Examples

### Example 1: Single Text Analysis
```python
from absa_pipeline import ABSAPipeline

pipeline = ABSAPipeline()
result = pipeline.process_text("Amazing food but terrible service!")

# Output:
# {
#   "text": "Amazing food but terrible service!",
#   "language": "en",
#   "aspects": [
#     {"aspect": "food", "sentiment": "positive", "confidence": 0.92},
#     {"aspect": "service", "sentiment": "negative", "confidence": 0.88}
#   ]
# }
```

### Example 2: Arabic Text
```python
result = pipeline.process_text("الطعام رائع والخدمة سيئة جداً")

# Automatically detects Arabic and uses MARBERT model
# {
#   "text": "الطعام رائع والخدمة سيئة جداً",
#   "language": "ar",
#   "aspects": [
#     {"aspect": "food", "sentiment": "positive", "confidence": 0.95},
#     {"aspect": "service", "sentiment": "negative", "confidence": 0.90}
#   ]
# }
```

### Example 3: Batch Processing
```python
texts = [
    "Great food and quick service",
    "الطعام لذيذ والموظفين ودودين",
    "Excelente calidad, precios razonables"
]

results = pipeline.process_batch(texts)
```

### Example 4: Process File
```python
results = pipeline.process_file('example_dataset.json')

# Statistics
stats = pipeline.get_statistics(results)
print(f"Total reviews: {stats['total_samples']}")
print(f"Languages: {stats['languages']}")
print(f"Avg aspects per review: {stats['average_aspects_per_sample']}")

# Save results
pipeline.save_results(results, format='json')  # or 'csv'
```

### Example 5: Custom Aspects
```python
# Add custom aspect
pipeline.aspect_extractor.add_custom_aspect(
    "wifi_quality",
    ["wifi", "internet", "connection", "network"]
)

result = pipeline.process_text("Great food and the wifi is amazing!")
# Now detects "wifi_quality" aspect
```

## Output Format

### JSON Output
```json
{
  "text": "The food was delicious but service was slow",
  "language": "en",
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
  ]
}
```

### CSV Output
```csv
text,language,aspect,sentiment,confidence
"The food was delicious but service was slow",en,food,positive,0.85
"The food was delicious but service was slow",en,service,negative,0.88
```

## Running Examples

```bash
# Quick start (2 minutes)
python quick_start.py

# Full demonstration (10 minutes)
python demo.py

# Advanced examples (15 minutes)
python advanced_examples.py
```

## Default Aspects

The pipeline detects these aspects by default:
- **service** - Staff, waiters, hospitality
- **price** - Cost, affordability, expenses
- **quality** - Overall quality, freshness
- **food** - Dishes, meals, cuisine
- **atmosphere** - Ambiance, environment, decor
- **cleanliness** - Hygiene, sanitation
- **parking** - Parking availability
- **delivery** - Delivery speed, timeliness
- **packaging** - Package condition
- **taste** - Flavor, taste profile

## Configuration

```python
from absa_pipeline import PipelineConfig, ABSAPipeline

config = PipelineConfig(
    BATCH_SIZE=64,
    DEVICE="cuda",  # "cpu", "cuda", or "mps"
    MAX_LENGTH=256,
    LOGGING_LEVEL="INFO"
)

pipeline = ABSAPipeline(config=config)
```

## Supported Languages

| Language | Code | Model |
|----------|------|-------|
| Arabic | ar | MARBERT |
| English | en | XLM-RoBERTa |
| French | fr | XLM-RoBERTa |
| Spanish | es | XLM-RoBERTa |
| German | de | XLM-RoBERTa |
| Portuguese | pt | XLM-RoBERTa |
| Italian | it | XLM-RoBERTa |

## API Reference

### Main Pipeline Class

```python
class ABSAPipeline:
    def __init__(config: PipelineConfig = None)
    def process_text(text: str, language: str = None) -> Dict
    def process_batch(texts: List[str]) -> List[Dict]
    def process_file(file_path: str) -> List[Dict]
    def save_results(results: List[Dict], output_path: str = None, format: str = "json") -> str
    def get_statistics(results: List[Dict]) -> Dict
```

## Requirements

- Python 3.8+
- transformers >= 4.36.0
- torch >= 2.1.0
- numpy >= 1.24.0
- langdetect >= 1.0.9
- pandas >= 2.0.0

## Troubleshooting

**Q: Models are not downloading**
```python
from transformers import AutoModel, AutoTokenizer
AutoTokenizer.from_pretrained("UBC-NLP/MARBERT")
```

**Q: Out of memory errors**
```python
config = PipelineConfig(BATCH_SIZE=8, DEVICE="cpu")
```

**Q: Slow processing**
```python
# Use GPU if available
config = PipelineConfig(DEVICE="cuda")
```

## Documentation

For complete documentation, see [PIPELINE_README.md](PIPELINE_README.md)

This includes:
- Detailed installation instructions
- Advanced configuration
- Custom aspect management
- Performance optimization
- API reference
- Troubleshooting guide

## Example Dataset

The package includes `example_dataset.json` with 10 sample reviews in both English and Arabic.

Use it to test the pipeline:
```bash
python demo.py
```

## Links

Dataset source: d1y8zswxjnvm73.cloudfront.net