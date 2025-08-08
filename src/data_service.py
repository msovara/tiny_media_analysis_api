import json
from typing import List, Dict, Optional
from datetime import datetime, date
from .models import Article, ArticleResponse
from .tagging import ArticleTagger


class DataService:
    """Service for managing article data and operations."""
    
    def __init__(self, data_file: str = "data/articles.json"):
        self.data_file = data_file
        self.articles: List[Article] = []
        self.tagger = ArticleTagger()
        self._load_data()
    
    def _load_data(self):
        """Load articles from JSON file and tag them."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                raw_articles = json.load(f)
            
            for article_data in raw_articles:
                # Tag the article
                tags = self.tagger.tag_article(
                    article_data['title'], 
                    article_data['body']
                )
                
                # Create Article object with tags
                article = Article(
                    id=int(article_data['id']),  # Convert string ID to int
                    title=article_data['title'],
                    body=article_data['body'],
                    source=article_data['source'],
                    date=article_data['date'],
                    url=article_data.get('url', ''),  # Handle missing url field
                    tags=tags
                )
                self.articles.append(article)
                
        except FileNotFoundError:
            print(f"Warning: Data file {self.data_file} not found.")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file: {e}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_articles(
        self,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[ArticleResponse]:
        """
        Get articles with optional filtering.
        
        Args:
            source: Filter by source name
            tags: Filter by tags (articles must have at least one of these tags)
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
            
        Returns:
            Filtered list of articles
        """
        filtered_articles = self.articles.copy()
        
        # Filter by source
        if source:
            filtered_articles = [
                article for article in filtered_articles 
                if article.source.lower() == source.lower()
            ]
        
        # Filter by tags
        if tags:
            filtered_articles = [
                article for article in filtered_articles
                if any(tag in article.tags for tag in tags)
            ]
        
        # Filter by date range
        if date_from or date_to:
            filtered_articles = self._filter_by_date_range(
                filtered_articles, date_from, date_to
            )
        
        # Convert to response format
        return [
            ArticleResponse(
                id=article.id,
                title=article.title,
                body=article.body,
                source=article.source,
                date=article.date,
                url=article.url or "",
                tags=article.tags
            )
            for article in filtered_articles
        ]
    
    def _filter_by_date_range(
        self,
        articles: List[Article],
        date_from: Optional[str],
        date_to: Optional[str]
    ) -> List[Article]:
        """Filter articles by date range."""
        filtered = articles
        
        if date_from:
            try:
                from_date = datetime.strptime(date_from, "%Y-%m-%d").date()
                filtered = [
                    article for article in filtered
                    if datetime.strptime(article.date, "%Y-%m-%d").date() >= from_date
                ]
            except ValueError:
                print(f"Invalid date_from format: {date_from}")
        
        if date_to:
            try:
                to_date = datetime.strptime(date_to, "%Y-%m-%d").date()
                filtered = [
                    article for article in filtered
                    if datetime.strptime(article.date, "%Y-%m-%d").date() <= to_date
                ]
            except ValueError:
                print(f"Invalid date_to format: {date_to}")
        
        return filtered
    
    def get_stats(self) -> Dict:
        """Get statistics about articles, tags, and sources."""
        # Count by tags
        tag_counts = {}
        for article in self.articles:
            for tag in article.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count by sources
        source_counts = {}
        for article in self.articles:
            source_counts[article.source] = source_counts.get(article.source, 0) + 1
        
        return {
            "tags": tag_counts,
            "sources": source_counts,
            "total_articles": len(self.articles)
        } 