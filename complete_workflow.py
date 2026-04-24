#!/usr/bin/env python
"""
Complete Workflow Example - From Raw Data to Insights
Shows the complete pipeline workflow with realistic data
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from absa_pipeline import ABSAPipeline, PipelineConfig
from absa_pipeline.utils import save_json_file


def workflow_complete():
    """Complete workflow example"""
    
    print("="*70)
    print("COMPLETE ABSA PIPELINE WORKFLOW")
    print("="*70)
    
    # =========================================================================
    # STEP 1: CONFIGURATION
    # =========================================================================
    print("\n[STEP 1] Configuration Setup")
    print("-" * 70)
    
    config = PipelineConfig(
        BATCH_SIZE=32,
        DEVICE="cpu",
        OUTPUT_DIR="./workflow_results",
        LOGGING_LEVEL="INFO"
    )
    
    print("✓ Configuration created")
    print(f"  - Batch size: {config.BATCH_SIZE}")
    print(f"  - Device: {config.DEVICE}")
    print(f"  - Output directory: {config.OUTPUT_DIR}")
    
    # =========================================================================
    # STEP 2: INITIALIZE PIPELINE
    # =========================================================================
    print("\n[STEP 2] Initialize Pipeline")
    print("-" * 70)
    
    pipeline = ABSAPipeline(config=config)
    print("✓ Pipeline initialized with all components")
    print(f"  - Available aspects: {len(pipeline.aspect_extractor.get_available_aspects())}")
    print(f"  - Supported routes: {pipeline.model_router.get_available_routes()}")
    
    # =========================================================================
    # STEP 3: PREPARE DATA
    # =========================================================================
    print("\n[STEP 3] Prepare Input Data")
    print("-" * 70)
    
    # Real-world sample data
    raw_data = [
        {
            "id": 1,
            "text": "Fantastic experience! The food quality was exceptional and the staff were incredibly friendly. Highly recommended!",
            "source": "Google Reviews"
        },
        {
            "id": 2,
            "text": "Disappointing visit. Cold food, slow service, but decent prices and clean environment.",
            "source": "Yelp"
        },
        {
            "id": 3,
            "text": "The burger was delicious and juicy. Service was fast. Unfortunately the parking situation is terrible.",
            "source": "TripAdvisor"
        },
        {
            "id": 4,
            "text": "الطعام رائع جداً والموظفين ودودين جداً. الأسعار معقولة. أنصح الجميع بزيارة هذا المكان",
            "source": "Google Reviews (Arabic)"
        },
        {
            "id": 5,
            "text": "خدمة سيئة جداً وطعام بارد. السعر غالي مقابل الجودة. لن أعود",
            "source": "Yelp (Arabic)"
        }
    ]
    
    print(f"✓ Loaded {len(raw_data)} raw reviews")
    print("  Sample reviews:")
    for i, review in enumerate(raw_data[:2], 1):
        print(f"    [{i}] {review['text'][:60]}...")
    
    # =========================================================================
    # STEP 4: LANGUAGE DETECTION
    # =========================================================================
    print("\n[STEP 4] Language Detection & Analysis")
    print("-" * 70)
    
    language_stats = {}
    for review in raw_data:
        text = review['text']
        lang, confidence = pipeline.language_detector.detect_language(text)
        if lang not in language_stats:
            language_stats[lang] = 0
        language_stats[lang] += 1
    
    print("✓ Language detection completed")
    print("  Language distribution:")
    for lang, count in language_stats.items():
        print(f"    - {lang.upper()}: {count} reviews")
    
    # =========================================================================
    # STEP 5: PROCESS ALL REVIEWS
    # =========================================================================
    print("\n[STEP 5] Process Reviews Through Pipeline")
    print("-" * 70)
    
    results = []
    for i, review in enumerate(raw_data, 1):
        # Process
        result = pipeline.process_text(review['text'])
        
        # Attach metadata
        result['id'] = review['id']
        result['source'] = review['source']
        results.append(result)
        
        # Show progress
        lang = result['language']
        aspect_count = len(result['aspects'])
        print(f"  [{i}/{len(raw_data)}] {lang.upper():<2} | "
              f"{aspect_count} aspects | "
              f"{result['text'][:50]}...")
    
    print("\n✓ All reviews processed successfully")
    
    # =========================================================================
    # STEP 6: ANALYZE RESULTS
    # =========================================================================
    print("\n[STEP 6] Analysis & Statistics")
    print("-" * 70)
    
    stats = pipeline.get_statistics(results)
    
    print("✓ Statistics Generated:")
    print(f"  Total Samples: {stats['total_samples']}")
    print(f"  Languages: {stats['languages']}")
    print(f"  Avg Aspects per Review: {stats['average_aspects_per_sample']:.2f}")
    
    print("\n  Top Aspects:")
    sorted_aspects = sorted(
        stats['aspects_found'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    for aspect, count in sorted_aspects:
        print(f"    - {aspect}: {count} times")
    
    print("\n  Sentiment Distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        percentage = (count / sum(stats['sentiment_distribution'].values())) * 100
        print(f"    - {sentiment}: {count} ({percentage:.1f}%)")
    
    # =========================================================================
    # STEP 7: DETAILED INSIGHTS
    # =========================================================================
    print("\n[STEP 7] Detailed Insights by Aspect")
    print("-" * 70)
    
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
    
    print("✓ Sentiment by Aspect:")
    for aspect in sorted(aspect_sentiments.keys()):
        sentiments = aspect_sentiments[aspect]
        total = sum(sentiments.values())
        print(f"\n  {aspect.upper()}:")
        for sentiment in ['positive', 'negative', 'neutral']:
            count = sentiments.get(sentiment, 0)
            pct = (count / total * 100) if total > 0 else 0
            print(f"    - {sentiment}: {count} ({pct:.0f}%)")
    
    # =========================================================================
    # STEP 8: DETAILED RESULTS
    # =========================================================================
    print("\n[STEP 8] Detailed Results for Each Review")
    print("-" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\nReview #{result['id']} ({result['source']})")
        print(f"Language: {result['language']} | Text: {result['text'][:70]}...")
        
        if result['aspects']:
            print("Aspects & Sentiments:")
            for aspect in result['aspects']:
                sentiment = aspect['sentiment']
                confidence = aspect['confidence']
                print(f"  • {aspect['aspect']}: {sentiment} ({confidence:.0%} confidence)")
        else:
            print("No aspects found in this review")
    
    # =========================================================================
    # STEP 9: EXPORT RESULTS
    # =========================================================================
    print("\n[STEP 9] Export Results")
    print("-" * 70)
    
    # Prepare export data with insights
    export_data = {
        "metadata": {
            "total_reviews": len(results),
            "statistics": stats,
            "aspect_sentiments": aspect_sentiments
        },
        "reviews": results
    }
    
    # Save JSON
    json_file = pipeline.save_results(results, format="json")
    print(f"✓ JSON export: {json_file}")
    
    # Save CSV
    csv_file = pipeline.save_results(results, format="csv")
    print(f"✓ CSV export: {csv_file}")
    
    # Save comprehensive JSON with insights
    insights_file = f"{config.OUTPUT_DIR}/comprehensive_insights.json"
    save_json_file(export_data, insights_file)
    print(f"✓ Comprehensive insights: {insights_file}")
    
    # =========================================================================
    # STEP 10: KEY RECOMMENDATIONS
    # =========================================================================
    print("\n[STEP 10] Business Insights & Recommendations")
    print("-" * 70)
    
    print("\n✓ Key Findings:")
    
    # Find most problematic aspects
    negative_aspects = {}
    for aspect, sentiments in aspect_sentiments.items():
        if sentiments['negative'] > 0:
            negative_aspects[aspect] = sentiments['negative']
    
    if negative_aspects:
        print("\n  Areas of Concern:")
        for aspect, count in sorted(negative_aspects.items(), key=lambda x: x[1], reverse=True):
            print(f"    • {aspect}: {count} negative mentions")
    
    # Find strengths
    positive_aspects = {}
    for aspect, sentiments in aspect_sentiments.items():
        if sentiments['positive'] > 0:
            positive_aspects[aspect] = sentiments['positive']
    
    if positive_aspects:
        print("\n  Strengths:")
        for aspect, count in sorted(positive_aspects.items(), key=lambda x: x[1], reverse=True):
            print(f"    • {aspect}: {count} positive mentions")
    
    print("\n✓ Recommendations:")
    
    # Generate recommendations
    recommendations = []
    
    if 'service' in negative_aspects:
        recommendations.append("Improve staff training and service speed")
    
    if 'price' in negative_aspects:
        recommendations.append("Review pricing strategy or improve value perception")
    
    if 'parking' in negative_aspects:
        recommendations.append("Address parking issues (signage, availability, or quality)")
    
    if 'delivery' in negative_aspects:
        recommendations.append("Optimize delivery process and timing")
    
    if 'food' in positive_aspects:
        recommendations.append("Leverage positive food reviews in marketing")
    
    if 'atmosphere' in positive_aspects:
        recommendations.append("Highlight ambiance as a key differentiator")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("  • All aspects performing well - maintain current quality")
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE!")
    print("="*70)
    
    print(f"\n✓ Processed: {len(results)} reviews")
    print(f"✓ Languages detected: {len(stats['languages'])}")
    print(f"✓ Aspects analyzed: {len(aspect_sentiments)}")
    print(f"✓ Outputs generated:")
    print(f"  - JSON results: {json_file}")
    print(f"  - CSV results: {csv_file}")
    print(f"  - Insights: {insights_file}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        workflow_complete()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
