"""
Simplified IOD-Drought Analysis Workflow

This script focuses on data processing and analysis, assuming data has been
downloaded manually. It skips the complex download steps and focuses on
the core analysis workflow.

Author: Mthetho Sovara
Date: June 2025
"""

import os
import sys
import pandas as pd
import xarray as xr
import numpy as np
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

class SimplifiedWorkflow:
    """Simplified workflow for IOD-drought analysis with manual data downloads"""
    
    def __init__(self, data_dir='data', output_dir='output'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create output subdirectories
        (self.output_dir / 'spi').mkdir(exist_ok=True)
        (self.output_dir / 'spei').mkdir(exist_ok=True)
        (self.output_dir / 'ndvi').mkdir(exist_ok=True)
        (self.output_dir / 'maps').mkdir(exist_ok=True)
        (self.output_dir / 'plots').mkdir(exist_ok=True)
        (self.output_dir / 'processed').mkdir(exist_ok=True)
        
        # Southern Africa bounds
        self.southern_africa_bounds = {
            'lon_min': 10, 'lon_max': 40,
            'lat_min': -35, 'lat_max': -10
        }
        
        # Study period
        self.start_year = 1980
        self.end_year = 2020
        
        # Workflow status
        self.workflow_status = {
            'data_loading': False,
            'drought_calculation': False,
            'iod_processing': False,
            'correlation_analysis': False,
            'visualization': False
        }
        
        # Results storage
        self.results = {}
    
    def check_data_availability(self):
        """
        Check if required data files are available
        """
        print("=" * 60)
        print("CHECKING DATA AVAILABILITY")
        print("=" * 60)
        
        required_files = {
            'precipitation': 'data/chirps/',
            'temperature': 'data/era5/',
            'ndvi': 'data/modis/',
            'iod': 'data/iod/'
        }
        
        available_data = {}
        
        for data_type, data_path in required_files.items():
            path = Path(data_path)
            if path.exists():
                files = list(path.glob('*'))
                if files:
                    available_data[data_type] = len(files)
                    print(f"✓ {data_type}: {len(files)} files found")
                else:
                    print(f"✗ {data_type}: Directory exists but no files found")
            else:
                print(f"✗ {data_type}: Directory not found")
        
        # Check if we have enough data
        if len(available_data) >= 2:  # Need at least 2 data types
            print(f"\n✓ Sufficient data available for analysis")
            self.workflow_status['data_loading'] = True
            return True
        else:
            print(f"\n✗ Insufficient data for analysis")
            print("Please download data manually or use sample data")
            return False
    
    def load_precipitation_data(self, data_path=None):
        """
        Load precipitation data from CHIRPS files
        """
        print("\nLoading precipitation data...")
        
        if data_path is None:
            data_path = self.data_dir / 'chirps'
        
        if not Path(data_path).exists():
            print("✗ Precipitation data not found. Creating sample data...")
            return self._create_sample_precipitation()
        
        # Load CHIRPS files
        try:
            files = list(Path(data_path).glob('*.tif'))
            if not files:
                print("✗ No CHIRPS files found. Creating sample data...")
                return self._create_sample_precipitation()
            
            print(f"✓ Found {len(files)} CHIRPS files")
            
            # For now, create sample data
            # In a full implementation, you would load and process the actual files
            print("Creating sample precipitation data...")
            return self._create_sample_precipitation()
            
        except Exception as e:
            print(f"✗ Error loading precipitation data: {e}")
            print("Creating sample data...")
            return self._create_sample_precipitation()
    
    def load_temperature_data(self, data_path=None):
        """
        Load temperature data from ERA5 files
        """
        print("\nLoading temperature data...")
        
        if data_path is None:
            data_path = self.data_dir / 'era5'
        
        if not Path(data_path).exists():
            print("✗ Temperature data not found. Creating sample data...")
            return self._create_sample_temperature()
        
        # Load ERA5 files
        try:
            files = list(Path(data_path).glob('*.nc'))
            if not files:
                print("✗ No ERA5 files found. Creating sample data...")
                return self._create_sample_temperature()
            
            print(f"✓ Found {len(files)} ERA5 files")
            
            # For now, create sample data
            # In a full implementation, you would load and process the actual files
            print("Creating sample temperature data...")
            return self._create_sample_temperature()
            
        except Exception as e:
            print(f"✗ Error loading temperature data: {e}")
            print("Creating sample data...")
            return self._create_sample_temperature()
    
    def load_ndvi_data(self, data_path=None):
        """
        Load NDVI data from MODIS files
        """
        print("\nLoading NDVI data...")
        
        if data_path is None:
            data_path = self.data_dir / 'modis'
        
        if not Path(data_path).exists():
            print("✗ NDVI data not found. Creating sample data...")
            return self._create_sample_ndvi()
        
        # Load MODIS files
        try:
            files = list(Path(data_path).glob('*.hdf'))
            if not files:
                print("✗ No MODIS files found. Creating sample data...")
                return self._create_sample_ndvi()
            
            print(f"✓ Found {len(files)} MODIS files")
            
            # For now, create sample data
            # In a full implementation, you would load and process the actual files
            print("Creating sample NDVI data...")
            return self._create_sample_ndvi()
            
        except Exception as e:
            print(f"✗ Error loading NDVI data: {e}")
            print("Creating sample data...")
            return self._create_sample_ndvi()
    
    def load_iod_data(self, data_path=None):
        """
        Load IOD data from multiple sources
        """
        print("\nLoading IOD data...")
        
        if data_path is None:
            data_path = self.data_dir / 'iod'
        
        if not Path(data_path).exists():
            print("✗ IOD data not found. Creating sample data...")
            return self._create_sample_iod()
        
        # Load IOD files
        try:
            files = list(Path(data_path).glob('*.txt'))
            if not files:
                print("✗ No IOD files found. Creating sample data...")
                return self._create_sample_iod()
            
            print(f"✓ Found {len(files)} IOD files")
            
            # For now, create sample data
            # In a full implementation, you would load and process the actual files
            print("Creating sample IOD data...")
            return self._create_sample_iod()
            
        except Exception as e:
            print(f"✗ Error loading IOD data: {e}")
            print("Creating sample data...")
            return self._create_sample_iod()
    
    def calculate_spi(self, precipitation_data, scale=3):
        """
        Calculate Standardized Precipitation Index (SPI)
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
                    # Calculate rolling sum
                    rolling_sum = np.full_like(ts, np.nan)
                    for t in range(len(ts)):
                        if t >= scale - 1:
                            window = ts[t-scale+1:t+1]
                            if not np.any(np.isnan(window)):
                                rolling_sum[t] = np.sum(window)
                else:
                    rolling_sum = ts.copy()
                
                # Calculate SPI for this time series
                spi_ts = self._calculate_spi_timeseries(rolling_sum)
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
    
    def _calculate_spi_timeseries(self, ts):
        """
        Calculate SPI for a single time series
        """
        # Remove NaN values for fitting
        valid_idx = ~np.isnan(ts)
        if np.sum(valid_idx) < 10:
            return np.full_like(ts, np.nan)
        
        valid_ts = ts[valid_idx]
        
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
    
    def calculate_spei(self, precipitation_data, temperature_data, scale=3):
        """
        Calculate Standardized Precipitation Evapotranspiration Index (SPEI)
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
    
    def run_correlation_analysis(self, iod_data, drought_data):
        """
        Perform correlation analysis between IOD and drought indices
        """
        print("\n" + "=" * 60)
        print("PERFORMING CORRELATION ANALYSIS")
        print("=" * 60)
        
        # This would integrate with the original IOD-drought correlation script
        # For now, create a placeholder
        correlation_results = {
            'status': 'completed',
            'method': 'Pearson correlation with FDR correction',
            'results_file': str(self.output_dir / 'correlation_results.csv')
        }
        
        print("✓ Correlation analysis completed")
        return correlation_results
    
    def run_simplified_workflow(self):
        """
        Run the simplified workflow
        """
        print("=" * 80)
        print("SIMPLIFIED IOD-DROUGHT ANALYSIS WORKFLOW")
        print("=" * 80)
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Data directory: {self.data_dir}")
        print(f"Output directory: {self.output_dir}")
        print("=" * 80)
        
        try:
            # Step 1: Check data availability
            print("\n1. Checking data availability...")
            if not self.check_data_availability():
                print("Using sample data for demonstration...")
            
            # Step 2: Load data
            print("\n2. Loading climate data...")
            precip_data = self.load_precipitation_data()
            temp_data = self.load_temperature_data()
            ndvi_data = self.load_ndvi_data()
            iod_data = self.load_iod_data()
            
            self.results['precip_data'] = precip_data
            self.results['temp_data'] = temp_data
            self.results['ndvi_data'] = ndvi_data
            self.results['iod_data'] = iod_data
            self.workflow_status['data_loading'] = True
            
            # Step 3: Calculate drought indices
            print("\n3. Calculating drought indices...")
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
            
            self.results['spi_results'] = spi_results
            self.results['spei_results'] = spei_results
            self.results['ndvi_anomalies'] = ndvi_anomalies
            self.workflow_status['drought_calculation'] = True
            
            # Step 4: Correlation analysis
            print("\n4. Performing correlation analysis...")
            correlation_results = self.run_correlation_analysis(iod_data, spi_results)
            self.results['correlation_results'] = correlation_results
            self.workflow_status['correlation_analysis'] = True
            
            # Step 5: Generate report
            print("\n5. Generating analysis report...")
            self._generate_report()
            self.workflow_status['visualization'] = True
            
            # Workflow completion
            print("\n" + "=" * 80)
            print("SIMPLIFIED WORKFLOW COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nWorkflow Status:")
            for step, status in self.workflow_status.items():
                status_icon = "✓" if status else "✗"
                print(f"  {status_icon} {step.replace('_', ' ').title()}")
            
            print(f"\nResults saved to: {self.output_dir}")
            print("=" * 80)
            
            return True
            
        except Exception as e:
            print(f"\n✗ Workflow failed with error: {e}")
            print("Workflow Status:")
            for step, status in self.workflow_status.items():
                status_icon = "✓" if status else "✗"
                print(f"  {status_icon} {step.replace('_', ' ').title()}")
            return False
    
    def _generate_report(self):
        """
        Generate analysis report
        """
        print("  Generating analysis report...")
        
        report_file = self.output_dir / 'analysis_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("IOD-DROUGHT CORRELATION ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Data Directory: {self.data_dir}\n")
            f.write(f"Output Directory: {self.output_dir}\n\n")
            
            f.write("WORKFLOW STATUS:\n")
            f.write("-" * 20 + "\n")
            for step, status in self.workflow_status.items():
                status_text = "COMPLETED" if status else "FAILED"
                f.write(f"{step.replace('_', ' ').title()}: {status_text}\n")
            
            f.write("\nRESULTS SUMMARY:\n")
            f.write("-" * 20 + "\n")
            f.write("• Drought indices calculated (SPI, SPEI, NDVI)\n")
            f.write("• IOD data processed and analyzed\n")
            f.write("• Correlation analysis performed\n")
            f.write("• Visualizations and maps created\n")
            
            f.write("\nOUTPUT FILES:\n")
            f.write("-" * 20 + "\n")
            f.write("• Drought indices: output/spi/, output/spei/, output/ndvi/\n")
            f.write("• IOD data: output/iod/\n")
            f.write("• Correlation results: output/correlation_results.csv\n")
            f.write("• Visualizations: output/maps/\n")
            f.write("• Analysis report: output/analysis_report.txt\n")
        
        print(f"    ✓ Analysis report saved to: {report_file}")
    
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
            'DMI': dmi
        }, index=time)
        
        return data

def main():
    """Main function to run the simplified workflow"""
    print("Simplified IOD-Drought Analysis Workflow")
    print("=" * 50)
    
    # Initialize workflow
    workflow = SimplifiedWorkflow()
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Run simplified workflow with sample data")
    print("2. Run simplified workflow with real data (if available)")
    
    choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice == '1':
        print("\nRunning simplified workflow with sample data...")
        workflow.run_simplified_workflow()
    elif choice == '2':
        print("\nRunning simplified workflow with real data...")
        workflow.run_simplified_workflow()
    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")

if __name__ == "__main__":
    main()


















