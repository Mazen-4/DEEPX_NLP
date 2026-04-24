# ABSA Pipeline - Complete Navigation Guide

Welcome to the ABSA Pipeline! This guide helps you navigate all the resources and get started quickly.

## 🎯 Quick Navigation

### I want to... Find my answer:

| Goal | File | Time |
|------|------|------|
| Get started in < 5 min | [quick_start.py](quick_start.py) | 5 min |
| Understand all features | [demo.py](demo.py) | 10 min |
| See advanced usage | [advanced_examples.py](advanced_examples.py) | 15 min |
| Check workflow example | [complete_workflow.py](complete_workflow.py) | 10 min |
| Verify installation | [test_pipeline.py](test_pipeline.py) | 2 min |
| Learn detailed usage | [PIPELINE_README.md](PIPELINE_README.md) | Read as needed |
| See project overview | [README.md](README.md) | 5 min |
| Understand deliverables | [DELIVERABLES.md](DELIVERABLES.md) | 10 min |

---

## 📚 Documentation Structure

### Quick References
- **[README.md](README.md)** - Project overview, features, quick start
- **[DELIVERABLES.md](DELIVERABLES.md)** - Complete list of what's included
- **[PIPELINE_README.md](PIPELINE_README.md)** - Comprehensive documentation

### Usage Guides (Scripts)
1. **[quick_start.py](quick_start.py)** - 4 quick examples (5 min)
2. **[demo.py](demo.py)** - 5 full demonstrations (10 min)
3. **[advanced_examples.py](advanced_examples.py)** - 10 advanced examples (15 min)
4. **[complete_workflow.py](complete_workflow.py)** - End-to-end workflow
5. **[test_pipeline.py](test_pipeline.py)** - Test suite

---

## 🚀 Getting Started

### Option 1: Quick Start (Recommended for First Time)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run quick start (5 minutes)
python quick_start.py

# 3. If that works, try full demo
python demo.py
```

### Option 2: Complete Workflow
```bash
# Run complete workflow with realistic data
python complete_workflow.py
```

### Option 3: Test Everything
```bash
# Verify installation with full test suite
python test_pipeline.py
```

---

## 📖 Learning Path

### Beginner (< 30 minutes)
1. Read [README.md](README.md) - Overview (5 min)
2. Run [quick_start.py](quick_start.py) - Examples (5 min)
3. Read sections 1-3 of [PIPELINE_README.md](PIPELINE_README.md) - Setup (10 min)
4. Try modifying quick_start.py with your own data (10 min)

### Intermediate (1-2 hours)
1. Run [demo.py](demo.py) - All features (10 min)
2. Run [complete_workflow.py](complete_workflow.py) - Real-world example (10 min)
3. Read sections 4-6 of [PIPELINE_README.md](PIPELINE_README.md) - Usage (30 min)
4. Try creating custom aspects and processing your data (30 min)

### Advanced (2-4 hours)
1. Run [advanced_examples.py](advanced_examples.py) - 10 examples (30 min)
2. Read [DELIVERABLES.md](DELIVERABLES.md) - Understand architecture (30 min)
3. Read remaining sections of [PIPELINE_README.md](PIPELINE_README.md) (30 min)
4. Review core modules in `absa_pipeline/` directory (30 min)
5. Create custom pipeline configuration and extend functionality (1 hour)

---

## 📂 File Organization

```
DeepX_NLP/
│
├── GETTING_STARTED.md              # ← YOU ARE HERE
├── README.md                        # Quick reference
├── DELIVERABLES.md                 # What's included
├── PIPELINE_README.md              # Complete documentation
│
├── requirements.txt                # Dependencies
├── setup.sh                        # Setup automation
│
├── quick_start.py                  # Quick start (5 min)
├── demo.py                         # Full demo (10 min)
├── advanced_examples.py            # Advanced (15 min)
├── complete_workflow.py            # Real-world workflow
├── test_pipeline.py                # Test suite
│
├── example_dataset.json            # Sample data
│
└── absa_pipeline/                  # Main package
    ├── __init__.py
    ├── config.py
    ├── pipeline.py
    ├── language_detector.py
    ├── preprocessor.py
    ├── model_router.py
    ├── aspect_extractor.py
    ├── sentiment_classifier.py
    ├── data_loader.py
    └── utils.py
```

---

## 💡 Code Examples by Use Case

### Use Case 1: Process a Single Review
```python
from absa_pipeline import ABSAPipeline

