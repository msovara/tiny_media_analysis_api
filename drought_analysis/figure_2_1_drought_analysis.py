#!/usr/bin/env python3
"""
Figure 2.1: Southern Africa Drought Frequency/Severity Analysis for Lengau Cluster

This script creates a comprehensive drought analysis map showing the frequency
and severity of drought events across Southern Africa using historical drought
index data (SPI, SPEI).

Optimized for cluster computing with parallel processing and job submission.

Author: Drought Analysis Toolkit
Date: 2024
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for cluster
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
import warnings
import os
import sys
from datetime import datetime
warnings.filterwarnings('ignore')

# Import our custom modules
from drought_indices import DroughtIndices, create_sample_data
from visualization import DroughtVisualizer


def main():
    """
    Main function to create Figure 2.1: Drought frequency/severity map
    """
    print("=" * 80)
    print("FIGURE 2.1: SOUTHERN AFRICA DROUGHT ANALYSIS - LENGAU CLUSTER")
    print("=" * 80)
    print(f"Job started at: {datetime.now()}")
    print(f"Running on node: {os.uname().nodename}")
    print(f"Python version: {sys.version}")
    
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    print("\n1. Initializing analysis components...")
    drought_calc = DroughtIndices()
    
    # Set chunk size for cluster processing
    chunk_size = {'time': 100, 'lat': 20, 'lon': 20}
    visualizer = DroughtVisualizer(figsize=(14, 10), dpi=300)
    
    # Load or create climate data
    print("\n2. Preparing climate data...")
    try:
        # Create sample data with cluster optimization
        precip, temp = create_sample_data(
            lon_range=(-20, 60),
            lat_range=(-40, -10),
            time_range=('2000-01-01', '2023-12-31'),
            chunk_size=chunk_size
        )
        print("✓ Sample climate data created with cluster optimization")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        return 1
    
    # Calculate drought indices
    print("\n3. Calculating drought indices...")
    
    # Calculate SPI for different time scales
    scales = [3, 6, 12]
    spi_data = {}
    
    for scale in scales:
        print(f"   - Calculating {scale}-month SPI...")
        spi_data[scale] = drought_calc.calculate_spi(
            precip, scale=scale, chunk_size=chunk_size
        )
    
    # Calculate SPEI (if temperature data available)
    print("   - Calculating 3-month SPEI...")
    spei_3m = drought_calc.calculate_spei(
        precip, temp, scale=3, chunk_size=chunk_size
    )
    
    print("✓ Drought indices calculated successfully")
    
    # Calculate drought frequency and severity
    print("\n4. Analyzing drought characteristics...")
    
    # Define drought thresholds
    thresholds = {
        'moderate': -1.0,
        'severe': -1.5,
        'extreme': -2.0
    }
    
    # Calculate frequency and severity for different thresholds
    drought_metrics = {}
    
    for severity, threshold in thresholds.items():
        print(f"   - Analyzing {severity} drought (threshold: {threshold})...")
        
        # Use 12-month SPI for main analysis
        spi_12m = spi_data[12]
        
        # Frequency analysis
        freq = drought_calc.calculate_drought_frequency(spi_12m, threshold=threshold)
        
        # Severity analysis
        sev = drought_calc.calculate_drought_severity(spi_12m, threshold=threshold)
        
        drought_metrics[severity] = {
            'frequency': freq,
            'severity': sev
        }
    
    print("✓ Drought analysis completed")
    
    # Create visualizations
    print("\n5. Creating visualizations...")
    
    # Main Figure 2.1: Comprehensive drought frequency map
    print("   - Creating Figure 2.1: Main drought frequency map...")
    main_figure = visualizer.create_drought_frequency_map(
        drought_metrics['moderate']['frequency'],
        title="Figure 2.1: Southern Africa Drought Frequency Analysis\n(12-month SPI, Moderate Drought Threshold: -1.0)",
        threshold=-1.0,
        save_path=output_dir / 'figure_2_1_main_drought_frequency.png',
        show=False
    )
    
    # Additional analysis maps
    print("   - Creating multi-scale drought frequency comparison...")
    create_multi_scale_comparison(spi_data, visualizer, output_dir)
    
    print("   - Creating drought severity analysis...")
    create_severity_analysis(drought_metrics, visualizer, output_dir)
    
    print("   - Creating composite map...")
    visualizer.create_composite_map(
        drought_metrics['moderate']['frequency'],
        drought_metrics['moderate']['severity'],
        save_path=output_dir / 'figure_2_1_composite_map.png',
        show=False
    )
    
    print("   - Creating interactive map...")
    visualizer.create_interactive_map(
        drought_metrics['moderate']['frequency'],
        drought_metrics['moderate']['severity'],
        save_path=output_dir / 'figure_2_1_interactive_map.html'
    )
    
    # Generate summary statistics
    print("\n6. Generating summary statistics...")
    generate_summary_statistics(drought_metrics, output_dir)
    
    # Create time series analysis
    print("\n7. Creating time series analysis...")
    create_time_series_analysis(spi_data[12], visualizer, output_dir)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"Job completed at: {datetime.now()}")
    print(f"\nOutput files saved to: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob('*')):
        print(f"  - {file.name}")
    
    print(f"\nMain Figure 2.1: {output_dir / 'figure_2_1_main_drought_frequency.png'}")
    print(f"Interactive Map: {output_dir / 'figure_2_1_interactive_map.html'}")
    
    return 0


def create_multi_scale_comparison(spi_data, visualizer, output_dir):
    """
    Create comparison maps for different time scales
    """
    fig, axes = plt.subplots(1, 3, figsize=(20, 6), dpi=300,
                            subplot_kw={'projection': ccrs.PlateCarree()})
    
    scales = [3, 6, 12]
    titles = ['3-Month SPI', '6-Month SPI', '12-Month SPI']
    
    for i, (scale, title) in enumerate(zip(scales, titles)):
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
        
        # Calculate and plot drought frequency
        freq_data = visualizer.drought_calc.calculate_drought_frequency(
            spi_data[scale], threshold=-1.0
        )
        
        im = freq_data.plot(ax=ax, transform=ccrs.PlateCarree(),
                          cmap='Reds', vmin=0, vmax=50,
                          add_colorbar=False, alpha=0.8)
        
        ax.set_title(f'{title} - Drought Frequency (%)', fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Frequency (%)', fontsize=10)
    
    # Add overall title
    plt.suptitle('Multi-Scale Drought Frequency Comparison\n(Moderate Drought Threshold: SPI < -1.0)', 
                fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure_2_1_multi_scale_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_severity_analysis(drought_metrics, visualizer, output_dir):
    """
    Create drought severity analysis maps
    """
    fig, axes = plt.subplots(1, 3, figsize=(20, 6), dpi=300,
                            subplot_kw={'projection': ccrs.PlateCarree()})
    
    severities = ['moderate', 'severe', 'extreme']
    titles = ['Moderate Drought\n(SPI < -1.0)', 'Severe Drought\n(SPI < -1.5)', 'Extreme Drought\n(SPI < -2.0)']
    
    for i, (severity, title) in enumerate(zip(severities, titles)):
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
        
        # Plot drought frequency
        freq_data = drought_metrics[severity]['frequency']
        im = freq_data.plot(ax=ax, transform=ccrs.PlateCarree(),
                          cmap='Reds', vmin=0, vmax=30,
                          add_colorbar=False, alpha=0.8)
        
        ax.set_title(title, fontsize=12, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, orientation='horizontal', 
                           pad=0.05, shrink=0.8, aspect=30)
        cbar.set_label('Frequency (%)', fontsize=10)
    
    plt.suptitle('Drought Frequency by Severity Level\n(12-Month SPI)', 
                fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure_2_1_severity_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()


def generate_summary_statistics(drought_metrics, output_dir):
    """
    Generate and save summary statistics
    """
    stats_data = []
    
    for severity, metrics in drought_metrics.items():
        # Calculate statistics
        freq_values = metrics['frequency'].values.flatten()
        freq_values = freq_values[~np.isnan(freq_values)]
        
        stats = {
            'Severity': severity,
            'Mean_Frequency': np.mean(freq_values),
            'Median_Frequency': np.median(freq_values),
            'Std_Frequency': np.std(freq_values),
            'Min_Frequency': np.min(freq_values),
            'Max_Frequency': np.max(freq_values),
            'Grid_Points': len(freq_values)
        }
        stats_data.append(stats)
    
    # Create DataFrame and save
    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(output_dir / 'figure_2_1_summary_statistics.csv', index=False)
    
    # Create summary plot
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
    
    # Bar plot of mean frequencies
    severity_order = ['moderate', 'severe', 'extreme']
    means = [stats_df[stats_df['Severity'] == sev]['Mean_Frequency'].iloc[0] 
             for sev in severity_order]
    
    bars = ax.bar(severity_order, means, alpha=0.8, color=['red', 'orange', 'darkred'])
    ax.set_xlabel('Drought Severity Level', fontsize=12)
    ax.set_ylabel('Mean Drought Frequency (%)', fontsize=12)
    ax.set_title('Mean Drought Frequency by Severity Level', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{mean:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'figure_2_1_summary_statistics.png', 
                dpi=300, bbox_inches='tight')
    plt.close()


def create_time_series_analysis(spi_data, visualizer, output_dir):
    """
    Create time series analysis for key locations
    """
    # Select key locations in Southern Africa
    locations = [
        {'name': 'Cape Town', 'lat': -33.9, 'lon': 18.4},
        {'name': 'Johannesburg', 'lat': -26.2, 'lon': 28.0},
        {'name': 'Durban', 'lat': -29.9, 'lon': 31.0},
        {'name': 'Windhoek', 'lat': -22.6, 'lon': 17.1},
        {'name': 'Gaborone', 'lat': -24.7, 'lon': 25.9}
    ]
    
    fig, axes = plt.subplots(len(locations), 1, figsize=(15, 3*len(locations)), dpi=300)
    if len(locations) == 1:
        axes = [axes]
    
    for i, location in enumerate(locations):
        # Find nearest grid point
        lat_idx = np.argmin(np.abs(spi_data.lat - location['lat']))
        lon_idx = np.argmin(np.abs(spi_data.lon - location['lon']))
        time_series = spi_data[:, lat_idx, lon_idx]
        
        # Plot time series
        axes[i].plot(time_series.time, time_series, linewidth=1.5, color='blue', alpha=0.7)
        
        # Add drought threshold lines
        axes[i].axhline(y=-1.0, color='orange', linestyle='--', alpha=0.7, label='Moderate Drought')
        axes[i].axhline(y=-1.5, color='red', linestyle='--', alpha=0.7, label='Severe Drought')
        axes[i].axhline(y=-2.0, color='darkred', linestyle='--', alpha=0.7, label='Extreme Drought')
        axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Fill areas for drought periods
        axes[i].fill_between(time_series.time, time_series, -1.0, 
                           where=(time_series < -1.0), color='red', alpha=0.3, 
                           label='Drought Periods')
        
        # Formatting
        axes[i].set_ylabel('SPI', fontsize=10)
        axes[i].set_title(f"SPI Time Series - {location['name']} ({location['lat']:.1f}°N, {location['lon']:.1f}°E)", 
                         fontsize=12, fontweight='bold')
        axes[i].legend(loc='upper right', fontsize=8)
        axes[i].grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Time', fontsize=12)
    plt.suptitle('SPI Time Series for Key Southern Africa Locations', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'figure_2_1_time_series_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)







