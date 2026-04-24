#!/usr/bin/env python
"""
Test Suite for ABSA Pipeline
Verifies all components work correctly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from absa_pipeline import ABSAPipeline, PipelineConfig
        from absa_pipeline.data_loader import DataLoader
        from absa_pipeline.language_detector import LanguageDetector
        from absa_pipeline.preprocessor import TextPreprocessor
        from absa_pipeline.model_router import ModelRouter
        from absa_pipeline.aspect_extractor import AspectExtractor
        from absa_pipeline.sentiment_classifier import SentimentClassifier
        print("✓ All imports successful\n")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}\n")
        return False


def test_data_loader():
    """Test data loader"""
    print("Testing data loader...")
    try:
        from absa_pipeline.data_loader import DataLoader
        loader = DataLoader()
        
        # Test sample data creation
        sample_data = loader.create_sample_data()
        assert len(sample_data) > 0, "Sample data is empty"
        assert 'text' in sample_data[0], "Missing 'text' field"
        
        print(f"✓ Data loader works (loaded {len(sample_data)} samples)\n")
        return True
    except Exception as e:
        print(f"✗ Data loader test failed: {e}\n")
        return False


def test_language_detector():
    """Test language detection"""
    print("Testing language detector...")
    try:
        from absa_pipeline.language_detector import LanguageDetector
        detector = LanguageDetector()
        
        test_texts = [
            "Hello, how are you?",
            "مرحبا، كيف حالك؟",
        ]
        
        for text in test_texts:
            lang, conf = detector.detect_language(text)
            assert lang != "unknown", f"Could not detect language for: {text}"
        
        print("✓ Language detector works\n")
        return True
    except Exception as e:
        print(f"✗ Language detector test failed: {e}\n")
        return False


def test_preprocessor():
    """Test text preprocessor"""
    print("Testing text preprocessor...")
    try:
        from absa_pipeline.preprocessor import TextPreprocessor
        preprocessor = TextPreprocessor()
        
        test_text = "The food was AMAZING!!!  Check it out @ example.com"
        processed = preprocessor.preprocess(test_text, language="en")
        
        assert len(processed) > 0, "Preprocessor produced empty output"
        assert "example.com" not in processed, "URLs not removed"
        
        print(f"✓ Text preprocessor works\n")
        return True
    except Exception as e:
        print(f"✗ Preprocessor test failed: {e}\n")
        return False


def test_aspect_extractor():
    """Test aspect extraction"""
    print("Testing aspect extractor...")
    try:
        from absa_pipeline.aspect_extractor import AspectExtractor
        extractor = AspectExtractor()
        
        test_text = "The food quality was excellent and the service was terrible"
        aspects = extractor.extract_aspects(test_text)
        
        assert len(aspects) > 0, "No aspects found"
        assert "food" in aspects or "quality" in aspects, "Expected aspects not found"
        
        # Test custom aspect
        extractor.add_custom_aspect("delivery", ["delivery", "fast", "slow"])
        test_text2 = "Fast delivery"
        aspects2 = extractor.extract_aspects(test_text2)
        assert "delivery" in aspects2, "Custom aspect not working"
        
        print("✓ Aspect extractor works\n")
        return True
    except Exception as e:
        print(f"✗ Aspect extractor test failed: {e}\n")
        return False


def test_model_router():
    """Test model router"""
    print("Testing model router...")
    try:
        from absa_pipeline.model_router import ModelRouter
        router = ModelRouter()
        
        # Test routing
        assert router.route("ar") == "arabic", "Arabic routing failed"
        assert router.route("en") == "multilingual", "English routing failed"
        
        # Test model config
        config = router.get_model_config("arabic")
        assert "name" in config, "Model config missing name"
        assert "MARBERT" in config["name"], "Wrong model for Arabic"
        
        print("✓ Model router works\n")
        return True
    except Exception as e:
        print(f"✗ Model router test failed: {e}\n")
        return False


def test_pipeline():
    """Test main pipeline"""
    print("Testing main ABSA pipeline...")
    try:
        from absa_pipeline import ABSAPipeline
        pipeline = ABSAPipeline()
        
        # Test single text processing
        result = pipeline.process_text("The food was great but service was slow")
        assert "language" in result, "Missing language in result"
        assert "aspects" in result, "Missing aspects in result"
        
        # Test batch processing
        texts = ["Great food!", "Bad service"]
        results = pipeline.process_batch(texts)
        assert len(results) == 2, "Batch processing returned wrong count"
        
        print("✓ ABSA pipeline works\n")
        return True
    except Exception as e:
        print(f"✗ ABSA pipeline test failed: {e}\n")
        return False


def test_configuration():
    """Test configuration"""
    print("Testing configuration...")
    try:
        from absa_pipeline import PipelineConfig
        
        config = PipelineConfig(
            BATCH_SIZE=16,
            MAX_LENGTH=256,
            DEVICE="cpu"
        )
        
        assert config.BATCH_SIZE == 16, "Configuration not set correctly"
        assert len(config.ASPECTS_TO_EXTRACT) > 0, "No aspects configured"
        assert len(config.ASPECT_KEYWORDS) > 0, "No aspect keywords"
        
        print("✓ Configuration works\n")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}\n")
        return False


def test_utils():
    """Test utility functions"""
    print("Testing utility functions...")
    try:
        from absa_pipeline.utils import (
            normalize_text, extract_words, is_franco_arabic,
            batch_generator, Timer
        )
        
        # Test text normalization
        text = "  Hello    World  "
        normalized = normalize_text(text)
        assert normalized == "Hello World", "Text normalization failed"
        
        # Test batch generator
        items = list(range(10))
        batches = list(batch_generator(items, batch_size=3))
        assert len(batches) == 4, "Batch generator failed"
        
        # Test timer
        with Timer("Test"):
            pass
        
        print("✓ Utility functions work\n")
        return True
    except Exception as e:
        print(f"✗ Utility functions test failed: {e}\n")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("ABSA PIPELINE TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_configuration,
        test_data_loader,
        test_language_detector,
        test_preprocessor,
        test_aspect_extractor,
        test_model_router,
        test_utils,
        test_pipeline,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Unexpected error in {test.__name__}: {e}\n")
            results.append(False)
    
    # Summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