pipeline = ABSAPipeline()
result = pipeline.process_text("Great food but slow service!")

print(f"Language: {result['language']}")
for aspect in result['aspects']:
    print(f"  {aspect['aspect']}: {aspect['sentiment']}")
```
**See:** [quick_start.py](quick_start.py) - Example 1

### Use Case 2: Process Multiple Reviews (Batch)
```python
texts = ["Great food!", "Bad service", "الطعام لذيذ"]
results = pipeline.process_batch(texts)
```
**See:** [demo.py](demo.py) - Demo 2

### Use Case 3: Process Dataset File
```python
results = pipeline.process_file('reviews.json')
stats = pipeline.get_statistics(results)
pipeline.save_results(results, format='csv')
```
**See:** [demo.py](demo.py) - Demo 3

### Use Case 4: Custom Aspects
```python
pipeline.aspect_extractor.add_custom_aspect(
    "wifi_quality", ["wifi", "internet", "connection"]
)
result = pipeline.process_text("Great wifi speed!")
```
**See:** [demo.py](demo.py) - Demo 4

### Use Case 5: Language Detection
```python
lang, confidence = pipeline.language_detector.detect_language(text)
print(f"Language: {lang} ({confidence:.0%})")
```
**See:** [demo.py](demo.py) - Demo 1

### Use Case 6: Custom Configuration
```python
from absa_pipeline import PipelineConfig

