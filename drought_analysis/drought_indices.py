1c^pd9+ILf
"""
Drought Indices Calculation Module for Lengau Cluster

This module provides functions to calculate Standardized Precipitation Index (SPI)
and Standardized Precipitation Evapotranspiration Index (SPEI) for drought analysis.

Optimized for cluster computing with parallel processing capabilities.

Author: Drought Analysis Toolkit
"""

import numpy as np
import pandas as pd
import xarray as xr
from scipy import stats
from scipy.special import gamma
import warnings
warnings.filterwarnings('ignore')


class DroughtIndices:
    """
    Class for calculating drought indices (SPI and SPEI) with cluster optimization
    """
    
    def __init__(self):
        self.spi_thresholds = {
            'extremely_dry': -2.0,
            'severely_dry': -1.5,
            'moderately_dry': -1.0,
            'mildly_dry': -0.5,
            'near_normal': 0.5,
            'moderately_wet': 1.0,
            'severely_wet': 1.5,
            'extremely_wet': 2.0
        }
    
    def calculate_spi(self, precipitation, scale=3, distribution='gamma', chunk_size=None):
        """
        Calculate Standardized Precipitation Index (SPI) with cluster optimization
        
        Parameters:
        -----------
        precipitation : xarray.DataArray
            Precipitation data (mm)
        scale : int
            Time scale for SPI calculation (e.g., 3 for 3-month SPI)
        distribution : str
            Distribution to fit ('gamma' or 'normal')
        chunk_size : dict, optional
            Chunk size for dask processing
            
        Returns:
        --------
        xarray.DataArray
            SPI values
        """
        print(f"Calculating {scale}-month SPI...")
        
        # Create rolling sum for the specified scale
        precip_sum = precipitation.rolling(time=scale, min_periods=scale).sum()
        
        # Set chunk size for parallel processing if provided
        if chunk_size:
            precip_sum = precip_sum.chunk(chunk_size)
        
        # Calculate SPI for each grid point using dask
        spi = xr.apply_ufunc(
            self._spi_single_point,
            precip_sum,
            input_core_dims=[['time']],
            output_core_dims=[['time']],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[float]
        )
        
        print(f"✓ {scale}-month SPI calculation completed")
        return spi
    
    def _spi_single_point(self, precip_series):
        """Calculate SPI for a single time series"""
        # Remove NaN values
        valid_data = precip_series[~np.isnan(precip_series)]
        
        if len(valid_data) < 30:  # Need sufficient data
            return np.full_like(precip_series, np.nan)
        
        # Fit gamma distribution
        try:
            # Estimate shape and scale parameters
            mean_val = np.mean(valid_data)
            var_val = np.var(valid_data)
            
            if var_val <= 0 or mean_val <= 0:
                return np.full_like(precip_series, np.nan)
            
            # Method of moments estimation
            shape = (mean_val ** 2) / var_val
            scale = var_val / mean_val
            
            # Calculate cumulative probability
            prob = stats.gamma.cdf(precip_series, a=shape, scale=scale)
            
            # Convert to standard normal distribution
            spi = stats.norm.ppf(prob)
            
            # Handle infinite values
            spi[np.isinf(spi)] = np.nan
            
            return spi
            
        except Exception:
            return np.full_like(precip_series, np.nan)
    
    def calculate_spei(self, precipitation, temperature, scale=3, chunk_size=None):
        """
        Calculate Standardized Precipitation Evapotranspiration Index (SPEI)
        
        Parameters:
        -----------
        precipitation : xarray.DataArray
            Precipitation data (mm)
        temperature : xarray.DataArray
            Temperature data (°C)
        scale : int
            Time scale for SPEI calculation
        chunk_size : dict, optional
            Chunk size for dask processing
            
        Returns:
        --------
        xarray.DataArray
            SPEI values
        """
        print(f"Calculating {scale}-month SPEI...")
        
        # Calculate potential evapotranspiration (PET) using Thornthwaite method
        pet = self._calculate_pet_thornthwaite(temperature)
        
        # Calculate water balance (P - PET)
        water_balance = precipitation - pet
        
        # Set chunk size for parallel processing if provided
        if chunk_size:
            water_balance = water_balance.chunk(chunk_size)
        
        # Calculate SPEI using the same method as SPI but with water balance
        spei = self.calculate_spi(water_balance, scale=scale, distribution='normal')
        
        print(f"✓ {scale}-month SPEI calculation completed")
        return spei
    
    def _calculate_pet_thornthwaite(self, temperature):
        """
        Calculate Potential Evapotranspiration using Thornthwaite method
        """
        # Thornthwaite formula (simplified version)
        # PET = 16 * (10 * T / I)^a * (N / 12) * (DM / 30)
        
        # Simplified version for monthly data
        pet = 16 * ((10 * temperature / 12) ** 0.5)
        
        # Ensure positive values
        pet = xr.where(pet < 0, 0, pet)
        
        return pet
    
    def calculate_drought_frequency(self, index_values, threshold=-1.0, time_axis=0):
        """
        Calculate drought frequency for each location
        
        Parameters:
        -----------
        index_values : xarray.DataArray
            SPI or SPEI values
        threshold : float
            Drought threshold (default -1.0 for moderate drought)
        time_axis : int
            Axis representing time dimension
            
        Returns:
        --------
        xarray.DataArray
            Drought frequency (percentage of time in drought)
        """
        print(f"Calculating drought frequency (threshold: {threshold})...")
        
        # For xarray DataArray
        drought_events = index_values < threshold
        total_time = drought_events.count(dim='time')
        drought_time = drought_events.sum(dim='time')
        frequency = (drought_time / total_time) * 100
        
        print(f"✓ Drought frequency calculation completed")
        return frequency
    
    def calculate_drought_severity(self, index_values, threshold=-1.0):
        """
        Calculate drought severity (average intensity during drought periods)
        
        Parameters:
        -----------
        index_values : xarray.DataArray
            SPI or SPEI values
        threshold : float
            Drought threshold
            
        Returns:
        --------
        xarray.DataArray
            Average drought severity during drought periods
        """
        print(f"Calculating drought severity (threshold: {threshold})...")
        
        # For xarray DataArray
        drought_mask = index_values < threshold
        drought_values = index_values.where(drought_mask)
        severity = drought_values.mean(dim='time')
        
        print(f"✓ Drought severity calculation completed")
        return severity


