"""
Advanced Mapping and Visualization Examples

This example demonstrates advanced mapping and visualization techniques
for drought analysis in Southern Africa.

Author: Drought Analysis Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import folium
from folium import plugins
from pathlib import Path

from drought_indices import DroughtIndices, create_sample_data
from visualization import DroughtVisualizer


def create_advanced_drought_map():
    """
    Create an advanced drought map with multiple layers
    """
    print("=" * 50)
    print("ADVANCED DROUGHT MAPPING")
    print("=" * 50)
    
    # Create sample data
    precip, temp = create_sample_data()
    
    # Calculate drought indices
    drought_calc = DroughtIndices()
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    spi_6m = drought_calc.calculate_spi(precip, scale=6)
    spi_12m = drought_calc.calculate_spi(precip, scale=12)
    
    # Calculate different drought metrics
    freq_moderate = drought_calc.calculate_drought_frequency(spi_12m, threshold=-1.0)
    freq_severe = drought_calc.calculate_drought_frequency(spi_12m, threshold=-1.5)
    freq_extreme = drought_calc.calculate_drought_frequency(spi_12m, threshold=-2.0)
    
    severity_moderate = drought_calc.calculate_drought_severity(spi_12m, threshold=-1.0)
    
    # Create visualizer
    visualizer = DroughtVisualizer(figsize=(16, 12))
    
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # 1. Multi-threshold comparison
    print("\n1. Creating multi-threshold comparison...")
    fig, axes = plt.subplots(1, 3, figsize=(20, 6), dpi=300,
                            subplot_kw={'projection': visualizer.projection})
    
    thresholds = [
        (freq_moderate, 'Moderate Drought\n(SPI < -1.0)', 'Reds'),
        (freq_severe, 'Severe Drought\n(SPI < -1.5)', 'Oranges'),
        (freq_extreme, 'Extreme Drought\n(SPI < -2.0)', 'Purples')
    ]
    
    for i, (freq_data, title, cmap) in enumerate(thresholds):
        ax = axes[i]
        
        # Set extent
        ax.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                      visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                     crs=ccrs.PlateCarree())
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot data
        im = freq_data.plot(ax=ax, transform=ccrs.PlateCarree(),
                          cmap=cmap, vmin=0, vmax=30,
                          add_colorbar=False, alpha=0.8)
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Frequency (%)', fontsize=10)
    
    plt.suptitle('Drought Frequency by Severity Level', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'advanced_multi_threshold_map.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Composite severity-frequency map
    print("\n2. Creating composite severity-frequency map...")
    create_composite_severity_frequency_map(freq_moderate, severity_moderate, visualizer, output_dir)
    
    # 3. Interactive map with multiple layers
    print("\n3. Creating interactive multi-layer map...")
    create_interactive_multi_layer_map(freq_moderate, freq_severe, freq_extreme, 
                                     severity_moderate, output_dir)
    
    # 4. Statistical analysis maps
    print("\n4. Creating statistical analysis maps...")
    create_statistical_analysis_maps(spi_3m, spi_6m, spi_12m, visualizer, output_dir)
    
    print("\n✓ Advanced mapping completed!")


def create_composite_severity_frequency_map(frequency, severity, visualizer, output_dir):
    """
    Create a composite map showing both frequency and severity
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8), dpi=300,
                                  subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Frequency map
    ax1.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                   visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                  crs=ccrs.PlateCarree())
    ax1.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax1.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax1.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
    ax1.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
    
    im1 = frequency.plot(ax=ax1, transform=ccrs.PlateCarree(),
                        cmap='Reds', vmin=0, vmax=50,
                        add_colorbar=False, alpha=0.8)
    ax1.set_title('Drought Frequency (%)', fontsize=14, fontweight='bold')
    
    cbar1 = plt.colorbar(im1, ax=ax1, orientation='horizontal', 
                        pad=0.05, shrink=0.8, aspect=30)
    cbar1.set_label('Frequency (%)', fontsize=12)
    
    # Severity map
    ax2.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                   visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                  crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax2.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax2.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
    ax2.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
    
    im2 = severity.plot(ax=ax2, transform=ccrs.PlateCarree(),
                       cmap='RdYlBu_r', vmin=-3, vmax=0,
                       add_colorbar=False, alpha=0.8)
    ax2.set_title('Drought Severity (SPI)', fontsize=14, fontweight='bold')
    
    cbar2 = plt.colorbar(im2, ax=ax2, orientation='horizontal', 
                        pad=0.05, shrink=0.8, aspect=30)
    cbar2.set_label('Severity (SPI)', fontsize=12)
    
    plt.suptitle('Composite Drought Analysis: Frequency vs Severity', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'composite_severity_frequency_map.png', 
                dpi=300, bbox_inches='tight')
    plt.show()


