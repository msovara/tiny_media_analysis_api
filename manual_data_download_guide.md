# Manual Data Download Guide

## Overview

This guide provides step-by-step instructions for manually downloading the required datasets for IOD-drought correlation analysis. Manual downloads are recommended because they require API credentials and account setups.

## Required Datasets

### 1. CHIRPS Precipitation Data

**Source**: Climate Hazards Group InfraRed Precipitation with Station data  
**Website**: https://www.chc.ucsb.edu/data/chirps  
**Format**: NetCDF or GeoTIFF  
**Spatial Resolution**: 0.05° (~5km)  
**Temporal Coverage**: 1981-present  

#### Download Instructions:
1. Go to: https://www.chc.ucsb.edu/data/chirps
2. Navigate to "CHIRPS-2.0 Global Monthly"
3. Download files for 1980-2020
4. File naming pattern: `chirps-v2.0.YYYY.MM.tif`
5. Save to: `data/chirps/`

#### Alternative: Use Python script
```python
# Create download script for CHIRPS
import requests
import os

def download_chirps():
    base_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs"
    
    for year in range(1980, 2021):
        for month in range(1, 13):
            filename = f"chirps-v2.0.{year}.{month:02d}.tif"
            url = f"{base_url}/{filename}"
            
            # Download file
            response = requests.get(url)
            if response.status_code == 200:
                with open(f"data/chirps/{filename}", 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
```

### 2. ERA5 Temperature Data

**Source**: ECMWF Reanalysis v5  
**Website**: https://cds.climate.copernicus.eu/  
**Format**: NetCDF  
**Spatial Resolution**: 0.25° (~25km)  
**Temporal Coverage**: 1940-present  

#### Setup Instructions:
1. **Register at CDS**: https://cds.climate.copernicus.eu/
2. **Get API key** from your profile
3. **Create `~/.cdsapirc` file**:
   ```
   url: https://cds.climate.copernicus.eu/api/v2
   key: YOUR_API_KEY
   ```
4. **Install cdsapi**: `pip install cdsapi`

#### Download Script:
```python
import cdsapi

def download_era5_temperature():
    c = cdsapi.Client()
    
    # Southern Africa bounds
    area = [10, -35, 40, -10]  # North, West, South, East
    
    for year in range(1980, 2021):
        for month in range(1, 13):
            filename = f"era5_temperature_{year}{month:02d}.nc"
            
            c.retrieve(
                'reanalysis-era5-single-levels-monthly-means',
                {
                    'product_type': 'monthly_averaged_reanalysis',
                    'variable': '2m_temperature',
                    'year': str(year),
                    'month': f"{month:02d}",
                    'time': '00:00',
                    'area': area,
                    'format': 'netcdf',
                },
                f'data/era5/{filename}'
            )
            print(f"Downloaded {filename}")

# Run the download
download_era5_temperature()
```

### 3. MODIS NDVI Data

**Source**: Moderate Resolution Imaging Spectroradiometer  
**Website**: https://modis.gsfc.nasa.gov/data/  
**Format**: HDF/NetCDF  
**Spatial Resolution**: 250m, 500m, 1km  
**Temporal Coverage**: 2000-present  

#### Setup Instructions:
1. **Register at NASA Earthdata**: https://urs.earthdata.nasa.gov/
2. **Install modis-tools**: `pip install modis-tools`
3. **Set up authentication** for data download

#### Download Script:
```python
import os
import requests
from pathlib import Path

def download_modis_ndvi():
    # NASA Earthdata base URL
    base_url = "https://e4ftl01.cr.usgs.gov/MOLT/MOD13A3.061"
    
    # Southern Africa bounds
    bounds = {
        'lon_min': 10, 'lon_max': 40,
        'lat_min': -35, 'lat_max': -10
    }
    
    # Download years 2000-2020 (MODIS availability)
    for year in range(2000, 2021):
        for month in range(1, 13):
            # MODIS filename format
            filename = f"MOD13A3.A{year}{month:02d}01.h08v06.061.hdf"
            url = f"{base_url}/{year}.{month:02d}.01/{filename}"
            
            # Download logic here
            print(f"Would download: {filename}")
            # Add actual download implementation

# Run the download
download_modis_ndvi()
```

