"""
IOD-Drought Analysis Data Download Workflow

This script automates the download of all required datasets for IOD-drought
correlation analysis in Southern Africa.

Required datasets:
1. CHIRPS precipitation data
2. ERA5 temperature data  
3. MODIS NDVI data
4. IOD index data (JAMSTEC/NOAA/BOM)

Author: Mthetho Sovara
Date: June 2025
"""

import os
import sys
import requests
import pandas as pd
import xarray as xr
import numpy as np
from pathlib import Path
import time
import warnings
from datetime import datetime, timedelta
import urllib.parse
import json

warnings.filterwarnings('ignore')

class DataDownloader:
    """Main class for downloading climate and IOD data"""
    
    def __init__(self, data_dir='data', output_dir='output'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.data_dir / 'chirps').mkdir(exist_ok=True)
        (self.data_dir / 'era5').mkdir(exist_ok=True)
        (self.data_dir / 'modis').mkdir(exist_ok=True)
        (self.data_dir / 'iod').mkdir(exist_ok=True)
        (self.data_dir / 'processed').mkdir(exist_ok=True)
        
        # Southern Africa bounds
        self.southern_africa_bounds = {
            'lon_min': 10, 'lon_max': 40,
            'lat_min': -35, 'lat_max': -10
        }
        
        # Study period
        self.start_year = 1980
        self.end_year = 2020
        
    def download_chirps_data(self):
        """
        Download CHIRPS precipitation data for Southern Africa
        """
        print("=" * 60)
        print("DOWNLOADING CHIRPS PRECIPITATION DATA")
        print("=" * 60)
        
        chirps_dir = self.data_dir / 'chirps'
        
        # CHIRPS base URL
        base_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/tifs"
        
        downloaded_files = []
        failed_downloads = []
        
        for year in range(self.start_year, self.end_year + 1):
            for month in range(1, 13):
                # CHIRPS filename format: chirps-v2.0.YYYY.MM.tif
                filename = f"chirps-v2.0.{year}.{month:02d}.tif"
                url = f"{base_url}/{filename}"
                local_path = chirps_dir / filename
                
                if local_path.exists():
                    print(f"✓ {filename} already exists")
                    downloaded_files.append(str(local_path))
                    continue
                
                try:
                    print(f"Downloading {filename}...")
                    response = requests.get(url, timeout=30)
                    
                    if response.status_code == 200:
                        with open(local_path, 'wb') as f:
                            f.write(response.content)
                        print(f"✓ Downloaded {filename}")
                        downloaded_files.append(str(local_path))
                    else:
                        print(f"✗ Failed to download {filename} (Status: {response.status_code})")
                        failed_downloads.append(filename)
                        
                except Exception as e:
                    print(f"✗ Error downloading {filename}: {e}")
                    failed_downloads.append(filename)
                
                # Rate limiting
                time.sleep(1)
        
        print(f"\nCHIRPS Download Summary:")
        print(f"✓ Successfully downloaded: {len(downloaded_files)} files")
        print(f"✗ Failed downloads: {len(failed_downloads)} files")
        
        if failed_downloads:
            print(f"Failed files: {failed_downloads}")
        
        return downloaded_files
    
    def download_era5_data(self):
        """
        Download ERA5 temperature data for Southern Africa
        Note: This requires CDS API access - see setup instructions
        """
        print("=" * 60)
        print("DOWNLOADING ERA5 TEMPERATURE DATA")
        print("=" * 60)
        
        print("⚠️  ERA5 download requires CDS API setup")
        print("Please follow these steps:")
        print("1. Register at: https://cds.climate.copernicus.eu/")
        print("2. Get your API key")
        print("3. Install cdsapi: pip install cdsapi")
        print("4. Set up ~/.cdsapirc file with your credentials")
        
        # Create sample ERA5 download script
        era5_script = self.data_dir / 'download_era5.py'
        
        era5_script_content = '''
import cdsapi
import xarray as xr
from pathlib import Path

def download_era5_temperature():
    """Download ERA5 2m temperature data for Southern Africa"""
    
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

if __name__ == "__main__":
    download_era5_temperature()
'''
        
        with open(era5_script, 'w') as f:
            f.write(era5_script_content)
        
        print(f"✓ Created ERA5 download script: {era5_script}")
        print("Run this script after setting up CDS API credentials")
        
        return str(era5_script)
    
    def download_modis_ndvi(self):
        """
        Download MODIS NDVI data for Southern Africa
        Note: This requires NASA Earthdata login
        """
        print("=" * 60)
        print("DOWNLOADING MODIS NDVI DATA")
        print("=" * 60)
        
        print("⚠️  MODIS download requires NASA Earthdata login")
        print("Please follow these steps:")
        print("1. Register at: https://urs.earthdata.nasa.gov/")
        print("2. Install modis-tools: pip install modis-tools")
        print("3. Set up authentication")
        
        # Create sample MODIS download script
        modis_script = self.data_dir / 'download_modis.py'
        
        modis_script_content = '''
import os
import requests
from pathlib import Path
import numpy as np
import xarray as xr

def download_modis_ndvi():
    """Download MODIS NDVI data for Southern Africa"""
    
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

if __name__ == "__main__":
    download_modis_ndvi()
'''
        
        with open(modis_script, 'w') as f:
            f.write(modis_script_content)
        
        print(f"✓ Created MODIS download script: {modis_script}")
        print("Run this script after setting up NASA Earthdata authentication")
        
        return str(modis_script)
    
    def download_iod_data(self):
        """
        Download IOD index data from multiple sources
        """
        print("=" * 60)
        print("DOWNLOADING IOD INDEX DATA")
        print("=" * 60)
        
        iod_dir = self.data_dir / 'iod'
        downloaded_files = []
        
        # JAMSTEC IOD Index
        try:
            print("Downloading JAMSTEC IOD index...")
            jamstec_url = "http://www.jamstec.go.jp/frsgc/research/d1/iod/DATA/dmi.monthly.txt"
            
            response = requests.get(jamstec_url, timeout=30)
            if response.status_code == 200:
                jamstec_file = iod_dir / 'jamstec_iod_index.txt'
                with open(jamstec_file, 'w') as f:
                    f.write(response.text)
                print(f"✓ Downloaded JAMSTEC IOD data: {jamstec_file}")
                downloaded_files.append(str(jamstec_file))
            else:
                print(f"✗ Failed to download JAMSTEC data (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ Error downloading JAMSTEC data: {e}")
        
        # NOAA IOD Index
        try:
            print("Downloading NOAA IOD index...")
            noaa_url = "https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt"
            
            response = requests.get(noaa_url, timeout=30)
            if response.status_code == 200:
                noaa_file = iod_dir / 'noaa_iod_index.txt'
                with open(noaa_file, 'w') as f:
                    f.write(response.text)
                print(f"✓ Downloaded NOAA IOD data: {noaa_file}")
                downloaded_files.append(str(noaa_file))
            else:
                print(f"✗ Failed to download NOAA data (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ Error downloading NOAA data: {e}")
        
        # BOM IOD Index
        try:
            print("Downloading BOM IOD index...")
            bom_url = "http://www.bom.gov.au/climate/enso/indices/iod.txt"
            
            response = requests.get(bom_url, timeout=30)
            if response.status_code == 200:
                bom_file = iod_dir / 'bom_iod_index.txt'
                with open(bom_file, 'w') as f:
                    f.write(response.text)
                print(f"✓ Downloaded BOM IOD data: {bom_file}")
                downloaded_files.append(str(bom_file))
            else:
                print(f"✗ Failed to download BOM data (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ Error downloading BOM data: {e}")
        
        print(f"\nIOD Download Summary:")
        print(f"✓ Successfully downloaded: {len(downloaded_files)} files")
        
        return downloaded_files
    
    def create_sample_data(self):
        """
        Create sample data for testing when real data is not available
        """
        print("=" * 60)
        print("CREATING SAMPLE DATA")
        print("=" * 60)
        
        # Create sample precipitation data
        print("Creating sample precipitation data...")
        precip_data = self._create_sample_precipitation()
        precip_file = self.data_dir / 'processed' / 'sample_precipitation.nc'
        precip_data.to_netcdf(precip_file)
        print(f"✓ Created sample precipitation: {precip_file}")
        
        # Create sample temperature data
        print("Creating sample temperature data...")
        temp_data = self._create_sample_temperature()
        temp_file = self.data_dir / 'processed' / 'sample_temperature.nc'
        temp_data.to_netcdf(temp_file)
        print(f"✓ Created sample temperature: {temp_file}")
        
        # Create sample IOD data
        print("Creating sample IOD data...")
        iod_data = self._create_sample_iod()
        iod_file = self.data_dir / 'processed' / 'sample_iod.csv'
        iod_data.to_csv(iod_file)
        print(f"✓ Created sample IOD data: {iod_file}")
        
        return {
            'precipitation': str(precip_file),
            'temperature': str(temp_file),
            'iod': str(iod_file)
        }
    
    def _create_sample_precipitation(self):
        """Create sample precipitation data"""
        # Create time series
        time = pd.date_range('1980-01-01', '2020-12-31', freq='MS')
        
        # Create spatial grid for Southern Africa
        lon = np.arange(10, 40.5, 0.5)
        lat = np.arange(-35, -9.5, 0.5)
        
        # Create random precipitation data with seasonal cycle
        np.random.seed(42)
        n_times = len(time)
        n_lats = len(lat)
        n_lons = len(lon)
        
        # Seasonal cycle
        seasonal = np.zeros((n_times, n_lats, n_lons))
        for i, t in enumerate(time):
            month = t.month
            if month in [12, 1, 2]:  # Summer
                seasonal[i] = np.random.uniform(50, 150, (n_lats, n_lons))
            elif month in [6, 7, 8]:  # Winter
                seasonal[i] = np.random.uniform(10, 50, (n_lats, n_lons))
            else:  # Transition seasons
                seasonal[i] = np.random.uniform(20, 80, (n_lats, n_lons))
        
        # Add some spatial patterns
        lon_grid, lat_grid = np.meshgrid(lon, lat)
        
        # Southeastern region (wetter)
        se_mask = (lon_grid >= 25) & (lon_grid <= 40) & (lat_grid >= -35) & (lat_grid <= -20)
        seasonal[:, se_mask] *= 1.5
        
        # Northwestern region (drier)
        nw_mask = (lon_grid >= 10) & (lon_grid <= 25) & (lat_grid >= -20) & (lat_grid <= -10)
        seasonal[:, nw_mask] *= 0.7
        
        # Create xarray dataset
        data = xr.Dataset(
            data_vars={
                'precipitation': (('time', 'lat', 'lon'), seasonal)
            },
            coords={
                'time': time,
                'lat': lat,
                'lon': lon
            }
        )
        
        return data
    
    def _create_sample_temperature(self):
        """Create sample temperature data"""
        # Create time series
        time = pd.date_range('1980-01-01', '2020-12-31', freq='MS')
        
        # Create spatial grid for Southern Africa
        lon = np.arange(10, 40.5, 0.5)
        lat = np.arange(-35, -9.5, 0.5)
        
        # Create random temperature data with seasonal cycle
        np.random.seed(42)
        n_times = len(time)
        n_lats = len(lat)
        n_lons = len(lon)
        
        # Seasonal cycle
        seasonal = np.zeros((n_times, n_lats, n_lons))
        for i, t in enumerate(time):
            month = t.month
            if month in [12, 1, 2]:  # Summer
                seasonal[i] = np.random.uniform(20, 35, (n_lats, n_lons))
            elif month in [6, 7, 8]:  # Winter
                seasonal[i] = np.random.uniform(5, 20, (n_lats, n_lons))
            else:  # Transition seasons
                seasonal[i] = np.random.uniform(10, 25, (n_lats, n_lons))
        
        # Add latitude effect
        lon_grid, lat_grid = np.meshgrid(lon, lat)
        lat_effect = lat_grid * 0.5  # Temperature decreases with latitude
        seasonal += lat_effect
        
        # Create xarray dataset
        data = xr.Dataset(
            data_vars={
                'temperature': (('time', 'lat', 'lon'), seasonal)
            },
            coords={
                'time': time,
                'lat': lat,
                'lon': lon
            }
        )
        
        return data
    
    def _create_sample_iod(self):
        """Create sample IOD data"""
        # Create time series
        time = pd.date_range('1980-01-01', '2020-12-31', freq='MS')
        
        # Create IOD-like time series with known events
        np.random.seed(42)
        n_months = len(time)
        
        # Base seasonal cycle
        seasonal = 0.3 * np.sin(2 * np.pi * np.arange(n_months) / 12)
        
        # Add known IOD events
        iod_events = np.zeros(n_months)
        
        # Strong positive IOD events
        iod_events[33:45] = 1.2   # 1982-83
        iod_events[213:225] = 1.5 # 1997-98
        iod_events[321:333] = 1.0 # 2006-07
        iod_events[381:393] = 1.3 # 2011-12
        
        # Strong negative IOD events
        iod_events[192:204] = -1.0 # 1996
        iod_events[360:372] = -1.2 # 2010
        iod_events[432:444] = -1.1 # 2016
        
        # Add noise
        noise = np.random.normal(0, 0.3, n_months)
        
        # Combine components
        dmi = seasonal + iod_events + noise
        
        # Create DataFrame
        data = pd.DataFrame({
            'time': time,
            'DMI': dmi
        })
        data.set_index('time', inplace=True)
        
        return data
    
    def run_download_workflow(self, use_sample_data=False):
        """
        Run the complete data download workflow
        """
        print("=" * 80)
        print("IOD-DROUGHT ANALYSIS DATA DOWNLOAD WORKFLOW")
        print("=" * 80)
        print(f"Data directory: {self.data_dir}")
        print(f"Output directory: {self.output_dir}")
        print(f"Study period: {self.start_year}-{self.end_year}")
        print(f"Region: Southern Africa ({self.southern_africa_bounds})")
        print("=" * 80)
        
        if use_sample_data:
            print("\nUsing sample data for testing...")
            sample_files = self.create_sample_data()
            return sample_files
        
        # Download real data
        print("\nDownloading real climate data...")
        
        # Download CHIRPS precipitation
        chirps_files = self.download_chirps_data()
        
        # Download ERA5 temperature (requires setup)
        era5_script = self.download_era5_data()
        
        # Download MODIS NDVI (requires setup)
        modis_script = self.download_modis_ndvi()
        
        # Download IOD data
        iod_files = self.download_iod_data()
        
        print("\n" + "=" * 80)
        print("DOWNLOAD WORKFLOW COMPLETE")
        print("=" * 80)
        print("Next steps:")
        print("1. Set up CDS API credentials for ERA5 download")
        print("2. Set up NASA Earthdata credentials for MODIS download")
        print("3. Run the index calculation workflow")
        print("=" * 80)
        
        return {
            'chirps_files': chirps_files,
            'era5_script': era5_script,
            'modis_script': modis_script,
            'iod_files': iod_files
        }

def main():
    """Main function to run the download workflow"""
    downloader = DataDownloader()
    
    # Ask user if they want to use sample data
    use_sample = input("Use sample data for testing? (y/n): ").lower().strip() == 'y'
    
    if use_sample:
        print("Using sample data for demonstration...")
        sample_files = downloader.run_download_workflow(use_sample_data=True)
        print(f"\nSample data created:")
        for data_type, file_path in sample_files.items():
            print(f"  {data_type}: {file_path}")
    else:
        print("Downloading real climate data...")
        downloader.run_download_workflow(use_sample_data=False)

if __name__ == "__main__":
    main()


















