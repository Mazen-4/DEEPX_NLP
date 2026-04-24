#!/usr/bin/env python
"""
Advanced ABSA Pipeline Usage Examples
Demonstrates advanced features and customization
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from absa_pipeline import ABSAPipeline, PipelineConfig
from absa_pipeline.aspect_extractor import AspectExtractor
from absa_pipeline.data_loader import DataLoader
from absa_pipeline.language_detector import LanguageDetector


def example_1_custom_configuration():
    """Example 1: Custom configuration"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Custom Configuration")
    print("="*60)
    
    # Create custom configuration
    config = PipelineConfig(
        BATCH_SIZE=16,
        MAX_LENGTH=256,
        DEVICE="cpu",  # Change to "cuda" for GPU
        LOGGING_LEVEL="DEBUG",
        OUTPUT_DIR="./my_results"
    )
    
    # Add custom aspects
    config.ASPECT_KEYWORDS["delivery_speed"] = [
        "delivery", "fast", "slow", "quick", "timely", "delayed"
    ]
    config.ASPECT_KEYWORDS["value_for_money"] = [
        "value", "worth", "overpriced", "reasonable", "expensive"
    ]
    
    pipeline = ABSAPipeline(config=config)
    
    # Process text with custom config
    text = "Fast delivery but the value for money wasn't great."
    result = pipeline.process_text(text)
    
    print(f"Result: {json.dumps(result, indent=2, ensure_ascii=False)}")


def example_2_aspect_frequency_analysis():
    """Example 2: Aspect frequency analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Aspect Frequency Analysis")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    texts = [
        "Food quality was excellent but service was slow",
        "Great atmosphere and friendly staff",
        "Amazing food and excellent service, a bit pricey though",
        "Poor quality food, terrible service",
        "Clean restaurant with reasonable prices"
    ]
    
    # Get aspect frequencies
    frequency = pipeline.aspect_extractor.get_aspect_frequency(texts)
    
    print("Aspect Frequencies:")
    sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    for aspect, count in sorted_freq:
        print(f"  {aspect}: {count}")


def example_3_multilingual_processing():
    """Example 3: Multilingual processing"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multilingual Processing")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    multilingual_texts = [
        {"text": "Excellent food quality and friendly service", "lang": "English"},
        {"text": "الطعام رائع والموظفين ودودين جداً", "lang": "Arabic"},
        {"text": "Cuisine excellente et service impeccable", "lang": "French"},
        {"text": "Comida deliciosa y servicio excelente", "lang": "Spanish"}
    ]
    
    print("Processing multilingual texts:\n")
    
    for item in multilingual_texts:
        text = item["text"]
        lang, confidence = pipeline.language_detector.detect_language(text)
        route = pipeline.language_detector.route_to_model(lang)
        
        print(f"Language: {item['lang']} (detected: {lang})")
        print(f"Text: {text}")
        print(f"Route: {route}")
        print(f"Confidence: {confidence:.3f}\n")


def example_4_advanced_aspect_extraction():
    """Example 4: Advanced aspect extraction"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Advanced Aspect Extraction")
    print("="*60)
    
    aspect_extractor = AspectExtractor()
    
    text = "The food quality was excellent and the service was friendly, though the prices were expensive"
    
    # Basic extraction
    print(f"Text: {text}\n")
    
    aspects = aspect_extractor.extract_aspects(text)
    print(f"Extracted aspects: {aspects}\n")
    
    # Extract with context
    print("Aspects with context:")
    aspects_context = aspect_extractor.extract_aspects_with_context(text)
    for aspect, contexts in aspects_context.items():
        print(f"  {aspect}:")
        for context in contexts:
            print(f"    - '{context}'")
    
    # Extract aspect-opinion pairs
    print("\nAspect-Opinion pairs:")
    pairs = aspect_extractor.extract_aspect_opinion_pairs(text)
    for pair in pairs:
        print(f"  {pair}")


def example_5_custom_aspects():
    """Example 5: Add and manage custom aspects"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Aspects Management")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    extractor = pipeline.aspect_extractor
    
    # Get available aspects
    print("Available aspects:", extractor.get_available_aspects()[:5], "...\n")
    
    # Add custom aspects
    print("Adding custom aspects...\n")
    
    extractor.add_custom_aspect(
        "online_ordering",
        ["online", "app", "website", "mobile", "ordering"]
    )
    
    extractor.add_custom_aspect(
        "wait_time",
        ["wait", "queue", "line", "reservation", "booking"]
    )
    
    # Get aspect info
    print("Custom aspect info:")
    for aspect_name in ["online_ordering", "wait_time"]:
        info = extractor.get_aspect_info(aspect_name)
        print(f"  {info}")
    
    # Use custom aspects
    text = "Great website and easy online ordering, but had to wait for 30 minutes"
    result = pipeline.process_text(text)
    
    print(f"\nProcessing text: {text}")
    print(f"Detected aspects: {[a['aspect'] for a in result['aspects']]}")