### 4. IOD Index Data

#### JAMSTEC IOD Index
**Source**: Japan Agency for Marine-Earth Science and Technology  
**Website**: http://www.jamstec.go.jp/frsgc/research/d1/iod/  
**Format**: TXT/CSV  
**Temporal Coverage**: 1958-present  

#### Download Instructions:
1. Go to: http://www.jamstec.go.jp/frsgc/research/d1/iod/DATA/dmi.monthly.txt
2. Save as: `data/iod/jamstec_iod_index.txt`

#### NOAA IOD Index
**Source**: National Oceanic and Atmospheric Administration  
**Website**: https://www.cpc.ncep.noaa.gov/data/indices/  
**Format**: TXT/CSV  
**Temporal Coverage**: 1870-present  

#### Download Instructions:
1. Go to: https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt
2. Save as: `data/iod/noaa_iod_index.txt`

#### BOM IOD Index
**Source**: Bureau of Meteorology, Australia  
**Website**: http://www.bom.gov.au/climate/enso/indices/  
**Format**: TXT/CSV  
**Temporal Coverage**: 1870-present  

#### Download Instructions:
1. Go to: http://www.bom.gov.au/climate/enso/indices/iod.txt
2. Save as: `data/iod/bom_iod_index.txt`

## Data Organization

After downloading, organize your data as follows:

```
data/
├── chirps/
│   ├── chirps-v2.0.1980.01.tif
│   ├── chirps-v2.0.1980.02.tif
│   └── ... (all monthly files)
├── era5/
│   ├── era5_temperature_198001.nc
│   ├── era5_temperature_198002.nc
│   └── ... (all monthly files)
├── modis/
│   ├── MOD13A3.A20000101.h08v06.061.hdf
│   ├── MOD13A3.A20000201.h08v06.061.hdf
│   └── ... (all monthly files)
├── iod/
│   ├── jamstec_iod_index.txt
│   ├── noaa_iod_index.txt
│   └── bom_iod_index.txt
└── processed/
    └── (processed data files)
```

## Data Quality Checklist

Before proceeding with analysis, verify:

- [ ] **CHIRPS**: 492 files (41 years × 12 months)
- [ ] **ERA5**: 492 files (41 years × 12 months)
- [ ] **MODIS**: 252 files (21 years × 12 months, 2000-2020)
- [ ] **IOD**: 3 files (one from each source)
- [ ] **File sizes**: Reasonable file sizes (not empty)
- [ ] **Spatial coverage**: Southern Africa region
- [ ] **Temporal coverage**: 1980-2020 (or 2000-2020 for MODIS)

## Alternative: Use Sample Data

If manual downloads are too complex, you can use the sample data feature:

```bash
python main_workflow.py
# Select option 3: "Run complete workflow with sample data"
```

This will create synthetic data that mimics the real data structure for testing the workflow.

## Next Steps

After downloading the data:

1. **Run the workflow**: `python main_workflow.py`
2. **Select option 2**: "Run complete workflow with real data"
3. **Specify data file paths** when prompted
4. **Check results** in the `output/` directory

## Troubleshooting

### Common Issues:
- **File not found**: Check file paths and naming
- **Permission denied**: Check file permissions
- **Empty files**: Re-download the files
- **Wrong format**: Convert files to NetCDF format

### Data Conversion:
If you have data in different formats, use these conversion tools:

```python
# Convert GeoTIFF to NetCDF
import rasterio
import xarray as xr

def convert_geotiff_to_netcdf(tiff_file, nc_file):
    with rasterio.open(tiff_file) as src:
        data = src.read(1)
        transform = src.transform
        crs = src.crs
        
        # Create xarray dataset
        ds = xr.Dataset(
            data_vars={'precipitation': (('lat', 'lon'), data)},
            coords={
                'lat': np.arange(data.shape[0]),
                'lon': np.arange(data.shape[1])
            }
        )
        
        ds.to_netcdf(nc_file)
```

## Support

For questions about data downloads:
1. Check the official data provider websites
2. Review the API documentation
3. Contact the data providers for support
4. Use sample data for testing the workflow


















