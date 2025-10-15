"""
Data Processing Module for Climate Data

This module provides functions to load, process, and prepare climate data
for drought analysis in Southern Africa.

Author: Drought Analysis Toolkit
"""

import numpy as np
import pandas as pd
import xarray as xr
import netCDF4 as nc
import requests
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class ClimateDataProcessor:
    """
    Class for processing climate data for drought analysis
    """
    
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Southern Africa bounding box
        self.southern_africa_bounds = {
            'lon_min': -20, 'lon_max': 60,
            'lat_min': -40, 'lat_max': -10
        }
    
    def load_netcdf_data(self, file_path, var_name=None, time_slice=None, spatial_slice=None):
        """
        Load climate data from NetCDF file
        
        Parameters:
        -----------
        file_path : str
            Path to NetCDF file
        var_name : str, optional
            Variable name to load (if None, loads first variable)
        time_slice : slice or tuple, optional
            Time slice to extract
        spatial_slice : dict, optional
            Spatial slice {'lon': slice(), 'lat': slice()}
            
        Returns:
        --------
        xarray.DataArray
            Climate data
        """
        try:
            # Open dataset
            ds = xr.open_dataset(file_path)
            
            # Select variable
            if var_name is None:
                var_name = list(ds.data_vars.keys())[0]
            
            data = ds[var_name]
            
            # Apply time slice
            if time_slice is not None:
                if isinstance(time_slice, tuple):
                    data = data.sel(time=slice(time_slice[0], time_slice[1]))
                else:
                    data = data.isel(time=time_slice)
            
            # Apply spatial slice
            if spatial_slice is not None:
                for coord, slc in spatial_slice.items():
                    if coord in data.coords:
                        data = data.sel({coord: slc})
            
            return data
            
        except Exception as e:
            print(f"Error loading NetCDF file: {e}")
            return None
    
    def load_csv_data(self, file_path, lat_col='lat', lon_col='lon', 
                     time_col='time', value_col='value'):
        """
        Load climate data from CSV file
        
        Parameters:
        -----------
        file_path : str
            Path to CSV file
        lat_col : str
            Latitude column name
        lon_col : str
            Longitude column name
        time_col : str
            Time column name
        value_col : str
            Value column name
            
        Returns:
        --------
        xarray.DataArray
            Climate data
        """
        try:
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Convert time column to datetime
            df[time_col] = pd.to_datetime(df[time_col])
            
            # Create xarray DataArray
            data = df.set_index([time_col, lat_col, lon_col])[value_col].to_xarray()
            
            return data
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    
    def download_chirps_data(self, start_year=2000, end_year=2023, 
                           region='southern_africa', resolution='0.05'):
        """
        Download CHIRPS precipitation data for Southern Africa
        
        Parameters:
        -----------
        start_year : int
            Start year for data download
        end_year : int
            End year for data download
        region : str
            Region identifier
        resolution : str
            Data resolution ('0.05' or '0.25')
            
        Returns:
        --------
        str
            Path to downloaded data file
        """
        # CHIRPS data URL template
        base_url = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf"
        
        # Create filename
        filename = f"chirps-v2.0.{start_year}-{end_year}.days_p05.nc"
        file_path = self.data_dir / filename
        
        if file_path.exists():
            print(f"File already exists: {file_path}")
            return str(file_path)
        
        # Download URL
        url = f"{base_url}/{filename}"
        
        try:
            print(f"Downloading CHIRPS data from: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Download with progress bar
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\rDownload progress: {progress:.1f}%", end='')
            
            print(f"\nDownload complete: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"Error downloading CHIRPS data: {e}")
            return None
    
    def crop_to_southern_africa(self, data):
        """
        Crop data to Southern Africa region
        
        Parameters:
        -----------
        data : xarray.DataArray
            Input climate data
            
        Returns:
        --------
        xarray.DataArray
            Cropped data
        """
        bounds = self.southern_africa_bounds
        
        # Crop by coordinates
        if 'lon' in data.coords:
            data = data.sel(lon=slice(bounds['lon_min'], bounds['lon_max']))
        if 'lat' in data.coords:
            data = data.sel(lat=slice(bounds['lat_min'], bounds['lat_max']))
        
        return data
    
    def resample_to_monthly(self, data, method='sum'):
        """
        Resample daily data to monthly
        
        Parameters:
        -----------
        data : xarray.DataArray
            Daily climate data
        method : str
            Resampling method ('sum' for precipitation, 'mean' for temperature)
            
        Returns:
        --------
        xarray.DataArray
            Monthly data
        """
        if method == 'sum':
            return data.resample(time='M').sum()
        elif method == 'mean':
            return data.resample(time='M').mean()
        else:
            raise ValueError("Method must be 'sum' or 'mean'")
    
    def fill_missing_data(self, data, method='interpolate', max_gap=3):
        """
        Fill missing data in climate dataset
        
        Parameters:
        -----------
        data : xarray.DataArray
            Climate data with missing values
        method : str
            Method to fill missing data ('interpolate', 'forward_fill', 'backward_fill')
        max_gap : int
            Maximum gap length to fill
            
        Returns:
        --------
        xarray.DataArray
            Data with filled missing values
        """
        if method == 'interpolate':
            # Linear interpolation
            filled_data = data.interpolate_na(dim='time', method='linear', max_gap=max_gap)
        elif method == 'forward_fill':
            filled_data = data.fillna(method='ffill', limit=max_gap)
        elif method == 'backward_fill':
            filled_data = data.fillna(method='bfill', limit=max_gap)
        else:
            raise ValueError("Method must be 'interpolate', 'forward_fill', or 'backward_fill'")
        
        return filled_data
    
    def quality_control(self, data, min_value=None, max_value=None, 
                       outlier_threshold=3):
        """
        Perform quality control on climate data
        
        Parameters:
        -----------
        data : xarray.DataArray
            Climate data
        min_value : float, optional
            Minimum valid value
        max_value : float, optional
            Maximum valid value
        outlier_threshold : float
            Standard deviation threshold for outlier detection
            
        Returns:
        --------
        xarray.DataArray
            Quality-controlled data
        """
        # Create mask for valid data
        valid_mask = np.ones_like(data, dtype=bool)
        
        # Apply value range limits
        if min_value is not None:
            valid_mask &= (data >= min_value)
        if max_value is not None:
            valid_mask &= (data <= max_value)
        
        # Detect outliers using z-score
        if outlier_threshold is not None:
            z_scores = np.abs((data - data.mean()) / data.std())
            valid_mask &= (z_scores <= outlier_threshold)
        
        # Apply mask
        quality_data = data.where(valid_mask)
        
        return quality_data
    
    def create_southern_africa_mask(self, data):
        """
        Create a mask for Southern Africa land areas
        
        Parameters:
        -----------
        data : xarray.DataArray
            Climate data
            
        Returns:
        --------
        xarray.DataArray
            Boolean mask (True for land, False for ocean)
        """
        # Simple land mask based on data availability
        # In practice, you would use a proper land-sea mask
        land_mask = ~np.isnan(data).all(dim='time')
        
        return land_mask
    
    def prepare_drought_analysis_data(self, precip_file=None, temp_file=None,
                                    start_date='2000-01-01', end_date='2023-12-31'):
        """
        Prepare complete dataset for drought analysis
        
        Parameters:
        -----------
        precip_file : str, optional
            Path to precipitation data file
        temp_file : str, optional
            Path to temperature data file
        start_date : str
            Start date for analysis
        end_date : str
            End date for analysis
            
        Returns:
        --------
        tuple
            (precipitation, temperature) xarray DataArrays
        """
        print("Preparing drought analysis data...")
        
        # Load precipitation data
        if precip_file and os.path.exists(precip_file):
            print(f"Loading precipitation data from: {precip_file}")
            precip = self.load_netcdf_data(precip_file)
        else:
            print("Creating sample precipitation data...")
            from drought_indices import create_sample_data
            precip, _ = create_sample_data()
        
        # Load temperature data
        if temp_file and os.path.exists(temp_file):
            print(f"Loading temperature data from: {temp_file}")
            temp = self.load_netcdf_data(temp_file)
        else:
            print("Creating sample temperature data...")
            from drought_indices import create_sample_data
            _, temp = create_sample_data()
        
        # Crop to Southern Africa
        precip = self.crop_to_southern_africa(precip)
        temp = self.crop_to_southern_africa(temp)
        
        # Select time period
        precip = precip.sel(time=slice(start_date, end_date))
        temp = temp.sel(time=slice(start_date, end_date))
        
        # Quality control
        precip = self.quality_control(precip, min_value=0, max_value=1000)
        temp = self.quality_control(temp, min_value=-20, max_value=50)
        
        # Fill missing data
        precip = self.fill_missing_data(precip, method='interpolate')
        temp = self.fill_missing_data(temp, method='interpolate')
        
        print("Data preparation complete!")
        print(f"Precipitation shape: {precip.shape}")
        print(f"Temperature shape: {temp.shape}")
        
        return precip, temp
    
    def save_processed_data(self, data, filename, output_dir='data/processed'):
        """
        Save processed data to NetCDF file
        
        Parameters:
        -----------
        data : xarray.DataArray
            Data to save
        filename : str
            Output filename
        output_dir : str
            Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        file_path = output_path / filename
        
        try:
            data.to_netcdf(file_path)
            print(f"Data saved to: {file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")


def create_sample_station_data(n_stations=50, start_date='2000-01-01', 
                              end_date='2023-12-31'):
    """
    Create sample station data for Southern Africa
    
    Parameters:
    -----------
    n_stations : int
        Number of stations to create
    start_date : str
        Start date
    end_date : str
        End date
        
    Returns:
    --------
    pandas.DataFrame
        Station data
    """
    # Generate random station locations in Southern Africa
    np.random.seed(42)
    
    lats = np.random.uniform(-35, -15, n_stations)
    lons = np.random.uniform(-15, 50, n_stations)
    
    # Generate time series
    dates = pd.date_range(start_date, end_date, freq='M')
    
    # Create data for each station
    data_list = []
    
    for i in range(n_stations):
        # Generate realistic precipitation data
        base_precip = 50 + 30 * np.sin(np.radians(lons[i])) + 20 * np.cos(np.radians(lats[i]))
        seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
        noise = np.random.normal(0, 15, len(dates))
        
        precip = np.maximum(base_precip + seasonal + noise, 0)
        
        # Generate temperature data
        base_temp = 25 - 0.5 * np.abs(lats[i])
        temp_seasonal = 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
        temp_noise = np.random.normal(0, 2, len(dates))
        
        temp = base_temp + temp_seasonal + temp_noise
        
        # Create DataFrame for this station
        station_data = pd.DataFrame({
            'station_id': f'STA_{i:03d}',
            'lat': lats[i],
            'lon': lons[i],
            'time': dates,
            'precipitation': precip,
            'temperature': temp
        })
        
        data_list.append(station_data)
    
    # Combine all station data
    all_data = pd.concat(data_list, ignore_index=True)
    
    return all_data


if __name__ == "__main__":
    # Example usage
    processor = ClimateDataProcessor()
    
    # Create sample data
    print("Creating sample station data...")
    station_data = create_sample_station_data()
    
    # Save sample data
    sample_file = processor.data_dir / 'sample_station_data.csv'
    station_data.to_csv(sample_file, index=False)
    print(f"Sample data saved to: {sample_file}")
    
    # Prepare analysis data
    precip, temp = processor.prepare_drought_analysis_data()
    
    print("Data processing example completed!")







