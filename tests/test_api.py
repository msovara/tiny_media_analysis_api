import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for API endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Tiny Media Analysis API"
        assert "endpoints" in data
    
    def test_health_check(self):
        """Test the health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_get_articles_no_filters(self):
        """Test getting all articles without filters."""
        response = client.get("/api/v1/articles")
        
        assert response.status_code == 200
        articles = response.json()
        assert isinstance(articles, list)
        assert len(articles) > 0
        
        # Check that articles have the expected structure
        article = articles[0]
        assert "id" in article
        assert "title" in article
        assert "body" in article
        assert "source" in article
        assert "date" in article
        assert "url" in article
        assert "tags" in article
        assert isinstance(article["tags"], list)
    
    def test_get_articles_filter_by_source(self):
        """Test filtering articles by source."""
        response = client.get("/api/v1/articles?source=Daily%20Nation")
        
        assert response.status_code == 200
        articles = response.json()
        
        # All articles should be from Daily Nation
        for article in articles:
            assert article["source"] == "Daily Nation"
    
    def test_get_articles_filter_by_tag(self):
        """Test filtering articles by tag."""
        response = client.get("/api/v1/articles?tag=elections")
        
        assert response.status_code == 200
        articles = response.json()
        
        # All articles should have the elections tag
        for article in articles:
            assert "elections" in article["tags"]
    
    def test_get_articles_filter_by_multiple_tags(self):
        """Test filtering articles by multiple tags."""
        response = client.get("/api/v1/articles?tag=elections&tag=health")
        
        assert response.status_code == 200
        articles = response.json()
        
        # All articles should have at least one of the specified tags
        for article in articles:
            assert "elections" in article["tags"] or "health" in article["tags"]
    
    def test_get_articles_filter_by_date_range(self):
        """Test filtering articles by date range."""
        response = client.get("/api/v1/articles?date_from=2024-01-15&date_to=2024-01-20")
        
        assert response.status_code == 200
        articles = response.json()
        
        # All articles should be within the date range
        for article in articles:
            article_date = article["date"]
            assert "2024-01-15" <= article_date <= "2024-01-20"
    
    def test_get_stats(self):
        """Test getting statistics."""
        response = client.get("/api/v1/stats")
        
        assert response.status_code == 200
        stats = response.json()
        
        assert "tags" in stats
        assert "sources" in stats
        assert "total_articles" in stats
        assert isinstance(stats["tags"], dict)
        assert isinstance(stats["sources"], dict)
        assert isinstance(stats["total_articles"], int)
        assert stats["total_articles"] > 0
    
    def test_get_articles_invalid_date_format(self):
        """Test that invalid date format returns all articles (graceful handling)."""
        response = client.get("/api/v1/articles?date_from=invalid-date")
        
        assert response.status_code == 200
        # Should still return articles (invalid date is ignored)
        articles = response.json()
        assert isinstance(articles, list)
    
    def test_get_articles_nonexistent_source(self):
        """Test filtering by nonexistent source returns empty list."""
        response = client.get("/api/v1/articles?source=NonexistentSource")
        
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0
    
    def test_get_articles_nonexistent_tag(self):
        """Test filtering by nonexistent tag returns empty list."""
        response = client.get("/api/v1/articles?tag=nonexistent")
        
        assert response.status_code == 200
        articles = response.json()
        assert len(articles) == 0 