from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class Article(BaseModel):
    """Article model representing a news article."""
    id: int
    title: str
    body: str
    source: str
    date: str
    url: Optional[str] = ""
    tags: Optional[List[str]] = []


class ArticleResponse(BaseModel):
    """Response model for articles with tags."""
    id: int
    title: str
    body: str
    source: str
    date: str
    url: Optional[str] = ""
    tags: List[str]


class StatsResponse(BaseModel):
    """Response model for statistics."""
    tags: dict[str, int]
    sources: dict[str, int]
    total_articles: int 