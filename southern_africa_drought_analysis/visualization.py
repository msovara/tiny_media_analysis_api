"""
Visualization and Mapping Module for Drought Analysis

This module provides functions to create maps and visualizations for
drought frequency and severity analysis in Southern Africa.

Author: Drought Analysis Toolkit
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import folium
from folium import plugins
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DroughtVisualizer:
    """
    Class for creating drought analysis visualizations
    """
    
    def __init__(self, figsize=(12, 8), dpi=300):
        self.figsize = figsize
        self.dpi = dpi
        
        # Southern Africa bounds
        self.bounds = {
            'lon_min': -20, 'lon_max': 60,
            'lat_min': -40, 'lat_max': -10
        }
        
        # Drought color scheme
        self.drought_colors = {
            'extremely_dry': '#8B0000',      # Dark red
            'severely_dry': '#DC143C',       # Crimson
            'moderately_dry': '#FF6347',     # Tomato
            'mildly_dry': '#FFA500',         # Orange
            'near_normal': '#90EE90',        # Light green
            'mildly_wet': '#32CD32',         # Lime green
            'moderately_wet': '#00CED1',     # Dark turquoise
            'severely_wet': '#4169E1',       # Royal blue
            'extremely_wet': '#000080'       # Navy
        }
        
        # Drought frequency color scheme
        self.frequency_colors = ['#FFFFFF', '#FFF2CC', '#FFE6B3', '#FFD9B3', 
                                '#FFCCB3', '#FFB3B3', '#FF9999', '#FF6666', 
                                '#FF3333', '#CC0000', '#990000']
    
    def create_drought_frequency_map(self, drought_frequency, title="Drought Frequency Map - Southern Africa",
                                   threshold=-1.0, save_path=None, show=True):
        """
        Create a map showing drought frequency across Southern Africa
        
        Parameters:
        -----------
        drought_frequency : xarray.DataArray
            Drought frequency data (percentage)
        title : str
            Map title
        threshold : float
            Drought threshold used for frequency calculation
        save_path : str, optional
            Path to save the map
        show : bool
            Whether to display the map
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        # Create figure with cartopy projection
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        # Set extent for Southern Africa
        ax.set_extent([self.bounds['lon_min'], self.bounds['lon_max'],
                      self.bounds['lat_min'], self.bounds['lat_max']],
                     crs=ccrs.PlateCarree())
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot drought frequency
        im = drought_frequency.plot(ax=ax, transform=ccrs.PlateCarree(),
                                  cmap='Reds', vmin=0, vmax=50,
                                  add_colorbar=False, alpha=0.8)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label(f'Drought Frequency (% of time with SPI < {threshold})', 
                      fontsize=12, fontweight='bold')
        
        # Add gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                         linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        
        # Add title
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Add text box with analysis info
        textstr = f'Analysis Period: {drought_frequency.time.dt.year.min().values}-{drought_frequency.time.dt.year.max().values}\n'
        textstr += f'Drought Threshold: SPI < {threshold}\n'
        textstr += f'Data Source: Sample Climate Data'
        
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Map saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig
    
    def create_drought_severity_map(self, drought_severity, title="Drought Severity Map - Southern Africa",
                                  save_path=None, show=True):
        """
        Create a map showing drought severity across Southern Africa
        
        Parameters:
        -----------
        drought_severity : xarray.DataArray
            Drought severity data (average SPI during drought)
        title : str
            Map title
        save_path : str, optional
            Path to save the map
        show : bool
            Whether to display the map
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        # Create figure with cartopy projection
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        # Set extent for Southern Africa
        ax.set_extent([self.bounds['lon_min'], self.bounds['lon_max'],
                      self.bounds['lat_min'], self.bounds['lat_max']],
                     crs=ccrs.PlateCarree())
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot drought severity
        im = drought_severity.plot(ax=ax, transform=ccrs.PlateCarree(),
                                 cmap='RdYlBu_r', vmin=-3, vmax=0,
                                 add_colorbar=False, alpha=0.8)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Average Drought Severity (SPI during drought periods)', 
                      fontsize=12, fontweight='bold')
        
        # Add gridlines
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                         linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        
        # Add title
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Map saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig
    
    def create_interactive_map(self, drought_frequency, drought_severity=None,
                             save_path='drought_interactive_map.html'):
        """
        Create an interactive Folium map for drought analysis
        
        Parameters:
        -----------
        drought_frequency : xarray.DataArray
            Drought frequency data
        drought_severity : xarray.DataArray, optional
            Drought severity data
        save_path : str
            Path to save the interactive map
            
        Returns:
        --------
        folium.Map
            Interactive map
        """
        # Create base map centered on Southern Africa
        center_lat = (self.bounds['lat_min'] + self.bounds['lat_max']) / 2
        center_lon = (self.bounds['lon_min'] + self.bounds['lon_max']) / 2
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=4,
            tiles='OpenStreetMap'
        )
        
        # Add drought frequency layer
        freq_data = drought_frequency.values
        freq_lats = drought_frequency.lat.values
        freq_lons = drought_frequency.lon.values
        
        # Create frequency heatmap
        freq_heatmap_data = []
        for i, lat in enumerate(freq_lats):
            for j, lon in enumerate(freq_lons):
                if not np.isnan(freq_data[i, j]):
                    freq_heatmap_data.append([lat, lon, freq_data[i, j]])
        
        # Add frequency heatmap layer
        plugins.HeatMap(
            freq_heatmap_data,
            name='Drought Frequency',
            min_opacity=0.4,
            max_zoom=18,
            radius=15,
            blur=15,
            gradient={0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: 'red'}
        ).add_to(m)
        
        # Add severity layer if provided
        if drought_severity is not None:
            sev_data = drought_severity.values
            sev_lats = drought_severity.lat.values
            sev_lons = drought_severity.lon.values
            
            sev_heatmap_data = []
            for i, lat in enumerate(sev_lats):
                for j, lon in enumerate(sev_lons):
                    if not np.isnan(sev_data[i, j]):
                        sev_heatmap_data.append([lat, lon, sev_data[i, j]])
            
            plugins.HeatMap(
                sev_heatmap_data,
                name='Drought Severity',
                min_opacity=0.4,
                max_zoom=18,
                radius=15,
                blur=15,
                gradient={0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: 'red'}
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add title
        title_html = '''
        <h3 align="center" style="font-size:20px"><b>Southern Africa Drought Analysis</b></h3>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        # Save map
        m.save(save_path)
        print(f"Interactive map saved to: {save_path}")
        
        return m
    
    def create_time_series_plot(self, spi_data, location_name="Sample Location",
                              lat=None, lon=None, save_path=None, show=True):
        """
        Create a time series plot of SPI values
        
        Parameters:
        -----------
        spi_data : xarray.DataArray
            SPI time series data
        location_name : str
            Name of the location
        lat : float, optional
            Latitude of the location
        lon : float, optional
            Longitude of the location
        save_path : str, optional
            Path to save the plot
        show : bool
            Whether to display the plot
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=(15, 6), dpi=self.dpi)
        
        # Extract time series for specific location or average
        if lat is not None and lon is not None:
            # Find nearest grid point
            lat_idx = np.argmin(np.abs(spi_data.lat - lat))
            lon_idx = np.argmin(np.abs(spi_data.lon - lon))
            time_series = spi_data[:, lat_idx, lon_idx]
            title = f"SPI Time Series - {location_name} ({lat:.2f}°N, {lon:.2f}°E)"
        else:
            # Use spatial average
            time_series = spi_data.mean(dim=['lat', 'lon'])
            title = f"SPI Time Series - {location_name} (Spatial Average)"
        
        # Plot time series
        ax.plot(time_series.time, time_series, linewidth=1.5, color='blue', alpha=0.7)
        
        # Add drought threshold lines
        ax.axhline(y=-1.0, color='orange', linestyle='--', alpha=0.7, label='Moderate Drought')
        ax.axhline(y=-1.5, color='red', linestyle='--', alpha=0.7, label='Severe Drought')
        ax.axhline(y=-2.0, color='darkred', linestyle='--', alpha=0.7, label='Extreme Drought')
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Fill areas for drought periods
        ax.fill_between(time_series.time, time_series, -1.0, 
                       where=(time_series < -1.0), color='red', alpha=0.3, 
                       label='Drought Periods')
        
        # Formatting
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('SPI', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Time series plot saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig
    
    def create_drought_statistics_plot(self, drought_frequency, drought_severity,
                                     save_path=None, show=True):
        """
        Create statistical plots for drought analysis
        
        Parameters:
        -----------
        drought_frequency : xarray.DataArray
            Drought frequency data
        drought_severity : xarray.DataArray
            Drought severity data
        save_path : str, optional
            Path to save the plot
        show : bool
            Whether to display the plot
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10), dpi=self.dpi)
        
        # 1. Frequency histogram
        freq_data = drought_frequency.values.flatten()
        freq_data = freq_data[~np.isnan(freq_data)]
        
        ax1.hist(freq_data, bins=20, alpha=0.7, color='red', edgecolor='black')
        ax1.set_xlabel('Drought Frequency (%)')
        ax1.set_ylabel('Number of Grid Points')
        ax1.set_title('Distribution of Drought Frequency')
        ax1.grid(True, alpha=0.3)
        
        # 2. Severity histogram
        sev_data = drought_severity.values.flatten()
        sev_data = sev_data[~np.isnan(sev_data)]
        
        ax2.hist(sev_data, bins=20, alpha=0.7, color='blue', edgecolor='black')
        ax2.set_xlabel('Average Drought Severity (SPI)')
        ax2.set_ylabel('Number of Grid Points')
        ax2.set_title('Distribution of Drought Severity')
        ax2.grid(True, alpha=0.3)
        
        # 3. Frequency vs Severity scatter plot
        valid_mask = ~(np.isnan(freq_data) | np.isnan(sev_data))
        ax3.scatter(freq_data[valid_mask], sev_data[valid_mask], alpha=0.6, s=20)
        ax3.set_xlabel('Drought Frequency (%)')
        ax3.set_ylabel('Average Drought Severity (SPI)')
        ax3.set_title('Drought Frequency vs Severity')
        ax3.grid(True, alpha=0.3)
        
        # 4. Box plot of frequency by severity categories
        # Create severity categories
        sev_categories = pd.cut(sev_data, bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        freq_by_sev = pd.DataFrame({'Frequency': freq_data[valid_mask], 'Severity': sev_categories[valid_mask]})
        
        freq_by_sev.boxplot(column='Frequency', by='Severity', ax=ax4)
        ax4.set_xlabel('Drought Severity Category')
        ax4.set_ylabel('Drought Frequency (%)')
        ax4.set_title('Drought Frequency by Severity Category')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('Drought Analysis Statistics', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Statistics plot saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig
    
    def create_composite_map(self, drought_frequency, drought_severity,
                           save_path=None, show=True):
        """
        Create a composite map showing both frequency and severity
        
        Parameters:
        -----------
        drought_frequency : xarray.DataArray
            Drought frequency data
        drought_severity : xarray.DataArray
            Drought severity data
        save_path : str, optional
            Path to save the map
        show : bool
            Whether to display the map
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), dpi=self.dpi,
                                      subplot_kw={'projection': ccrs.PlateCarree()})
        
        # Set extent for both subplots
        for ax in [ax1, ax2]:
            ax.set_extent([self.bounds['lon_min'], self.bounds['lon_max'],
                          self.bounds['lat_min'], self.bounds['lat_max']],
                         crs=ccrs.PlateCarree())
            ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
            ax.add_feature(cfeature.BORDERS, linewidth=0.3)
            ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
            ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot frequency
        im1 = drought_frequency.plot(ax=ax1, transform=ccrs.PlateCarree(),
                                   cmap='Reds', vmin=0, vmax=50,
                                   add_colorbar=False, alpha=0.8)
        ax1.set_title('Drought Frequency (%)', fontsize=14, fontweight='bold')
        
        # Plot severity
        im2 = drought_severity.plot(ax=ax2, transform=ccrs.PlateCarree(),
                                  cmap='RdYlBu_r', vmin=-3, vmax=0,
                                  add_colorbar=False, alpha=0.8)
        ax2.set_title('Drought Severity (SPI)', fontsize=14, fontweight='bold')
        
        # Add colorbars
        cbar1 = plt.colorbar(im1, ax=ax1, orientation='horizontal', 
                            pad=0.05, shrink=0.8, aspect=30)
        cbar1.set_label('Frequency (%)', fontsize=10)
        
        cbar2 = plt.colorbar(im2, ax=ax2, orientation='horizontal', 
                            pad=0.05, shrink=0.8, aspect=30)
        cbar2.set_label('Severity (SPI)', fontsize=10)
        
        plt.suptitle('Southern Africa Drought Analysis - Composite Map', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Composite map saved to: {save_path}")
        
        if show:
            plt.show()
        
        return fig


if __name__ == "__main__":
    # Example usage
    print("Creating sample visualizations...")
    
    # Create sample data
    from drought_indices import create_sample_data, DroughtIndices
    
    precip, temp = create_sample_data()
    drought_calc = DroughtIndices()
    
    # Calculate drought indices
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    drought_freq = drought_calc.calculate_drought_frequency(spi_3m, threshold=-1.0)
    drought_sev = drought_calc.calculate_drought_severity(spi_3m, threshold=-1.0)
    
    # Create visualizations
    visualizer = DroughtVisualizer()
    
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # Generate maps
    visualizer.create_drought_frequency_map(
        drought_freq, 
        save_path=output_dir / 'drought_frequency_map.png'
    )
    
    visualizer.create_drought_severity_map(
        drought_sev,
        save_path=output_dir / 'drought_severity_map.png'
    )
    
    visualizer.create_composite_map(
        drought_freq, drought_sev,
        save_path=output_dir / 'composite_drought_map.png'
    )
    
    visualizer.create_interactive_map(
        drought_freq, drought_sev,
        save_path=output_dir / 'interactive_drought_map.html'
    )
    
    print("Sample visualizations created successfully!")







