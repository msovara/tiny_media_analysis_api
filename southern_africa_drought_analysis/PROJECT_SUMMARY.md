# Southern Africa Drought Analysis - Project Summary

## What We've Built

A comprehensive Python toolkit for analyzing drought frequency and severity across Southern Africa using historical drought index data (SPI, SPEI). This toolkit creates **Figure 2.1: Map of Southern Africa showing drought frequency/severity** as requested.

## Project Structure

```
southern_africa_drought_analysis/
├── drought_indices.py              # Core drought calculation functions
├── data_processing.py              # Data loading and preprocessing
├── visualization.py                # Mapping and visualization functions
├── figure_2_1_drought_analysis.py  # Main analysis script for Figure 2.1
├── test_installation.py            # Installation and functionality test
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── USAGE_GUIDE.md                  # Detailed usage instructions
├── PROJECT_SUMMARY.md              # This file
└── examples/                       # Example scripts
    ├── basic_analysis.py           # Basic usage examples
    └── advanced_mapping.py         # Advanced visualization examples
```

## Key Features

### 1. Drought Index Calculations
- **Standardized Precipitation Index (SPI)**: Multiple time scales (1, 3, 6, 12 months)
- **Standardized Precipitation Evapotranspiration Index (SPEI)**: Accounts for temperature effects
- **Drought Classification**: Automatic classification based on standard thresholds
- **Statistical Analysis**: Frequency, severity, and duration calculations

### 2. Data Processing
- **Multiple Data Formats**: NetCDF, CSV, XArray support
- **Data Quality Control**: Missing data handling, outlier detection
- **Spatial Processing**: Southern Africa region cropping
- **Temporal Processing**: Monthly resampling, time series analysis

### 3. Visualization & Mapping
- **Static Maps**: High-resolution drought frequency/severity maps
- **Interactive Maps**: Web-based maps with multiple layers
- **Multi-scale Analysis**: Comparison across different time scales
- **Time Series Plots**: SPI evolution for specific locations
- **Statistical Plots**: Distribution analysis and summary statistics

### 4. Main Analysis (Figure 2.1)
- **Comprehensive Analysis**: Multi-scale drought frequency mapping
- **Multiple Thresholds**: Moderate, severe, and extreme drought analysis
- **Interactive Output**: Web-based interactive map
- **Summary Statistics**: Detailed statistical analysis
- **Time Series Analysis**: Key location analysis

## How to Use

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test installation
python test_installation.py

# 3. Run main analysis (Figure 2.1)
python figure_2_1_drought_analysis.py

# 4. View results
# - Static maps: outputs/figure_2_1_main_drought_frequency.png
# - Interactive map: outputs/figure_2_1_interactive_map.html
```

### Example Usage
```python
from drought_indices import DroughtIndices, create_sample_data
from visualization import DroughtVisualizer

# Create sample data
precip, temp = create_sample_data()

# Calculate drought indices
drought_calc = DroughtIndices()
spi_12m = drought_calc.calculate_spi(precip, scale=12)

# Calculate drought frequency
drought_freq = drought_calc.calculate_drought_frequency(spi_12m, threshold=-1.0)

# Create map
visualizer = DroughtVisualizer()
fig = visualizer.create_drought_frequency_map(drought_freq, 
    title="Southern Africa Drought Frequency")
```

## Output Files

When you run the main analysis, you'll get:

### Main Figure 2.1
- `figure_2_1_main_drought_frequency.png` - Main drought frequency map
- `figure_2_1_interactive_map.html` - Interactive web map

### Additional Analysis
- `figure_2_1_multi_scale_comparison.png` - Multi-scale comparison
- `figure_2_1_severity_analysis.png` - Severity level analysis
- `figure_2_1_time_series_analysis.png` - Time series for key locations
- `figure_2_1_summary_statistics.png` - Statistical summary
- `figure_2_1_summary_statistics.csv` - Raw statistics data

## Technical Details

### Dependencies
- **Core**: numpy, pandas, scipy, matplotlib
- **Geospatial**: xarray, netcdf4, rasterio, geopandas, cartopy
- **Visualization**: folium, plotly, seaborn
- **Climate**: cftime, dask

### Data Requirements
- **Precipitation**: Monthly values in mm
- **Temperature**: Monthly values in °C (for SPEI)
- **Spatial Coverage**: Southern Africa (-20° to 60°E, -40° to -10°N)
- **Temporal Coverage**: Minimum 20 years for reliable statistics

### Drought Thresholds
- **Moderate Drought**: SPI < -1.0
- **Severe Drought**: SPI < -1.5
- **Extreme Drought**: SPI < -2.0

## Customization Options

### Using Your Own Data
```python
from data_processing import ClimateDataProcessor

processor = ClimateDataProcessor()
precip, temp = processor.prepare_drought_analysis_data(
    precip_file='path/to/your/data.nc',
    temp_file='path/to/your/temp.nc'
)
```

### Custom Analysis Parameters
```python
# Different thresholds
thresholds = {'moderate': -1.0, 'severe': -1.5, 'extreme': -2.0}

# Different time scales
scales = [1, 3, 6, 12, 24]  # months

# Custom map extent
bounds = {'lon_min': -20, 'lon_max': 60, 'lat_min': -40, 'lat_max': -10}
```

## Research Applications

This toolkit can be used for:

1. **Climate Research**: Drought pattern analysis, climate change impacts
2. **Agricultural Planning**: Drought risk assessment, crop planning
3. **Water Resource Management**: Drought monitoring, water allocation
4. **Policy Making**: Drought policy development, early warning systems
5. **Academic Research**: Thesis work, research publications

## Future Enhancements

Potential improvements:
- Real-time data integration
- Machine learning drought prediction
- Additional drought indices (PDSI, CMI)
- Climate change projections
- Web-based dashboard
- API for data access

## Support

- **Documentation**: README.md, USAGE_GUIDE.md
- **Examples**: examples/ directory
- **Testing**: test_installation.py
- **Troubleshooting**: See USAGE_GUIDE.md

## Citation

If you use this toolkit in your research:

```
Southern Africa Drought Analysis Toolkit
[Your Name/Institution]
[Year]
```

---

**Project Status**: ✅ Complete and Ready to Use

**Main Output**: Figure 2.1 - Southern Africa Drought Frequency/Severity Map

**Next Step**: Run `python figure_2_1_drought_analysis.py` to generate your maps!







