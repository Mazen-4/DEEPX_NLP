#!/usr/bin/env python
"""
Quick Start Guide for ABSA Pipeline
Minimal example to get started in < 5 minutes
"""

import json
from absa_pipeline import ABSAPipeline

# =============================================================================
# QUICK START #1: Single Text Analysis (30 seconds)
# =============================================================================

print("="*60)
print("QUICK START #1: Single Text Analysis")
print("="*60)

# Create pipeline
pipeline = ABSAPipeline()

# Analyze a review
text = "The food was amazing and the service was fast, but it's quite expensive."
result = pipeline.process_text(text)

print(f"\nText: {text}")
print(f"\nLanguage: {result['language']}")
print(f"Aspects and Sentiments:")
for aspect in result['aspects']:
    print(f"  • {aspect['aspect']}: {aspect['sentiment']} ({aspect['confidence']:.0%})")


# =============================================================================
# QUICK START #2: Multiple Reviews (1 minute)
# =============================================================================

print("\n" + "="*60)
print("QUICK START #2: Batch Analysis")
print("="*60)

reviews = [
    "Excellent quality, reasonable prices, friendly staff!",
    "Terrible experience. Cold food, rude service.",
    "الطعام لذيذ جداً والموظفين ودودين"
]

results = pipeline.process_batch(reviews)

for i, (review, result) in enumerate(zip(reviews, results), 1):
    print(f"\n[Review {i}] {review[:50]}...")
    print(f"Language: {result['language']}")
    for aspect in result['aspects']:
        print(f"  {aspect['aspect']}: {aspect['sentiment']}")


# =============================================================================
# QUICK START #3: File Processing (2 minutes)
# =============================================================================

print("\n" + "="*60)
print("QUICK START #3: Process from File")
print("="*60)

try:
    results = pipeline.process_file('example_dataset.json')
    
    print(f"\nProcessed {len(results)} reviews")
    
    # Get statistics
    stats = pipeline.get_statistics(results)
    print(f"\nStatistics:")
    print(f"  Total reviews: {stats['total_samples']}")
    print(f"  Languages: {list(stats['languages'].keys())}")
    print(f"  Avg aspects per review: {stats['average_aspects_per_sample']:.1f}")
    
    # Save results
    output_file = pipeline.save_results(results)
    print(f"\nResults saved to: {output_file}")
    
except Exception as e:
    print(f"Note: {e}")
    print("Make sure example_dataset.json exists in the current directory")


# =============================================================================
# QUICK START #4: Customize Aspects (2 minutes)
# =============================================================================

print("\n" + "="*60)
print("QUICK START #4: Custom Aspects")
print("="*60)

# Add custom aspect
pipeline.aspect_extractor.add_custom_aspect(
    "wifi_quality",
    ["wifi", "internet", "connection", "network", "bandwidth"]
)

text = "Great food and the wifi is super fast!"
result = pipeline.process_text(text)

print(f"\nText: {text}")
print(f"Detected aspects: {[a['aspect'] for a in result['aspects']]}")


# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "="*60)
print("WHAT'S NEXT?")
print("="*60)

print("""
1. Run the full demo:
   python demo.py

2. Run advanced examples:
   python advanced_examples.py

3. Customize configuration:
   from absa_pipeline import PipelineConfig
   config = PipelineConfig(BATCH_SIZE=64, DEVICE="cuda")

4. Read full documentation:
   cat PIPELINE_README.md

5. Try with your own data:
   pipeline.process_file('your_dataset.json')

For more info:
   - Check PIPELINE_README.md for complete documentation
   - Review demo.py for comprehensive examples
   - Check advanced_examples.py for advanced usage
""")

print("="*60)
