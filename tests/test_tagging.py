import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.tagging import ArticleTagger


class TestArticleTagger:
    """Test cases for ArticleTagger class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tagger = ArticleTagger()
    
    def test_tag_article_elections_positive(self):
        """Test that articles with election keywords get the 'elections' tag."""
        title = "Election Commission Announces New Guidelines"
        body = "The commission has released new voting procedures."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "elections" in tags
    
    def test_tag_article_health_positive(self):
        """Test that articles with health keywords get the 'health' tag."""
        title = "New Hospital Opens in Rural Area"
        body = "The medical facility provides healthcare services to the community."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "health" in tags
    
    def test_tag_article_corruption_positive(self):
        """Test that articles with corruption keywords get the 'corruption' tag."""
        title = "Corruption Scandal Rocks Government"
        body = "Officials were arrested for accepting bribes and fraud."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "corruption" in tags
    
    def test_tag_article_negative(self):
        """Test that articles without keywords get no tags."""
        title = "Weather Forecast for Tomorrow"
        body = "Sunny skies expected with light winds."
        
        tags = self.tagger.tag_article(title, body)
        
        assert len(tags) == 0
    
    def test_tag_article_multiple_tags(self):
        """Test that articles can have multiple tags."""
        title = "Election Official Arrested for Health Fraud"
        body = "The electoral commission member was caught in a corruption scandal involving medical supplies."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "elections" in tags
        assert "health" in tags
        assert "corruption" in tags
    
    def test_tag_article_case_insensitive(self):
        """Test that keyword matching is case insensitive."""
        title = "ELECTION Results Show Tight Race"
        body = "The VOTING process was completed successfully."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "elections" in tags
    
    def test_tag_article_partial_word_not_matched(self):
        """Test that partial word matches are not counted."""
        title = "Electronics Store Opens"
        body = "The store sells various electronic devices."
        
        tags = self.tagger.tag_article(title, body)
        
        assert "elections" not in tags
    
    def test_get_available_tags(self):
        """Test that available tags are returned correctly."""
        tags = self.tagger.get_available_tags()
        
        expected_tags = ["elections", "health", "corruption"]
        assert set(tags) == set(expected_tags)
    
    def test_get_keywords_for_tag(self):
        """Test that keywords for a specific tag are returned."""
        keywords = self.tagger.get_keywords_for_tag("elections")
        
        assert "election" in keywords
        assert "vote" in keywords
        assert "campaign" in keywords
    
    def test_get_keywords_for_nonexistent_tag(self):
        """Test that empty list is returned for nonexistent tag."""
        keywords = self.tagger.get_keywords_for_tag("nonexistent")
        
        assert keywords == [] 