config = PipelineConfig(
    BATCH_SIZE=64,
    DEVICE="cuda",
    LOGGING_LEVEL="DEBUG"
)
pipeline = ABSAPipeline(config=config)
```
**See:** [advanced_examples.py](advanced_examples.py) - Example 1

### Use Case 7: Aspect Analysis
```python
texts = ["Great service", "Poor service", "OK service"]
frequency = pipeline.aspect_extractor.get_aspect_frequency(texts)
```
**See:** [advanced_examples.py](advanced_examples.py) - Example 2

### Use Case 8: Complete Workflow with Insights
```python
# See complete_workflow.py for:
# - Data preparation
# - Language detection
# - Processing
# - Statistics
# - Insights generation
# - Recommendations
```
**See:** [complete_workflow.py](complete_workflow.py) - Full example

---

## 🔍 Feature Quick Reference

### Language Support
- Arabic (عربي) - MARBERT model
- English - XLM-RoBERTa
- French, Spanish, German, Portuguese, Italian - XLM-RoBERTa
- Auto-detected

### Default Aspects
- service, price, quality, food, atmosphere
- cleanliness, parking, delivery, packaging, taste

### Output Formats
- JSON (structured, detailed)
- CSV (tabular, easy to import)
- Statistics (aggregate metrics)

### Processing Modes
- Single text → `process_text()`
- Multiple texts → `process_batch()`
- From file → `process_file()`

### Configuration Options
- Batch size, device (CPU/GPU), max length
- Logging level, output directory
- Custom aspects and keywords

---

## 🛠️ Common Tasks

### Task: Process Reviews from a File
```bash
python -c "
from absa_pipeline import ABSAPipeline
pipeline = ABSAPipeline()
results = pipeline.process_file('my_reviews.json')
pipeline.save_results(results, format='csv')
"
```

### Task: Add New Aspect to Detection
See [advanced_examples.py](advanced_examples.py) - Example 5

### Task: Optimize for Performance
See [advanced_examples.py](advanced_examples.py) - Example 10

### Task: Analyze Sentiment by Aspect
See [advanced_examples.py](advanced_examples.py) - Example 7

### Task: Handle Edge Cases
See [advanced_examples.py](advanced_examples.py) - Example 9

### Task: Export in Multiple Formats
See [advanced_examples.py](advanced_examples.py) - Example 8

---

## 📋 Checklist for First Setup

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tests passing: `python test_pipeline.py`
- [ ] Quick start working: `python quick_start.py`
- [ ] Demo runs: `python demo.py`
- [ ] Read [README.md](README.md) - understand overview
- [ ] Read [PIPELINE_README.md](PIPELINE_README.md) - detailed guide
- [ ] Try custom example with your data

---

## 🆘 Need Help?

### Q: Where do I start?
**A:** Read [README.md](README.md) then run [quick_start.py](quick_start.py)

### Q: How do I use it?
**A:** See examples in [demo.py](demo.py) and [quick_start.py](quick_start.py)

### Q: What can it do?
**A:** See features overview in [README.md](README.md) and full list in [DELIVERABLES.md](DELIVERABLES.md)

### Q: How do I customize it?
**A:** See [advanced_examples.py](advanced_examples.py) for customization patterns

### Q: What if something doesn't work?
**A:** See "Troubleshooting" section in [PIPELINE_README.md](PIPELINE_README.md)

### Q: How do I process my data?
**A:** See [complete_workflow.py](complete_workflow.py) for end-to-end workflow

### Q: Can I use it with my own models?
**A:** Yes, see Configuration section in [PIPELINE_README.md](PIPELINE_README.md)

---

## 📞 Support Resources

| Issue | Resource |
|-------|----------|
| Installation | [PIPELINE_README.md](PIPELINE_README.md) - Installation section |
| Usage questions | [quick_start.py](quick_start.py) or [demo.py](demo.py) |
| Configuration | [advanced_examples.py](advanced_examples.py) - Example 1 |
| Troubleshooting | [PIPELINE_README.md](PIPELINE_README.md) - Troubleshooting section |
| Code documentation | Inline docstrings in `absa_pipeline/*.py` |
| Errors/Edge cases | [test_pipeline.py](test_pipeline.py) or [advanced_examples.py](advanced_examples.py) - Example 9 |

---

## 🎯 Success Milestones

Track your progress:
- ✅ **Milestone 1:** Installation complete (requires: pip install + quick_start.py runs)
- ✅ **Milestone 2:** First analysis done (requires: process single text)
- ✅ **Milestone 3:** Batch processing working (requires: process multiple texts)
- ✅ **Milestone 4:** File processing working (requires: load and process dataset)
- ✅ **Milestone 5:** Custom configuration (requires: create custom config)
- ✅ **Milestone 6:** Custom aspects (requires: add new aspect)
- ✅ **Milestone 7:** Export implemented (requires: save in JSON/CSV)
- ✅ **Milestone 8:** Statistics generated (requires: get meaningful stats)

---

## 📊 Next Steps

1. **Immediate (Now):** Run `python quick_start.py`
2. **Today:** Try `python demo.py` and `python complete_workflow.py`
3. **This week:** Process your own data using the pipeline
4. **Advanced:** Customize aspects and configuration
5. **Production:** Deploy with your own data pipeline

---

## 🎓 Key Concepts

### 1. **Language Detection**
Automatically detects language and routes to appropriate model

### 2. **Aspect Extraction**
Identifies key topics (service, price, quality, etc.) in reviews

### 3. **Sentiment Analysis**
Classifies sentiment (positive/negative/neutral) for each aspect

### 4. **Batch Processing**
Efficiently processes multiple reviews together

### 5. **Statistics & Insights**
Generates actionable insights from processed reviews

---

## 💻 System Requirements

- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB+ recommended)
- **Storage:** 2GB for models and dependencies
- **Optional:** GPU (CUDA) for faster processing

---

## 🔗 File Dependencies

```
quick_start.py
├── absa_pipeline/
│   ├── __init__.py
│   └── pipeline.py
└── example_dataset.json

demo.py
├── absa_pipeline/ (all modules)
└── example_dataset.json

advanced_examples.py
├── absa_pipeline/ (all modules)
└── Data created at runtime

complete_workflow.py
└── absa_pipeline/ (all modules)
```

---

## ✨ Pro Tips

1. **Tip:** Start with `quick_start.py` if you're new
2. **Tip:** Use `complete_workflow.py` for production examples
3. **Tip:** Check `advanced_examples.py` for customization
4. **Tip:** Review code comments for implementation details
5. **Tip:** Use GPU if available for faster processing
6. **Tip:** Export to CSV for Excel/data analysis tools
7. **Tip:** Custom aspects for domain-specific analysis
8. **Tip:** Batch processing for large datasets

---

## 🎉 Ready to Go!

You now have everything needed to perform comprehensive Aspect-Based Sentiment Analysis!

**Quick Start:**
```bash
pip install -r requirements.txt
python quick_start.py
```

**Questions?** Check [PIPELINE_README.md](PIPELINE_README.md) for detailed documentation.

**Want to see everything?** Run [demo.py](demo.py)

**Need real-world example?** Run [complete_workflow.py](complete_workflow.py)

---

Happy analyzing! 🚀
