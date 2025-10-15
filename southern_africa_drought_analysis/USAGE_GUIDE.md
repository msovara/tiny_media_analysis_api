# Southern Africa Drought Analysis - Usage Guide

This guide shows you how to use the drought analysis toolkit to create Figure 2.1: Map of Southern Africa showing drought frequency/severity.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Main Analysis (Figure 2.1)

```bash
python figure_2_1_drought_analysis.py
```

This will create:
- Main drought frequency map
- Multi-scale comparison maps
- Drought severity analysis
- Interactive web map
- Summary statistics
- Time series analysis

### 3. Run Example Scripts

```bash
# Basic analysis examples
python examples/basic_analysis.py

# Advanced mapping examples
python examples/advanced_mapping.py
```

## Understanding the Output

### Main Figure 2.1
- **File**: `outputs/figure_2_1_main_drought_frequency.png`
- **Content**: Map showing drought frequency across Southern Africa
- **Method**: 12-month SPI with moderate drought threshold (-1.0)
- **Period**: 2000-2023 (sample data)

### Interactive Map
- **File**: `outputs/figure_2_1_interactive_map.html`
- **Content**: Interactive web map with multiple layers
- **Features**: Zoom, pan, layer control, hover information

### Additional Analysis
- **Multi-scale comparison**: Different time scales (3, 6, 12 months)
- **Severity analysis**: Different drought thresholds
- **Time series**: SPI evolution for key locations
- **Statistics**: Summary statistics and distributions

## Customizing the Analysis

### Using Your Own Data

1. **Replace sample data** in `figure_2_1_drought_analysis.py`:

```python
# Instead of create_sample_data(), load your data:
precip, temp = data_processor.prepare_drought_analysis_data(
    precip_file='path/to/your/precipitation.nc',
    temp_file='path/to/your/temperature.nc',
    start_date='2000-01-01',
    end_date='2023-12-31'
)
```

2. **Adjust analysis parameters**:

```python
# Different drought thresholds
thresholds = {
    'moderate': -1.0,    # Change these values
    'severe': -1.5,
    'extreme': -2.0
}

# Different time scales
scales = [1, 3, 6, 12, 24]  # Add more scales
```

### Modifying the Map

1. **Change map extent** in `visualization.py`:

```python
self.bounds = {
    'lon_min': -20, 'lon_max': 60,    # Adjust longitude range
    'lat_min': -40, 'lat_max': -10    # Adjust latitude range
}
```

2. **Customize colors**:

```python
# In DroughtVisualizer class
self.drought_colors = {
    'extremely_dry': '#8B0000',      # Your custom colors
    'severely_dry': '#DC143C',
    # ... etc
}
```

## Data Sources

### Supported Formats
- **NetCDF**: Climate data files (.nc)
- **CSV**: Station data with lat/lon/time columns
- **XArray**: Direct xarray DataArray objects

### Recommended Data Sources
- **CHIRPS**: Precipitation data for Africa
- **ERA5**: Reanalysis data (precipitation, temperature)
- **CRU**: Climate Research Unit datasets
- **Local stations**: Weather station data

### Data Requirements
- **Precipitation**: Monthly values in mm
- **Temperature**: Monthly values in °C (for SPEI)
- **Spatial coverage**: Southern Africa region
- **Temporal coverage**: At least 20 years for reliable statistics
- **Missing data**: Should be minimal (<10%)

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

## Troubleshooting

### Common Issues

1. **Import errors**:
   ```bash
   # Make sure you're in the project directory
   cd southern_africa_drought_analysis
   python figure_2_1_drought_analysis.py
   ```

2. **Missing dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Memory issues with large datasets**:
   - Use data chunking
   - Reduce spatial resolution
   - Process smaller time periods

4. **Cartopy installation issues**:
   ```bash
   # On Windows
   conda install -c conda-forge cartopy
   
   # On Linux/Mac
   pip install cartopy
   ```

### Performance Tips

1. **For large datasets**:
   - Use Dask for parallel processing
   - Process data in chunks
   - Reduce spatial resolution

2. **For faster visualization**:
   - Lower DPI for quick previews
   - Use fewer map features
   - Reduce color map resolution

## Advanced Usage

### Custom Analysis Functions

```python
from drought_indices import DroughtIndices
from visualization import DroughtVisualizer

# Create custom analysis
drought_calc = DroughtIndices()
visualizer = DroughtVisualizer()

# Your custom code here
spi = drought_calc.calculate_spi(precip, scale=6)
freq = drought_calc.calculate_drought_frequency(spi, threshold=-1.2)

# Create custom visualization
fig = visualizer.create_drought_frequency_map(freq, title="My Custom Map")
```

### Batch Processing

```python
# Process multiple regions
regions = ['south_africa', 'namibia', 'botswana']
for region in regions:
    # Load region-specific data
    precip, temp = load_region_data(region)
    
    # Run analysis
    spi = drought_calc.calculate_spi(precip, scale=12)
    freq = drought_calc.calculate_drought_frequency(spi)
    
    # Save results
    visualizer.create_drought_frequency_map(freq, 
        save_path=f'outputs/{region}_drought_map.png')
```

## Support

For questions or issues:
1. Check the example scripts in `examples/`
2. Review the code documentation
3. Check the troubleshooting section above

## Citation

If you use this toolkit in your research, please cite:

```
Southern Africa Drought Analysis Toolkit
[Your Name/Institution]
[Year]
```







