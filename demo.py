#!/usr/bin/env python
"""
ABSA Pipeline Demo Script
Demonstrates how to use the ABSA pipeline
"""

import json
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from absa_pipeline import ABSAPipeline, PipelineConfig
from absa_pipeline.utils import setup_logging


def demo_single_text():
    """Demo: Process single text"""
    print("\n" + "="*60)
    print("DEMO 1: Single Text Processing")
    print("="*60)
    
    # Initialize pipeline
    config = PipelineConfig()
    pipeline = ABSAPipeline(config=config)
    
    # Process single text
    test_texts = [
        "The food was delicious but the service was terrible.",
        "الطعام رائع والموظفين ودودين لكن السعر مرتفع جداً.",
        "Excellent quality with reasonable pricing. Clean environment!"
    ]
    
    for text in test_texts:
        print(f"\nProcessing: {text}")
        result = pipeline.process_text(text)
        print(f"Language: {result['language']}")
        print(f"Aspects: {[a['aspect'] for a in result['aspects']]}")
        print(f"Sentiments:")
        for aspect in result['aspects']:
            print(f"  - {aspect['aspect']}: {aspect['sentiment']} ({aspect['confidence']:.2f})")


def demo_file_processing():
    """Demo: Process file"""
    print("\n" + "="*60)
    print("DEMO 2: File Processing")
    print("="*60)
    
    config = PipelineConfig()
    pipeline = ABSAPipeline(config=config)
    
    # Process example dataset
    file_path = "example_dataset.json"
    
    if not Path(file_path).exists():
        print(f"Example dataset not found at {file_path}")
        print("Creating sample data for demo...")
        
        from absa_pipeline.data_loader import DataLoader
        sample_data = DataLoader.create_sample_data()
        with open(file_path, 'w') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    try:
        print(f"\nProcessing file: {file_path}")
        results = pipeline.process_file(file_path)
        
        print(f"\nProcessed {len(results)} records")
        
        # Show first few results
        print("\nFirst 3 Results:")
        for i, result in enumerate(results[:3]):
            print(f"\n--- Result {i+1} ---")
            print(f"Text: {result['text'][:80]}...")
            print(f"Language: {result['language']}")
            print(f"Aspects found: {len(result['aspects'])}")
            for aspect in result['aspects']:
                print(f"  • {aspect['aspect']}: {aspect['sentiment']}")
        
        # Save results
        output_file = pipeline.save_results(results, format="json")
        print(f"\nResults saved to: {output_file}")
        
        # Print statistics
        stats = pipeline.get_statistics(results)
        print("\nStatistics:")
        print(f"  Total samples: {stats['total_samples']}")
        print(f"  Languages: {stats['languages']}")
        print(f"  Aspects found: {dict(stats['aspects_found'])}")
        print(f"  Sentiment distribution: {stats['sentiment_distribution']}")
        print(f"  Avg aspects per sample: {stats['average_aspects_per_sample']:.2f}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()


def demo_batch_processing():
    """Demo: Batch processing"""
    print("\n" + "="*60)
    print("DEMO 3: Batch Processing")
    print("="*60)
    
    config = PipelineConfig()
    pipeline = ABSAPipeline(config=config)
    
    texts = [
        "Amazing food quality and friendly service!",
        "Terrible delivery experience, package arrived damaged.",
        "الأسعار معقولة والموظفين ودودين جداً",
        "Poor parking situation and expensive bills."
    ]
    
    print(f"Processing {len(texts)} texts in batch...")
    results = pipeline.process_batch(texts)
    
    print(f"\nResults:")
    for i, (text, result) in enumerate(zip(texts, results)):
        print(f"\n[{i+1}] {text[:50]}...")
        for aspect in result['aspects']:
            print(f"   {aspect['aspect']}: {aspect['sentiment']}")


def demo_custom_aspects():
    """Demo: Custom aspects"""
    print("\n" + "="*60)
    print("DEMO 4: Custom Aspects")
    print("="*60)
    
    config = PipelineConfig()
    pipeline = ABSAPipeline(config=config)
    
    # Add custom aspect
    print("\nAdding custom aspect: 'wifi'")
    pipeline.aspect_extractor.add_custom_aspect(
        "wifi",
        ["wifi", "internet", "connection", "network", "5G"]
    )
    
    text = "The wifi is very fast but the service could be better."
    print(f"\nProcessing: {text}")
    result = pipeline.process_text(text)
    
    print(f"Aspects found: {[a['aspect'] for a in result['aspects']]}")


def demo_language_detection():
    """Demo: Language detection"""
    print("\n" + "="*60)
    print("DEMO 5: Language Detection")
    print("="*60)
    
    pipeline = ABSAPipeline()
    
    test_texts = [
        "The food is amazing!",
        "الطعام رائع جداً!",
        "C'est très bon!",
        "¡La comida es deliciosa!"
    ]
    
    print("\nLanguage Detection Results:")
    for text in test_texts:
        lang, confidence = pipeline.language_detector.detect_language(text)
        route = pipeline.language_detector.route_to_model(lang)
        print(f"Text: {text[:40]}")
        print(f"  Language: {lang}, Confidence: {confidence:.2f}")
        print(f"  Route: {route}")
        print()


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("ABSA PIPELINE DEMONSTRATION")
    print("="*60)
    
    try:
        # Run demos
        demo_language_detection()
        demo_single_text()
        demo_batch_processing()
        demo_custom_aspects()
        demo_file_processing()
        
        print("\n" + "="*60)
        print("ALL DEMOS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
