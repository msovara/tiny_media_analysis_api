"""
Drought Indices Calculation Module

This module provides functions to calculate Standardized Precipitation Index (SPI)
and Standardized Precipitation Evapotranspiration Index (SPEI) for drought analysis.

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
    Class for calculating drought indices (SPI and SPEI)
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
    
    def calculate_spi(self, precipitation, scale=3, distribution='gamma'):
        """
        Calculate Standardized Precipitation Index (SPI)
        
        Parameters:
        -----------
        precipitation : xarray.DataArray or numpy.ndarray
            Precipitation data (mm)
        scale : int
            Time scale for SPI calculation (e.g., 3 for 3-month SPI)
        distribution : str
            Distribution to fit ('gamma' or 'normal')
            
        Returns:
        --------
        xarray.DataArray
            SPI values
        """
        if isinstance(precipitation, xr.DataArray):
            return self._calculate_spi_xarray(precipitation, scale, distribution)
        else:
            return self._calculate_spi_numpy(precipitation, scale, distribution)
    
    def _calculate_spi_xarray(self, precip, scale, distribution):
        """Calculate SPI for xarray DataArray"""
        # Create rolling sum for the specified scale
        precip_sum = precip.rolling(time=scale, min_periods=scale).sum()
        
        # Calculate SPI for each grid point
        spi = xr.apply_ufunc(
            self._spi_single_point,
            precip_sum,
            input_core_dims=[['time']],
            output_core_dims=[['time']],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[float]
        )
        
        return spi
    
    def _calculate_spi_numpy(self, precip, scale, distribution):
        """Calculate SPI for numpy array"""
        if precip.ndim == 1:
            # 1D array (time series)
            precip_sum = pd.Series(precip).rolling(window=scale, min_periods=scale).sum().values
            return self._spi_single_point(precip_sum)
        else:
            # 2D or 3D array
            result = np.full_like(precip, np.nan)
            for i in range(precip.shape[0]):
                if precip.ndim == 2:
                    result[i] = self._spi_single_point(precip[i])
                else:
                    for j in range(precip.shape[1]):
                        result[i, j] = self._spi_single_point(precip[i, j])
            return result
    
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
    
    def calculate_spei(self, precipitation, temperature, scale=3):
        """
        Calculate Standardized Precipitation Evapotranspiration Index (SPEI)
        
        Parameters:
        -----------
        precipitation : xarray.DataArray or numpy.ndarray
            Precipitation data (mm)
        temperature : xarray.DataArray or numpy.ndarray
            Temperature data (°C)
        scale : int
            Time scale for SPEI calculation
            
        Returns:
        --------
        xarray.DataArray
            SPEI values
        """
        # Calculate potential evapotranspiration (PET) using Thornthwaite method
        pet = self._calculate_pet_thornthwaite(temperature)
        
        # Calculate water balance (P - PET)
        water_balance = precipitation - pet
        
        # Calculate SPEI using the same method as SPI but with water balance
        spei = self.calculate_spi(water_balance, scale=scale, distribution='normal')
        
        return spei
    
    def _calculate_pet_thornthwaite(self, temperature):
        """
        Calculate Potential Evapotranspiration using Thornthwaite method
        
        Parameters:
        -----------
        temperature : xarray.DataArray or numpy.ndarray
            Temperature data (°C)
            
        Returns:
        --------
        xarray.DataArray or numpy.ndarray
            PET values (mm)
        """
        # Thornthwaite formula
        # PET = 16 * (10 * T / I)^a * (N / 12) * (DM / 30)
        # where I is the heat index, a is a function of I, N is day length, DM is days in month
        
        # Simplified version (monthly average)
        if isinstance(temperature, xr.DataArray):
            # For xarray, assume monthly data
            pet = 16 * ((10 * temperature / 12) ** 0.5)  # Simplified heat index
            return pet
        else:
            # For numpy arrays
            pet = 16 * ((10 * temperature / 12) ** 0.5)
            return pet
    
    def classify_drought(self, index_values, index_type='spi'):
        """
        Classify drought severity based on index values
        
        Parameters:
        -----------
        index_values : array-like
            SPI or SPEI values
        index_type : str
            Type of index ('spi' or 'spei')
            
        Returns:
        --------
        array-like
            Drought classification strings
        """
        classifications = np.full_like(index_values, 'unknown', dtype=object)
        
        # Apply classification thresholds
        classifications[index_values >= 2.0] = 'extremely_wet'
        classifications[(index_values >= 1.5) & (index_values < 2.0)] = 'severely_wet'
        classifications[(index_values >= 1.0) & (index_values < 1.5)] = 'moderately_wet'
        classifications[(index_values >= 0.5) & (index_values < 1.0)] = 'mildly_wet'
        classifications[(index_values >= -0.5) & (index_values < 0.5)] = 'near_normal'
        classifications[(index_values >= -1.0) & (index_values < -0.5)] = 'mildly_dry'
        classifications[(index_values >= -1.5) & (index_values < -1.0)] = 'moderately_dry'
        classifications[(index_values >= -2.0) & (index_values < -1.5)] = 'severely_dry'
        classifications[index_values < -2.0] = 'extremely_dry'
        
        return classifications
    
    def calculate_drought_frequency(self, index_values, threshold=-1.0, time_axis=0):
        """
        Calculate drought frequency for each location
        
        Parameters:
        -----------
        index_values : xarray.DataArray or numpy.ndarray
            SPI or SPEI values
        threshold : float
            Drought threshold (default -1.0 for moderate drought)
        time_axis : int
            Axis representing time dimension
            
        Returns:
        --------
        array-like
            Drought frequency (percentage of time in drought)
        """
        if isinstance(index_values, xr.DataArray):
            # For xarray DataArray
            drought_events = index_values < threshold
            total_time = drought_events.count(dim='time')
            drought_time = drought_events.sum(dim='time')
            frequency = (drought_time / total_time) * 100
            return frequency
        else:
            # For numpy arrays
            drought_events = index_values < threshold
            frequency = np.nanmean(drought_events, axis=time_axis) * 100
            return frequency
    
    def calculate_drought_severity(self, index_values, threshold=-1.0):
        """
        Calculate drought severity (average intensity during drought periods)
        
        Parameters:
        -----------
        index_values : xarray.DataArray or numpy.ndarray
            SPI or SPEI values
        threshold : float
            Drought threshold
            
        Returns:
        --------
        array-like
            Average drought severity during drought periods
        """
        if isinstance(index_values, xr.DataArray):
            # For xarray DataArray
            drought_mask = index_values < threshold
            drought_values = index_values.where(drought_mask)
            severity = drought_values.mean(dim='time')
            return severity
        else:
            # For numpy arrays
            drought_mask = index_values < threshold
            severity = np.full(index_values.shape[1:], np.nan)
            
            for i in range(index_values.shape[1]):
                if index_values.ndim == 2:
                    drought_data = index_values[:, i][drought_mask[:, i]]
                    if len(drought_data) > 0:
                        severity[i] = np.mean(drought_data)
                else:
                    for j in range(index_values.shape[2]):
                        drought_data = index_values[:, i, j][drought_mask[:, i, j]]
                        if len(drought_data) > 0:
                            severity[i, j] = np.mean(drought_data)
            
            return severity


def create_sample_data(lon_range=(-20, 60), lat_range=(-40, -10), 
                      time_range=('2000-01-01', '2023-12-31')):
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
        
    Returns:
    --------
    tuple
        (precipitation, temperature) xarray DataArrays
    """
    # Create coordinate arrays
    lon = np.linspace(lon_range[0], lon_range[1], 100)
    lat = np.linspace(lat_range[0], lat_range[1], 60)
    time = pd.date_range(time_range[0], time_range[1], freq='M')
    
    # Create synthetic precipitation data (mm/month)
    # Add some spatial and temporal patterns
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
    
    # Create xarray DataArrays
    precip = xr.DataArray(
        precip_data,
        coords={'time': time, 'lat': lat, 'lon': lon},
        dims=['time', 'lat', 'lon'],
        name='precipitation',
        attrs={'units': 'mm/month', 'long_name': 'Monthly precipitation'}
    )
    
    temp = xr.DataArray(
        temp_data,
        coords={'time': time, 'lat': lat, 'lon': lon},
        dims=['time', 'lat', 'lon'],
        name='temperature',
        attrs={'units': '°C', 'long_name': 'Monthly temperature'}
    )
    
    return precip, temp


if __name__ == "__main__":
    # Example usage
    print("Creating sample data for Southern Africa...")
    precip, temp = create_sample_data()
    
    print("Calculating SPI...")
    drought_calc = DroughtIndices()
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    
    print("Calculating drought frequency...")
    drought_freq = drought_calc.calculate_drought_frequency(spi_3m, threshold=-1.0)
    
    print("Sample data created successfully!")
    print(f"Precipitation shape: {precip.shape}")
    print(f"SPI shape: {spi_3m.shape}")
    print(f"Drought frequency shape: {drought_freq.shape}")







