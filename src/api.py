from fastapi import APIRouter, Query
from typing import List, Optional
from .data_service import DataService
from .models import ArticleResponse, StatsResponse

# Initialize data service
data_service = DataService()

# Create router
router = APIRouter()


@router.get("/articles", response_model=List[ArticleResponse])
async def get_articles(
    source: Optional[str] = Query(None, description="Filter by source name"),
    tag: Optional[List[str]] = Query(None, description="Filter by tags (can specify multiple)"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get articles with optional filtering.
    
    - **source**: Filter by a single source (e.g., Daily Nation)
    - **tag**: Filter by articles containing at least one of the provided tags (can specify multiple)
    - **date_from**: Filter by start date in YYYY-MM-DD format
    - **date_to**: Filter by end date in YYYY-MM-DD format
    """
    return data_service.get_articles(
        source=source,
        tags=tag,
        date_from=date_from,
        date_to=date_to
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get statistics about articles, including counts per tag and per source.
    """
    stats = data_service.get_stats()
    return StatsResponse(
        tags=stats["tags"],
        sources=stats["sources"],
        total_articles=stats["total_articles"]
    ) 