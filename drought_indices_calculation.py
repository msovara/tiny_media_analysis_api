"""
Drought Indices Calculation Workflow

This script calculates drought indices (SPI, SPEI, NDVI) from climate data
for IOD-drought correlation analysis in Southern Africa.

Author: Mthetho Sovara
Date: June 2025
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
import warnings
from scipy import stats
from scipy.special import gamma
import netCDF4 as nc
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

class DroughtIndicesCalculator:
    """Main class for calculating drought indices"""
    
    def __init__(self, data_dir='data', output_dir='output'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create output subdirectories
        (self.output_dir / 'spi').mkdir(exist_ok=True)
        (self.output_dir / 'spei').mkdir(exist_ok=True)
        (self.output_dir / 'ndvi').mkdir(exist_ok=True)
        (self.output_dir / 'maps').mkdir(exist_ok=True)
        
        # Southern Africa bounds
        self.southern_africa_bounds = {
            'lon_min': 10, 'lon_max': 40,
            'lat_min': -35, 'lat_max': -10
        }
        
        # Study period
        self.start_year = 1980
        self.end_year = 2020
        
    def calculate_spi(self, precipitation_data, scale=3, distribution='gamma'):
        """
        Calculate Standardized Precipitation Index (SPI)
        
        Parameters:
        -----------
        precipitation_data : xarray.DataArray
            Precipitation data in mm
        scale : int
            Time scale for SPI calculation (months)
        distribution : str
            Distribution to fit ('gamma' or 'normal')
            
        Returns:
        --------
        xarray.DataArray
            SPI values
        """
        print(f"Calculating SPI-{scale}...")
        
        # Convert to numpy array for processing
        if isinstance(precipitation_data, xr.DataArray):
            precip_array = precipitation_data.values
            coords = precipitation_data.coords
            dims = precipitation_data.dims
        else:
            precip_array = precipitation_data
            coords = None
            dims = None
        
        # Get dimensions
        if len(precip_array.shape) == 3:  # time, lat, lon
            n_times, n_lats, n_lons = precip_array.shape
        else:
            raise ValueError("Precipitation data must be 3D (time, lat, lon)")
        
        # Initialize SPI array
        spi_array = np.full_like(precip_array, np.nan)
        
        # Calculate SPI for each grid point
        for i in range(n_lats):
            for j in range(n_lons):
                # Extract time series for this grid point
                ts = precip_array[:, i, j]
                
                # Skip if too many missing values
                valid_idx = ~np.isnan(ts)
                if np.sum(valid_idx) < 30:  # Need at least 30 valid points
                    continue
                
                # Calculate rolling sum for the specified scale
                if scale > 1:
                    # Pad with NaN for rolling calculation
                    padded_ts = np.full(len(ts) + scale - 1, np.nan)
                    padded_ts[scale-1:] = ts
                    
                    # Calculate rolling sum
                    rolling_sum = np.full_like(ts, np.nan)
                    for t in range(len(ts)):
                        if t >= scale - 1:
                            window = padded_ts[t-scale+1:t+1]
                            if not np.any(np.isnan(window)):
                                rolling_sum[t] = np.sum(window)
                else:
                    rolling_sum = ts.copy()
                
                # Calculate SPI for this time series
                spi_ts = self._calculate_spi_timeseries(rolling_sum, distribution)
                spi_array[:, i, j] = spi_ts
        
        # Create output DataArray
        if coords is not None:
            spi_data = xr.DataArray(
                spi_array,
                coords=coords,
                dims=dims,
                name=f'SPI-{scale}'
            )
        else:
            spi_data = spi_array
        
        # Save to file
        output_file = self.output_dir / 'spi' / f'spi_{scale}month.nc'
        if isinstance(spi_data, xr.DataArray):
            spi_data.to_netcdf(output_file)
            print(f"✓ SPI-{scale} saved to: {output_file}")
        
        return spi_data
    
    def _calculate_spi_timeseries(self, ts, distribution='gamma'):
        """
        Calculate SPI for a single time series
        """
        # Remove NaN values for fitting
        valid_idx = ~np.isnan(ts)
        if np.sum(valid_idx) < 10:
            return np.full_like(ts, np.nan)
        
        valid_ts = ts[valid_idx]
        
        if distribution == 'gamma':
            # Fit gamma distribution
            try:
                # Method of moments for gamma distribution
                mean_val = np.mean(valid_ts)
                var_val = np.var(valid_ts)
                
                if var_val > 0:
                    # Gamma parameters
                    shape = mean_val**2 / var_val
                    scale = var_val / mean_val
                    
                    # Calculate SPI
                    spi_ts = np.full_like(ts, np.nan)
                    for i, val in enumerate(ts):
                        if not np.isnan(val):
                            # Calculate cumulative probability
                            if val > 0:
                                prob = stats.gamma.cdf(val, shape, scale=scale)
                                # Convert to standard normal
                                spi_ts[i] = stats.norm.ppf(prob)
                            else:
                                spi_ts[i] = -3.0  # Very dry
                    return spi_ts
                else:
                    return np.full_like(ts, np.nan)
            except:
                return np.full_like(ts, np.nan)
        
        elif distribution == 'normal':
            # Fit normal distribution
            try:
                mean_val = np.mean(valid_ts)
                std_val = np.std(valid_ts)
                
                if std_val > 0:
                    spi_ts = (ts - mean_val) / std_val
                    return spi_ts
                else:
                    return np.full_like(ts, np.nan)
            except:
                return np.full_like(ts, np.nan)
        
        else:
            raise ValueError(f"Unknown distribution: {distribution}")
    
    def calculate_spei(self, precipitation_data, temperature_data, scale=3):
        """
        Calculate Standardized Precipitation Evapotranspiration Index (SPEI)
        
        Parameters:
        -----------
        precipitation_data : xarray.DataArray
            Precipitation data in mm
        temperature_data : xarray.DataArray
            Temperature data in °C
        scale : int
            Time scale for SPEI calculation (months)
            
        Returns:
        --------
        xarray.DataArray
            SPEI values
        """
        print(f"Calculating SPEI-{scale}...")
        
        # Calculate potential evapotranspiration (PET)
        print("  Calculating potential evapotranspiration...")
        pet_data = self._calculate_pet(temperature_data)
        
        # Calculate water balance (P - PET)
        print("  Calculating water balance...")
        water_balance = precipitation_data - pet_data
        
        # Calculate SPEI using water balance
        print("  Calculating SPEI from water balance...")
        spei_data = self._calculate_spei_from_balance(water_balance, scale)
        
        # Save to file
        output_file = self.output_dir / 'spei' / f'spei_{scale}month.nc'
        spei_data.to_netcdf(output_file)
        print(f"✓ SPEI-{scale} saved to: {output_file}")
        
        return spei_data
    
    def _calculate_pet(self, temperature_data):
        """
        Calculate potential evapotranspiration using Thornthwaite method
        """
        # Thornthwaite formula for PET
        # PET = 16 * (10 * T / I)^a * (N / 12) * (dm / 30)
        # where T is temperature, I is heat index, a is exponent, N is day length, dm is days in month
        
        # Convert temperature to numpy array
        if isinstance(temperature_data, xr.DataArray):
            temp_array = temperature_data.values
            coords = temperature_data.coords
            dims = temperature_data.dims
        else:
            temp_array = temperature_data
            coords = None
            dims = None
        
        # Calculate heat index (I) - sum of (T/5)^1.514 for months with T > 0
        heat_index = np.zeros(temp_array.shape[1:])  # lat, lon
        
        for i in range(temp_array.shape[1]):
            for j in range(temp_array.shape[2]):
                monthly_temps = temp_array[:, i, j]
                valid_temps = monthly_temps[~np.isnan(monthly_temps)]
                positive_temps = valid_temps[valid_temps > 0]
                
                if len(positive_temps) > 0:
                    heat_index[i, j] = np.sum((positive_temps / 5) ** 1.514)
        
        # Calculate PET for each month
        pet_array = np.full_like(temp_array, np.nan)
        
        for t in range(temp_array.shape[0]):
            for i in range(temp_array.shape[1]):
                for j in range(temp_array.shape[2]):
                    temp = temp_array[t, i, j]
                    if not np.isnan(temp) and not np.isnan(heat_index[i, j]) and heat_index[i, j] > 0:
                        # Thornthwaite formula
                        if temp > 0:
                            a = 0.49239 + 1.7921e-2 * heat_index[i, j] - 7.71e-5 * heat_index[i, j]**2 + 6.75e-7 * heat_index[i, j]**3
                            pet_val = 16 * ((10 * temp) / heat_index[i, j]) ** a
                            pet_array[t, i, j] = pet_val
                        else:
                            pet_array[t, i, j] = 0
        
        # Create output DataArray
        if coords is not None:
            pet_data = xr.DataArray(
                pet_array,
                coords=coords,
                dims=dims,
                name='PET'
            )
        else:
            pet_data = pet_array
        
        return pet_data
    
    def _calculate_spei_from_balance(self, water_balance, scale):
        """
        Calculate SPEI from water balance time series
        """
        # Convert to numpy array
        if isinstance(water_balance, xr.DataArray):
            balance_array = water_balance.values
            coords = water_balance.coords
            dims = water_balance.dims
        else:
            balance_array = water_balance
            coords = None
            dims = None
        
        # Get dimensions
        n_times, n_lats, n_lons = balance_array.shape
        
        # Initialize SPEI array
        spei_array = np.full_like(balance_array, np.nan)
        
        # Calculate SPEI for each grid point
        for i in range(n_lats):
            for j in range(n_lons):
                # Extract time series for this grid point
                ts = balance_array[:, i, j]
                
                # Skip if too many missing values
                valid_idx = ~np.isnan(ts)
                if np.sum(valid_idx) < 30:
                    continue
                
                # Calculate rolling sum for the specified scale
                if scale > 1:
                    # Calculate rolling sum
                    rolling_sum = np.full_like(ts, np.nan)
                    for t in range(len(ts)):
                        if t >= scale - 1:
                            window = ts[t-scale+1:t+1]
                            if not np.any(np.isnan(window)):
                                rolling_sum[t] = np.sum(window)
                else:
                    rolling_sum = ts.copy()
                
                # Calculate SPEI using log-logistic distribution
                spei_ts = self._calculate_spei_timeseries(rolling_sum)
                spei_array[:, i, j] = spei_ts
        
        # Create output DataArray
        if coords is not None:
            spei_data = xr.DataArray(
                spei_array,
                coords=coords,
                dims=dims,
                name=f'SPEI-{scale}'
            )
        else:
            spei_data = spei_array
        
        return spei_data
    
    def _calculate_spei_timeseries(self, ts):
        """
        Calculate SPEI for a single time series using log-logistic distribution
        """
        # Remove NaN values for fitting
        valid_idx = ~np.isnan(ts)
        if np.sum(valid_idx) < 10:
            return np.full_like(ts, np.nan)
        
        valid_ts = ts[valid_idx]
        
        try:
            # Fit log-logistic distribution
            # Method of L-moments
            sorted_ts = np.sort(valid_ts)
            n = len(sorted_ts)
            
            # Calculate L-moments
            l1 = np.mean(sorted_ts)
            l2 = 0
            for i in range(n):
                l2 += (2 * i - n + 1) * sorted_ts[i]
            l2 /= (n * (n - 1))
            
            if l2 > 0:
                # Log-logistic parameters
                beta = l1
                alpha = l2 / (2 * np.sqrt(3))
                
                # Calculate SPEI
                spei_ts = np.full_like(ts, np.nan)
                for i, val in enumerate(ts):
                    if not np.isnan(val):
                        # Calculate cumulative probability
                        prob = 1 / (1 + (alpha / (val - beta)) ** (1/alpha))
                        # Convert to standard normal
                        spei_ts[i] = stats.norm.ppf(prob)
                return spei_ts
            else:
                return np.full_like(ts, np.nan)
        except:
            return np.full_like(ts, np.nan)
    
    def calculate_ndvi_anomalies(self, ndvi_data):
        """
        Calculate NDVI anomalies for drought analysis
        
        Parameters:
        -----------
        ndvi_data : xarray.DataArray
            NDVI data (0-1 scale)
            
        Returns:
        --------
        xarray.DataArray
            NDVI anomalies
        """
        print("Calculating NDVI anomalies...")
        
        # Calculate climatological mean for each month
        monthly_mean = ndvi_data.groupby('time.month').mean('time')
        
        # Calculate anomalies
        ndvi_anomalies = ndvi_data.groupby('time.month') - monthly_mean
        
        # Save to file
        output_file = self.output_dir / 'ndvi' / 'ndvi_anomalies.nc'
        ndvi_anomalies.to_netcdf(output_file)
        print(f"✓ NDVI anomalies saved to: {output_file}")
        
        return ndvi_anomalies
    
    def create_drought_maps(self, drought_index, index_name, output_file=None):
        """
        Create drought index maps
        
        Parameters:
        -----------
        drought_index : xarray.DataArray
            Drought index data
        index_name : str
            Name of the drought index
        output_file : str, optional
            Output file path
        """
        print(f"Creating {index_name} map...")
        
        # Create figure
        fig = plt.figure(figsize=(12, 10))
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        # Set up colormap
        cmap = plt.cm.RdYlBu_r
        norm = plt.Normalize(vmin=-3, vmax=3)
        
        # Plot drought index
        im = ax.pcolormesh(drought_index.lon, drought_index.lat, 
                         drought_index.isel(time=-1),  # Latest time step
                         cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        
        # Add coastlines and borders
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        
        # Add gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', pad=0.05, shrink=0.8)
        cbar.set_label(f'{index_name} Values')
        
        # Add title
        plt.title(f'{index_name} Map - Southern Africa')
        
        # Save figure
        if output_file is None:
            output_file = self.output_dir / 'maps' / f'{index_name.lower()}_map.png'
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ {index_name} map saved to: {output_file}")
        plt.close()
    
    def run_calculation_workflow(self, precip_file=None, temp_file=None, ndvi_file=None):
        """
        Run the complete drought indices calculation workflow
        """
        print("=" * 80)
        print("DROUGHT INDICES CALCULATION WORKFLOW")
        print("=" * 80)
        
        # Load data
        print("\n1. Loading climate data...")
        
        if precip_file and Path(precip_file).exists():
            print(f"Loading precipitation data from: {precip_file}")
            precip_data = xr.open_dataarray(precip_file)
        else:
            print("Using sample precipitation data...")
            precip_data = self._create_sample_precipitation()
        
        if temp_file and Path(temp_file).exists():
            print(f"Loading temperature data from: {temp_file}")
            temp_data = xr.open_dataarray(temp_file)
        else:
            print("Using sample temperature data...")
            temp_data = self._create_sample_temperature()
        
        if ndvi_file and Path(ndvi_file).exists():
            print(f"Loading NDVI data from: {ndvi_file}")
            ndvi_data = xr.open_dataarray(ndvi_file)
        else:
            print("Using sample NDVI data...")
            ndvi_data = self._create_sample_ndvi()
        
        # Calculate drought indices
        print("\n2. Calculating drought indices...")
        
        # Calculate SPI for different time scales
        spi_scales = [1, 3, 6, 12]
        spi_results = {}
        
        for scale in spi_scales:
            print(f"  Calculating SPI-{scale}...")
            spi_data = self.calculate_spi(precip_data, scale=scale)
            spi_results[f'SPI-{scale}'] = spi_data
            
            # Create map
            self.create_drought_maps(spi_data, f'SPI-{scale}')
        
        # Calculate SPEI for different time scales
        spei_scales = [1, 3, 6, 12]
        spei_results = {}
        
        for scale in spei_scales:
            print(f"  Calculating SPEI-{scale}...")
            spei_data = self.calculate_spei(precip_data, temp_data, scale=scale)
            spei_results[f'SPEI-{scale}'] = spei_data
            
            # Create map
            self.create_drought_maps(spei_data, f'SPEI-{scale}')
        
        # Calculate NDVI anomalies
        print("  Calculating NDVI anomalies...")
        ndvi_anomalies = self.calculate_ndvi_anomalies(ndvi_data)
        self.create_drought_maps(ndvi_anomalies, 'NDVI Anomalies')
        
        print("\n" + "=" * 80)
        print("DROUGHT INDICES CALCULATION COMPLETE")
        print("=" * 80)
        print("Output files saved to:")
        print(f"  SPI files: {self.output_dir / 'spi'}")
        print(f"  SPEI files: {self.output_dir / 'spei'}")
        print(f"  NDVI files: {self.output_dir / 'ndvi'}")
        print(f"  Maps: {self.output_dir / 'maps'}")
        print("=" * 80)
        
        return {
            'spi': spi_results,
            'spei': spei_results,
            'ndvi': ndvi_anomalies
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
        
        # Create xarray dataset
        data = xr.DataArray(
            seasonal,
            coords={'time': time, 'lat': lat, 'lon': lon},
            dims=('time', 'lat', 'lon'),
            name='precipitation'
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
        
        # Create xarray dataset
        data = xr.DataArray(
            seasonal,
            coords={'time': time, 'lat': lat, 'lon': lon},
            dims=('time', 'lat', 'lon'),
            name='temperature'
        )
        
        return data
    
    def _create_sample_ndvi(self):
        """Create sample NDVI data"""
        # Create time series
        time = pd.date_range('1980-01-01', '2020-12-31', freq='MS')
        
        # Create spatial grid for Southern Africa
        lon = np.arange(10, 40.5, 0.5)
        lat = np.arange(-35, -9.5, 0.5)
        
        # Create random NDVI data with seasonal cycle
        np.random.seed(42)
        n_times = len(time)
        n_lats = len(lat)
        n_lons = len(lon)
        
        # Seasonal cycle
        seasonal = np.zeros((n_times, n_lats, n_lons))
        for i, t in enumerate(time):
            month = t.month
            if month in [12, 1, 2]:  # Summer
                seasonal[i] = np.random.uniform(0.6, 0.9, (n_lats, n_lons))
            elif month in [6, 7, 8]:  # Winter
                seasonal[i] = np.random.uniform(0.2, 0.5, (n_lats, n_lons))
            else:  # Transition seasons
                seasonal[i] = np.random.uniform(0.4, 0.7, (n_lats, n_lons))
        
        # Create xarray dataset
        data = xr.DataArray(
            seasonal,
            coords={'time': time, 'lat': lat, 'lon': lon},
            dims=('time', 'lat', 'lon'),
            name='ndvi'
        )
        
        return data

def main():
    """Main function to run the calculation workflow"""
    calculator = DroughtIndicesCalculator()
    
    # Ask user for data files
    print("Drought Indices Calculation Workflow")
    print("=" * 50)
    
    precip_file = input("Precipitation data file (or press Enter for sample): ").strip()
    if not precip_file:
        precip_file = None
    
    temp_file = input("Temperature data file (or press Enter for sample): ").strip()
    if not temp_file:
        temp_file = None
    
    ndvi_file = input("NDVI data file (or press Enter for sample): ").strip()
    if not ndvi_file:
        ndvi_file = None
    
    # Run calculation workflow
    results = calculator.run_calculation_workflow(
        precip_file=precip_file,
        temp_file=temp_file,
        ndvi_file=ndvi_file
    )
    
    print(f"\nCalculation complete! Results saved to: {calculator.output_dir}")

if __name__ == "__main__":
    main()


















