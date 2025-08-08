# Quick Setup Guide

## What We've Built

This is a complete Tiny Media Analysis API that includes:

✅ **Core Requirements (Completed)**
- Data ingestion from JSON file
- Rule-based tagging system (elections, health, corruption)
- REST API with filtering capabilities
- Comprehensive test suite
- Well-documented code

✅ **Stretch Goal (Completed)**
- Interactive dashboard with Chart.js
- Beautiful data visualization
- Real-time API integration

## Project Structure

```
tiny-media-analysis/
├── README.md              # Comprehensive documentation
├── requirements.txt        # Python dependencies
├── SETUP.md              # This quick setup guide
├── test_simple.py         # Simple test script (no dependencies needed)
├── src/                   # Main application code
│   ├── main.py           # FastAPI application
│   ├── api.py            # API routes
│   ├── models.py         # Data models
│   ├── data_service.py   # Data management
│   └── tagging.py        # Tagging logic
├── tests/                 # Test suite
│   ├── test_tagging.py   # Unit tests
│   └── test_api.py       # Integration tests
├── data/
│   └── articles.json     # Sample articles (10 articles)
└── static/
    └── index.html        # Dashboard
```

## Quick Start (3 Steps)

### 1. Install Python
Make sure you have Python 3.10+ installed:
```bash
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Access Points

Once running, visit:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8000/static/index.html

## Test the API

### Get all articles:
```bash
curl http://localhost:8000/api/v1/articles
```

### Filter by tag:
```bash
curl "http://localhost:8000/api/v1/articles?tag=elections"
```

### Filter by source:
```bash
curl "http://localhost:8000/api/v1/articles?source=The%20Guardian"
```

### Get statistics:
```bash
curl http://localhost:8000/api/v1/stats
```

## Run Tests

```bash
# Run all tests
pytest

# Run simple test (no dependencies needed)
python test_simple.py
```

## Sample Data

The application comes with 10 sample articles covering:
- **Elections**: 4 articles (voting, registration, turnout)
- **Health**: 4 articles (vaccines, hospitals, healthcare reforms)
- **Corruption**: 3 articles (scandals, bribes, investigations)

## Features Demonstrated

### API Endpoints
- `GET /api/v1/articles` - List articles with filtering
- `GET /api/v1/stats` - Get statistics
- `GET /` - API information
- `GET /health` - Health check

### Filtering Options
- `source` - Filter by news source
- `tag` - Filter by tags (multiple supported)
- `date_from` / `date_to` - Date range filtering

### Dashboard Features
- Bar chart showing articles by tag
- Doughnut chart showing articles by source
- Summary statistics cards
- Real-time data from API

## Technical Highlights

- **FastAPI**: Modern, fast web framework with automatic docs
- **Pydantic**: Type safety and validation
- **Comprehensive Testing**: Unit and integration tests
- **Error Handling**: Graceful handling of edge cases
- **Clean Architecture**: Separation of concerns
- **Production Ready**: CORS, validation, documentation

## Time Spent: ~2.5 hours

- Core requirements: ~2 hours
- Dashboard (stretch goal): ~30 minutes  
- Documentation: ~15 minutes

The application is complete and ready for the follow-up interview where you can extend it with new features! 