def create_interactive_multi_layer_map(freq_moderate, freq_severe, freq_extreme, 
                                     severity, output_dir):
    """
    Create an interactive map with multiple drought layers
    """
    # Create base map
    center_lat = -25
    center_lon = 20
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=4,
        tiles='OpenStreetMap'
    )
    
    # Add different drought layers
    layers = [
        (freq_moderate, 'Moderate Drought Frequency', 'red'),
        (freq_severe, 'Severe Drought Frequency', 'orange'),
        (freq_extreme, 'Extreme Drought Frequency', 'purple'),
        (severity, 'Drought Severity', 'blue')
    ]
    
    for data, name, color in layers:
        # Convert data to heatmap format
        heatmap_data = []
        values = data.values
        lats = data.lat.values
        lons = data.lon.values
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                if not np.isnan(values[i, j]):
                    heatmap_data.append([lat, lon, values[i, j]])
        
        # Add heatmap layer
        plugins.HeatMap(
            heatmap_data,
            name=name,
            min_opacity=0.4,
            max_zoom=18,
            radius=15,
            blur=15,
            gradient={0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: color}
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add title
    title_html = '''
    <h3 align="center" style="font-size:20px"><b>Advanced Drought Analysis - Southern Africa</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    m.save(output_dir / 'advanced_interactive_map.html')
    print(f"   Interactive map saved to: {output_dir / 'advanced_interactive_map.html'}")


def create_statistical_analysis_maps(spi_3m, spi_6m, spi_12m, visualizer, output_dir):
    """
    Create statistical analysis maps
    """
    # Calculate statistics
    stats_3m = spi_3m.mean(dim='time')
    stats_6m = spi_6m.mean(dim='time')
    stats_12m = spi_12m.mean(dim='time')
    
    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300,
                            subplot_kw={'projection': visualizer.projection})
    
    # Mean SPI maps
    datasets = [
        (stats_3m, '3-Month SPI Mean'),
        (stats_6m, '6-Month SPI Mean'),
        (stats_12m, '12-Month SPI Mean')
    ]
    
    for i, (data, title) in enumerate(datasets):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        
        ax.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                      visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                     crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        im = data.plot(ax=ax, transform=ccrs.PlateCarree(),
                      cmap='RdYlBu', vmin=-2, vmax=2,
                      add_colorbar=False, alpha=0.8)
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('SPI', fontsize=10)
    
    # Standard deviation map
    ax = axes[1, 1]
    std_data = spi_12m.std(dim='time')
    
    ax.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                  visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                 crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
    ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
    
    im = std_data.plot(ax=ax, transform=ccrs.PlateCarree(),
                      cmap='viridis', vmin=0, vmax=2,
                      add_colorbar=False, alpha=0.8)
    
    ax.set_title('12-Month SPI Standard Deviation', fontsize=12, fontweight='bold')
    
    cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                       pad=0.05, shrink=0.8, aspect=30)
    cbar.set_label('Standard Deviation', fontsize=10)
    
    plt.suptitle('Statistical Analysis of SPI Values', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'statistical_analysis_maps.png', 
                dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """
    Run advanced mapping examples
    """
    print("ADVANCED DROUGHT MAPPING EXAMPLES")
    print("=" * 60)
    
    try:
        create_advanced_drought_map()
        
        print("\n" + "=" * 60)
        print("ADVANCED MAPPING EXAMPLES COMPLETED!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running advanced examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
