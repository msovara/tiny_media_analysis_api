# Southern Africa Drought Analysis

A comprehensive Python toolkit for analyzing drought frequency and severity across Southern Africa using historical drought index data (SPI, SPEI).

## Features

- **Drought Index Calculations**: Standardized Precipitation Index (SPI) and Standardized Precipitation Evapotranspiration Index (SPEI)
- **Geospatial Analysis**: Process and analyze climate data across Southern Africa
- **Interactive Mapping**: Create drought frequency/severity maps with multiple visualization options
- **Data Processing**: Handle NetCDF, CSV, and other climate data formats
- **Web API**: RESTful API for accessing drought analysis results
- **Export Options**: Generate maps in various formats (PNG, PDF, HTML)

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from drought_analysis import DroughtAnalyzer
import matplotlib.pyplot as plt

# Initialize analyzer
analyzer = DroughtAnalyzer()

# Load precipitation data (example)
precip_data = analyzer.load_precipitation_data('data/precipitation.nc')

# Calculate SPI for 3-month periods
spi_3m = analyzer.calculate_spi(precip_data, scale=3)

# Create drought frequency map
drought_map = analyzer.create_drought_frequency_map(spi_3m, threshold=-1.0)

# Save map
drought_map.save('drought_frequency_map.html')
```

### Using the Web API

```bash
# Start the API server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Access the interactive dashboard
# Open http://localhost:8000 in your browser
```

## Project Structure

```
southern_africa_drought_analysis/
├── drought_analysis/          # Core analysis modules
│   ├── __init__.py
│   ├── drought_indices.py     # SPI/SPEI calculations
│   ├── data_processing.py     # Data loading and preprocessing
│   ├── visualization.py       # Mapping and plotting functions
│   └── utils.py              # Utility functions
├── api/                      # Web API
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── routes.py            # API endpoints
├── data/                    # Sample data and outputs
│   ├── sample/             # Sample climate data
│   └── outputs/            # Generated maps and results
├── examples/               # Example scripts
│   ├── basic_analysis.py
│   ├── advanced_mapping.py
│   └── api_usage.py
├── tests/                  # Test suite
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Data Sources

This toolkit can work with various climate data sources:

- **CHIRPS**: Climate Hazards Group InfraRed Precipitation with Station data
- **ERA5**: ECMWF Reanalysis v5
- **CRU**: Climate Research Unit datasets
- **Local station data**: CSV files with precipitation/temperature data

## Drought Index Definitions

### Standardized Precipitation Index (SPI)
- **SPI < -2.0**: Extremely dry
- **-2.0 ≤ SPI < -1.5**: Severely dry
- **-1.5 ≤ SPI < -1.0**: Moderately dry
- **-1.0 ≤ SPI < 0**: Mildly dry
- **0 ≤ SPI < 1.0**: Near normal
- **1.0 ≤ SPI < 1.5**: Moderately wet
- **1.5 ≤ SPI < 2.0**: Severely wet
- **SPI ≥ 2.0**: Extremely wet

### Standardized Precipitation Evapotranspiration Index (SPEI)
Similar classification as SPI but accounts for evapotranspiration effects.

## Examples

See the `examples/` directory for detailed usage examples:

- `basic_analysis.py`: Simple SPI calculation and mapping
- `advanced_mapping.py`: Complex multi-scale drought analysis
- `api_usage.py`: Using the web API programmatically

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this toolkit in your research, please cite:

```
Southern Africa Drought Analysis Toolkit
[Your Name/Institution]
[Year]
```

## Support

For questions or support, please open an issue on the project repository.







