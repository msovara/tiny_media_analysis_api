#!/usr/bin/env python3
"""
Simple test script to verify the core functionality works.
This can be run without installing all dependencies.
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_data_loading():
    """Test that we can load the articles data."""
    try:
        with open('data/articles.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded {len(data)} articles from data/articles.json")
        return True
    except Exception as e:
        print(f"❌ Failed to load articles: {e}")
        return False

def test_tagging_logic():
    """Test the tagging logic with sample data."""
    try:
        from src.tagging import ArticleTagger
        
        tagger = ArticleTagger()
        
        # Test cases
        test_cases = [
            {
                "title": "Election Commission Announces New Guidelines",
                "body": "The commission has released new voting procedures.",
                "expected_tags": ["elections"]
            },
            {
                "title": "New Hospital Opens in Rural Area",
                "body": "The medical facility provides healthcare services.",
                "expected_tags": ["health"]
            },
            {
                "title": "Corruption Scandal Rocks Government",
                "body": "Officials were arrested for accepting bribes.",
                "expected_tags": ["corruption"]
            },
            {
                "title": "Weather Forecast for Tomorrow",
                "body": "Sunny skies expected with light winds.",
                "expected_tags": []
            }
        ]
        
        all_passed = True
        for i, test_case in enumerate(test_cases):
            tags = tagger.tag_article(test_case["title"], test_case["body"])
            expected = set(test_case["expected_tags"])
            actual = set(tags)
            
            if expected == actual:
                print(f"✅ Test case {i+1} passed: {tags}")
            else:
                print(f"❌ Test case {i+1} failed: expected {expected}, got {actual}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Failed to test tagging logic: {e}")
        return False

def test_article_processing():
    """Test processing a sample article."""
    try:
        from src.data_service import DataService
        
        # Create a temporary data service with a test file
        test_article = {
            "id": "1",
            "title": "Election Commission Announces New Guidelines",
            "body": "The commission has released new voting procedures.",
            "source": "Test News",
            "date": "2024-01-15"
        }
        
        # Write test data to temporary file
        with open('test_articles.json', 'w') as f:
            json.dump([test_article], f)
        
        # Test the data service
        data_service = DataService('test_articles.json')
        
        if len(data_service.articles) == 1:
            article = data_service.articles[0]
            if "elections" in article.tags:
                print("✅ Article processing and tagging works correctly")
                # Clean up
                os.remove('test_articles.json')
                return True
            else:
                print(f"❌ Article not tagged correctly: {article.tags}")
                return False
        else:
            print(f"❌ Expected 1 article, got {len(data_service.articles)}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to test article processing: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running simple tests...\n")
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Tagging Logic", test_tagging_logic),
        ("Article Processing", test_article_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The core functionality is working correctly.")
        print("\nTo run the full application:")
        print("1. Install Python 3.10+")
        print("2. Run: pip install -r requirements.txt")
        print("3. Run: python -m uvicorn src.main:app --reload")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 