def example_6_batch_statistics():
    """Example 6: Batch processing with statistics"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Batch Statistics")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    texts = [
        "Excellent food and fast service",
        "Terrible quality and rude staff",
        "Great atmosphere but expensive",
        "Perfect everything! Highly recommended",
        "الطعام رائع والموظفين ودودين",
        "الخدمة سيئة جداً والسعر مرتفع"
    ]
    
    print(f"Processing {len(texts)} texts...\n")
    
    results = pipeline.process_batch(texts)
    
    # Get statistics
    stats = pipeline.get_statistics(results)
    
    print("Results Statistics:")
    print(f"  Total samples: {stats['total_samples']}")
    print(f"  Languages: {stats['languages']}")
    print(f"  Average aspects per sample: {stats['average_aspects_per_sample']:.2f}")
    print(f"\n  Aspects found:")
    for aspect, count in stats['aspects_found'].items():
        print(f"    {aspect}: {count}")
    print(f"\n  Sentiment distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        print(f"    {sentiment}: {count}")


def example_7_sentiment_distribution():
    """Example 7: Analyze sentiment distribution"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Sentiment Distribution Analysis")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    # Load sample data
    loader = DataLoader()
    sample_data = loader.create_sample_data()
    
    print(f"Analyzing {len(sample_data)} sample reviews...\n")
    
    results = []
    for record in sample_data:
        result = pipeline.process_record(record)
        results.append(result)
    
    # Analyze sentiment distribution by aspect
    aspect_sentiments = {}
    
    for result in results:
        for aspect in result['aspects']:
            aspect_name = aspect['aspect']
            sentiment = aspect['sentiment']
            
            if aspect_name not in aspect_sentiments:
                aspect_sentiments[aspect_name] = {
                    'positive': 0, 'neutral': 0, 'negative': 0
                }
            
            aspect_sentiments[aspect_name][sentiment] += 1
    
    print("Sentiment distribution by aspect:")
    for aspect, sentiments in sorted(aspect_sentiments.items()):
        print(f"\n  {aspect}:")
        total = sum(sentiments.values())
        for sentiment, count in sentiments.items():
            percentage = (count / total * 100) if total > 0 else 0
            print(f"    {sentiment}: {count} ({percentage:.1f}%)")


def example_8_export_formats():
    """Example 8: Export results in different formats"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Export in Different Formats")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    texts = [
        "Excellent food and quick service",
        "Poor quality and slow delivery",
        "Great atmosphere but expensive prices"
    ]
    
    results = pipeline.process_batch(texts)
    
    # Save as JSON
    json_path = pipeline.save_results(results, format="json")
    print(f"Saved JSON to: {json_path}")
    
    # Save as CSV
    csv_path = pipeline.save_results(results, format="csv")
    print(f"Saved CSV to: {csv_path}")
    
    # Display JSON
    print("\nJSON Sample:")
    print(json.dumps(results[0], indent=2, ensure_ascii=False))


def example_9_error_handling():
    """Example 9: Error handling and edge cases"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Error Handling")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    test_cases = [
        {"text": "", "description": "Empty text"},
        {"text": "   ", "description": "Whitespace only"},
        {"text": "123", "description": "Numbers only"},
        {"text": "The food was good", "description": "No aspect"},
        {"text": "!!!###$$$", "description": "Special characters only"}
    ]
    
    print("Testing edge cases:\n")
    
    for case in test_cases:
        text = case["text"]
        description = case["description"]
        
        try:
            result = pipeline.process_text(text)
            status = "✓ OK"
            aspects = len(result.get('aspects', []))
        except Exception as e:
            status = f"✗ Error: {str(e)[:40]}"
            aspects = 0
        
        print(f"  {description:<25} {status:<20} Aspects: {aspects}")


def example_10_performance_optimization():
    """Example 10: Performance optimization"""
    print("\n" + "="*60)
    print("EXAMPLE 10: Performance Optimization")
    print("="*60)
    
    import time
    
    # Configuration for optimization
    config = PipelineConfig(
        BATCH_SIZE=64,
        MAX_LENGTH=256,
        DEVICE="cpu"
    )
    
    pipeline = ABSAPipeline(config=config)
    
    # Generate test data
    texts = [
        "The food was delicious but the service was slow"
    ] * 100
    
    print(f"Processing {len(texts)} texts...\n")
    
    # Time the processing
    start_time = time.time()
    results = pipeline.process_batch(texts)
    elapsed_time = time.time() - start_time
    
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    print(f"Average per text: {elapsed_time/len(texts)*1000:.1f} ms")
    print(f"Throughput: {len(texts)/elapsed_time:.1f} texts/sec")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("ADVANCED ABSA PIPELINE EXAMPLES")
    print("="*60)
    
    examples = [
        ("Custom Configuration", example_1_custom_configuration),
        ("Aspect Frequency Analysis", example_2_aspect_frequency_analysis),
        ("Multilingual Processing", example_3_multilingual_processing),
        ("Advanced Aspect Extraction", example_4_advanced_aspect_extraction),
        ("Custom Aspects", example_5_custom_aspects),
        ("Batch Statistics", example_6_batch_statistics),
        ("Sentiment Distribution", example_7_sentiment_distribution),
        ("Export Formats", example_8_export_formats),
        ("Error Handling", example_9_error_handling),
        ("Performance Optimization", example_10_performance_optimization),
    ]
    
    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"\nError in example {i}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETED!")
    print("="*60)


if __name__ == "__main__":
    main()
