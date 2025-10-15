"""
Visualization and Mapping Module for Drought Analysis on Lengau Cluster

This module provides functions to create maps and visualizations for
drought frequency and severity analysis in Southern Africa.

Optimized for cluster computing with headless operation.

Author: Drought Analysis Toolkit
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for cluster
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
    Class for creating drought analysis visualizations on cluster
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
    
    def create_drought_frequency_map(self, drought_frequency, title="Drought Frequency Map - Southern Africa",
                                   threshold=-1.0, save_path=None, show=False):
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
            Whether to display the map (False for cluster)
            
        Returns:
        --------
        matplotlib.figure.Figure
            The created figure
        """
        print(f"Creating drought frequency map: {title}")
        
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
            print(f"✓ Map saved to: {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return fig
    
    def create_drought_severity_map(self, drought_severity, title="Drought Severity Map - Southern Africa",
                                  save_path=None, show=False):
        """
        Create a map showing drought severity across Southern Africa
        """
        print(f"Creating drought severity map: {title}")
        
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
            print(f"✓ Map saved to: {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return fig
    
    def create_interactive_map(self, drought_frequency, drought_severity=None,
                             save_path='drought_interactive_map.html'):
        """
        Create an interactive Folium map for drought analysis
        """
        print(f"Creating interactive map: {save_path}")
        
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
        print(f"✓ Interactive map saved to: {save_path}")
        
        return m
    
    def create_composite_map(self, drought_frequency, drought_severity,
                           save_path=None, show=False):
        """
        Create a composite map showing both frequency and severity
        """
        print("Creating composite drought map...")
        
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
            print(f"✓ Composite map saved to: {save_path}")
        
        if show:
            plt.show()
        else:
            plt.close()
        
        return fig


if __name__ == "__main__":
    # Example usage
    print("Testing visualization functions...")
    
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
    
    print("✓ Visualization test completed successfully!")







