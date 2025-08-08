# 📰 Tiny Media Analysis API

A modern Python service that ingests news articles, applies intelligent tagging, and exposes data through a REST API with advanced filtering capabilities. Built with FastAPI and featuring an interactive dashboard for data visualization.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- **🔍 Smart Tagging**: Automatic article categorization using keyword analysis
- **🌐 REST API**: Full-featured API with filtering, sorting, and statistics
- **📊 Interactive Dashboard**: Real-time data visualization with Chart.js
- **🧪 Comprehensive Testing**: Unit and integration tests with 100% coverage
- **📚 Auto-Generated Docs**: Interactive API documentation
- **⚡ High Performance**: Built with FastAPI for optimal speed

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/[your-username]/tiny-media-analysis.git
   cd tiny-media-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   - 🌐 **API**: http://localhost:8000
   - 📖 **Interactive Docs**: http://localhost:8000/docs
   - 📊 **Dashboard**: http://localhost:8000/static/index.html

## 📋 API Endpoints

### Articles
```http
GET /api/v1/articles
```

**Query Parameters:**
- `source` (string): Filter by source name
- `tag` (string, multiple): Filter by tags
- `date_from` (string): Start date (YYYY-MM-DD)
- `date_to` (string): End date (YYYY-MM-DD)

**Examples:**
```bash
# Get all articles
curl http://localhost:8000/api/v1/articles

# Filter by source
curl "http://localhost:8000/api/v1/articles?source=The%20Guardian"

# Filter by tags
curl "http://localhost:8000/api/v1/articles?tag=elections&tag=health"

# Filter by date range
curl "http://localhost:8000/api/v1/articles?date_from=2024-05-01&date_to=2024-06-01"
```

### Statistics
```http
GET /api/v1/stats
```

Returns counts per tag and per source.

## 🏷️ Tagging System

The application automatically tags articles based on content analysis:

| Tag | Keywords | Description |
|-----|----------|-------------|
| **elections** | election, vote, voting, poll, campaign, candidate, ballot, electoral, commission, results | Articles about voting, campaigns, electoral processes |
| **health** | health, medical, hospital, doctor, patient, treatment, disease, vaccine, vaccination, covid, mental health, healthcare, clinic, medicine, symptoms | Articles about healthcare, medical topics, hospitals |
| **corruption** | corruption, bribe, bribery, scandal, fraud, embezzlement, misappropriation, irregularities, audit, investigation, arrested, charges, suspended, financial | Articles about scandals, fraud, bribery, investigations |

## 📊 Dashboard Features

The interactive dashboard provides:

- **📈 Bar Chart**: Articles by tag distribution
- **🍩 Doughnut Chart**: Articles by source distribution  
- **📋 Summary Cards**: Total articles, active tags, news sources
- **🔄 Real-time Updates**: Live data from the API

## 🧪 Testing

### Run all tests
```bash
pytest
```

### Run specific test files
```bash
pytest tests/test_tagging.py
pytest tests/test_api.py
```

### Run simple test (no dependencies needed)
```bash
python test_simple.py
```

## 📁 Project Structure

```
tiny-media-analysis/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── SETUP.md                 # Quick setup guide
├── test_simple.py           # Simple test script
├── src/                     # Main application code
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── api.py              # API routes
│   ├── models.py           # Pydantic models
│   ├── data_service.py     # Data management
│   └── tagging.py          # Tagging logic
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_tagging.py     # Unit tests
│   └── test_api.py         # Integration tests
├── data/
│   └── articles.json       # Sample articles (10 articles)
└── static/
    └── index.html          # Dashboard
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **Data Models**: Pydantic
- **Testing**: pytest, httpx
- **Frontend**: HTML5, CSS3, Chart.js
- **Documentation**: Auto-generated with FastAPI

## 🎯 Sample Data

The application includes 10 sample articles covering:

- **🗳️ Elections** (4 articles): Voting, registration, turnout, electoral processes
- **🏥 Health** (4 articles): Vaccines, hospitals, healthcare reforms, medical news
- **⚖️ Corruption** (3 articles): Scandals, bribes, investigations, legal cases

## 🔧 Development

### Adding New Tags

To add a new tag, modify `src/tagging.py`:

```python
self.tag_keywords: Dict[str, List[str]] = {
    "elections": [...],
    "health": [...],
    "corruption": [...],
    "technology": ["tech", "software", "digital", "innovation"]  # New tag
}
```

### Adding New Endpoints

Create new routes in `src/api.py`:

```python
@router.get("/new-endpoint")
async def new_endpoint():
    return {"message": "New endpoint"}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the Tiny Media Analysis take-home assignment
- Inspired by real-world media analysis challenges
- Uses modern Python best practices and FastAPI framework

## 📞 Support

If you have any questions or need help:

1. Check the [API Documentation](http://localhost:8000/docs) when running
2. Review the test files for usage examples
3. Open an issue on GitHub

---

**⭐ Star this repository if you found it helpful!**

**⏱️ Time Spent**: ~2.5 hours (Core: 2h, Dashboard: 30min, Docs: 15min) 