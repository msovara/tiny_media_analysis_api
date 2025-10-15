# IOD-Drought Correlation Analysis Workflow Documentation

## Overview

This comprehensive workflow automates the complete process of analyzing correlations between the Indian Ocean Dipole (IOD) and drought indices across Southern Africa. The workflow includes data download, processing, calculation of drought indices, and correlation analysis.

## Workflow Components

### 1. Data Download Workflow (`data_download_workflow.py`)

**Purpose**: Downloads and processes all required datasets for the analysis.

**Key Features**:
- Downloads CHIRPS precipitation data
- Downloads ERA5 temperature data (requires CDS API setup)
- Downloads MODIS NDVI data (requires NASA Earthdata login)
- Downloads IOD index data from multiple sources (JAMSTEC, NOAA, BOM)
- Creates sample data for testing when real data is unavailable

**Usage**:
```bash
python data_download_workflow.py
```

**Output**:
- Raw data files in `data/` directory
- Processed data files in `data/processed/` directory
- Sample data for testing

### 2. Drought Indices Calculation (`drought_indices_calculation.py`)

**Purpose**: Calculates drought indices (SPI, SPEI, NDVI) from climate data.

**Key Features**:
- Calculates SPI (Standardized Precipitation Index) for multiple time scales (1, 3, 6, 12 months)
- Calculates SPEI (Standardized Precipitation Evapotranspiration Index) using Thornthwaite method
- Calculates NDVI anomalies for vegetation drought monitoring
- Creates drought index maps and visualizations

**Usage**:
```bash
python drought_indices_calculation.py
```

**Output**:
- SPI files: `output/spi/`
- SPEI files: `output/spei/`
- NDVI files: `output/ndvi/`
- Maps: `output/maps/`

### 3. IOD Data Processing (`iod_data_processing.py`)

**Purpose**: Processes IOD data from multiple sources and prepares it for correlation analysis.

**Key Features**:
- Downloads IOD data from JAMSTEC, NOAA, and BOM
- Processes and standardizes data formats
- Creates combined IOD dataset from multiple sources
- Analyzes IOD statistics and identifies events
- Creates IOD analysis plots

**Usage**:
```bash
python iod_data_processing.py
```

**Output**:
- Raw IOD data: `data/iod/`
- Processed IOD data: `output/processed/`
- IOD analysis plots: `output/plots/`

### 4. Main Workflow (`main_workflow.py`)

**Purpose**: Orchestrates the complete analysis workflow.

**Key Features**:
- Runs all workflow components in sequence
- Manages data flow between components
- Creates final visualizations and reports
- Provides status tracking and error handling

**Usage**:
```bash
python main_workflow.py
```

**Output**:
- Complete analysis results in `output/` directory
- Analysis report: `output/analysis_report.txt`
- Summary visualizations and correlation maps

## Installation and Setup

### 1. Install Dependencies

```bash
# Install required Python packages
pip install -r requirements_iod_analysis.txt

# Additional packages for specific data sources
pip install cdsapi  # For ERA5 data
pip install modis-tools  # For MODIS data
```

### 2. Set Up Data Access Credentials

#### For ERA5 Data (CDS API):
1. Register at: https://cds.climate.copernicus.eu/
2. Get your API key
3. Create `~/.cdsapirc` file:
```
url: https://cds.climate.copernicus.eu/api/v2
key: YOUR_API_KEY
```

#### For MODIS Data (NASA Earthdata):
1. Register at: https://urs.earthdata.nasa.gov/
2. Set up authentication for data download

### 3. Directory Structure

```
project/
├── data_download_workflow.py
├── drought_indices_calculation.py
├── iod_data_processing.py
├── main_workflow.py
├── requirements_iod_analysis.txt
├── WORKFLOW_DOCUMENTATION.md
├── data/
│   ├── chirps/
│   ├── era5/
│   ├── modis/
│   ├── iod/
│   └── processed/
└── output/
    ├── spi/
    ├── spei/
    ├── ndvi/
    ├── maps/
    ├── plots/
    └── processed/
```

## Usage Instructions

### Quick Start (Sample Data)

1. **Run the main workflow with sample data**:
```bash
python main_workflow.py
# Select option 3: "Run complete workflow with sample data"
```

2. **Check results**:
- Results will be saved in the `output/` directory
- Review the analysis report: `output/analysis_report.txt`

### Full Analysis (Real Data)

1. **Set up data access credentials** (see Installation section)

2. **Download data**:
```bash
python data_download_workflow.py
# Select "n" when asked about sample data
```

3. **Run complete workflow**:
```bash
python main_workflow.py
# Select option 2: "Run complete workflow with real data"
```

### Individual Components

You can also run individual workflow components:

```bash
# Download data only
python data_download_workflow.py

# Calculate drought indices only
python drought_indices_calculation.py

# Process IOD data only
python iod_data_processing.py
```

## Data Requirements

### Required Datasets