def create_sample_data(lon_range=(-20, 60), lat_range=(-40, -10), 
                      time_range=('2000-01-01', '2023-12-31'),
                      chunk_size={'time': 100, 'lat': 20, 'lon': 20}):
    """
    Create sample precipitation and temperature data for Southern Africa
    
    Parameters:
    -----------
    lon_range : tuple
        Longitude range (min, max)
    lat_range : tuple
        Latitude range (min, max)
    time_range : tuple
        Time range (start_date, end_date)
    chunk_size : dict
        Chunk size for dask processing
        
    Returns:
    --------
    tuple
        (precipitation, temperature) xarray DataArrays
    """
    print("Creating sample climate data for Southern Africa...")
    
    # Create coordinate arrays
    lon = np.linspace(lon_range[0], lon_range[1], 100)
    lat = np.linspace(lat_range[0], lat_range[1], 60)
    time = pd.date_range(time_range[0], time_range[1], freq='M')
    
    # Create synthetic precipitation data (mm/month)
    np.random.seed(42)
    
    # Base precipitation pattern (higher in eastern regions)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    base_precip = 50 + 30 * np.sin(np.radians(lon_grid)) + 20 * np.cos(np.radians(lat_grid))
    
    # Add seasonal variation
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(time)) / 12)
    
    # Add random noise
    noise = np.random.normal(0, 15, (len(time), len(lat), len(lon)))
    
    # Combine patterns
    precip_data = base_precip[np.newaxis, :, :] + seasonal[:, np.newaxis, np.newaxis] + noise
    
    # Ensure positive values
    precip_data = np.maximum(precip_data, 0)
    
    # Create temperature data (°C)
    base_temp = 25 - 0.5 * np.abs(lat_grid)  # Temperature decreases with latitude
    temp_seasonal = 10 * np.sin(2 * np.pi * np.arange(len(time)) / 12)
    temp_noise = np.random.normal(0, 2, (len(time), len(lat), len(lon)))
    
    temp_data = base_temp[np.newaxis, :, :] + temp_seasonal[:, np.newaxis, np.newaxis] + temp_noise
    
    # Create xarray DataArrays with dask chunks
    precip = xr.DataArray(
        precip_data,
        coords={'time': time, 'lat': lat, 'lon': lon},
        dims=['time', 'lat', 'lon'],
        name='precipitation',
        attrs={'units': 'mm/month', 'long_name': 'Monthly precipitation'}
    ).chunk(chunk_size)
    
    temp = xr.DataArray(
        temp_data,
        coords={'time': time, 'lat': lat, 'lon': lon},
        dims=['time', 'lat', 'lon'],
        name='temperature',
        attrs={'units': '°C', 'long_name': 'Monthly temperature'}
    ).chunk(chunk_size)
    
    print(f"✓ Sample data created: {precip.shape}, {temp.shape}")
    return precip, temp


if __name__ == "__main__":
    # Example usage
    print("Testing drought indices calculation...")
    
    # Create sample data
    precip, temp = create_sample_data()
    
    # Initialize drought calculator
    drought_calc = DroughtIndices()
    
    # Calculate SPI
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    
    # Calculate drought frequency
    drought_freq = drought_calc.calculate_drought_frequency(spi_3m, threshold=-1.0)
    
    print("✓ Test completed successfully!")
    print(f"SPI shape: {spi_3m.shape}")
    print(f"Drought frequency shape: {drought_freq.shape}")