1. **Precipitation Data**:
   - Source: CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data)
   - Format: NetCDF or GeoTIFF
   - Spatial Resolution: 0.05° (~5km)
   - Temporal Coverage: 1981-present

2. **Temperature Data**:
   - Source: ERA5 (ECMWF Reanalysis v5)
   - Format: NetCDF
   - Spatial Resolution: 0.25° (~25km)
   - Temporal Coverage: 1940-present

3. **NDVI Data**:
   - Source: MODIS (Moderate Resolution Imaging Spectroradiometer)
   - Format: HDF/NetCDF
   - Spatial Resolution: 250m, 500m, 1km
   - Temporal Coverage: 2000-present

4. **IOD Data**:
   - Sources: JAMSTEC, NOAA, BOM
   - Format: CSV/TXT
   - Temporal Coverage: 1958-present

### Data Specifications

- **Spatial Coverage**: Southern Africa (10°E-40°E, 35°S-10°S)
- **Temporal Coverage**: 1980-2020 (40 years minimum)
- **Data Frequency**: Monthly values
- **Missing Data**: <10% for reliable statistics
- **Coordinate System**: WGS84 (EPSG:4326)

## Output Files

### Drought Indices
- `output/spi/spi_1month.nc` - 1-month SPI
- `output/spi/spi_3month.nc` - 3-month SPI
- `output/spi/spi_6month.nc` - 6-month SPI
- `output/spi/spi_12month.nc` - 12-month SPI
- `output/spei/spei_1month.nc` - 1-month SPEI
- `output/spei/spei_3month.nc` - 3-month SPEI
- `output/spei/spei_6month.nc` - 6-month SPEI
- `output/spei/spei_12month.nc` - 12-month SPEI
- `output/ndvi/ndvi_anomalies.nc` - NDVI anomalies

### IOD Data
- `output/processed/combined_iod_data.csv` - Combined IOD dataset
- `output/plots/iod_analysis.png` - IOD analysis plots

### Maps and Visualizations
- `output/maps/spi_1month_map.png` - SPI-1 maps
- `output/maps/spi_3month_map.png` - SPI-3 maps
- `output/maps/spi_6month_map.png` - SPI-6 maps
- `output/maps/spi_12month_map.png` - SPI-12 maps
- `output/maps/spei_1month_map.png` - SPEI-1 maps
- `output/maps/spei_3month_map.png` - SPEI-3 maps
- `output/maps/spei_6month_map.png` - SPEI-6 maps
- `output/maps/spei_12month_map.png` - SPEI-12 maps
- `output/maps/ndvi_anomalies_map.png` - NDVI anomaly maps

### Reports
- `output/analysis_report.txt` - Complete analysis report
- `output/correlation_results.csv` - Correlation analysis results

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Make sure you're in the project directory
   cd /path/to/project
   python main_workflow.py
   ```

2. **Missing Dependencies**:
   ```bash
   pip install -r requirements_iod_analysis.txt
   ```

3. **Data Access Issues**:
   - Check API credentials for ERA5 and MODIS
   - Verify internet connection for data downloads
   - Use sample data for testing

4. **Memory Issues**:
   - Reduce spatial resolution for large datasets
   - Process data in smaller time chunks
   - Use sample data for testing

5. **File Permission Issues**:
   ```bash
   chmod +x *.py
   ```

### Error Messages

- **"No data downloaded"**: Check internet connection and API credentials
- **"File not found"**: Verify file paths and data availability
- **"Memory error"**: Reduce dataset size or use sample data
- **"Import error"**: Install missing dependencies

## Advanced Usage

### Customizing the Analysis

1. **Change Study Period**:
   ```python
   # In main_workflow.py
   self.start_year = 1990
   self.end_year = 2020
   ```

2. **Modify Spatial Coverage**:
   ```python
   # In data_download_workflow.py
   self.southern_africa_bounds = {
       'lon_min': 15, 'lon_max': 35,
       'lat_min': -30, 'lat_max': -15
   }
   ```

3. **Add Custom Drought Indices**:
   ```python
   # In drought_indices_calculation.py
   # Add new calculation methods
   ```

### Batch Processing

For processing multiple regions or time periods:

```python
# Example batch processing script
regions = [
    {'name': 'southeastern', 'bounds': {...}},
    {'name': 'central', 'bounds': {...}},
    {'name': 'northwestern', 'bounds': {...}}
]

for region in regions:
    # Process each region
    workflow = MainWorkflow()
    workflow.run_complete_workflow()
```

## Contributing

To contribute to this workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample data
5. Submit a pull request

## License

This workflow is provided under the MIT License. See LICENSE file for details.

## Support

For questions and support:

1. Check the troubleshooting section
2. Review the error messages
3. Use sample data for testing
4. Contact the development team

## Changelog

### Version 1.0 (June 2025)
- Initial release
- Complete workflow implementation
- Sample data support
- Documentation and examples

---

**Author**: Mthetho Sovara  
**Date**: June 2025  
**Version**: 1.0


















