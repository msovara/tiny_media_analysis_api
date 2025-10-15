"""
Figure 2.1: Southern Africa Drought Frequency/Severity Analysis

This script creates a comprehensive drought analysis map showing the frequency
and severity of drought events across Southern Africa using historical drought
index data (SPI, SPEI).

Author: Drought Analysis Toolkit
Date: 2024
"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from drought_indices import DroughtIndices, create_sample_data
from data_processing import ClimateDataProcessor
from visualization import DroughtVisualizer


def main():
    """
    Main function to create Figure 2.1: Drought frequency/severity map
    """
    print("=" * 60)
    print("FIGURE 2.1: SOUTHERN AFRICA DROUGHT ANALYSIS")
    print("=" * 60)
    
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    print("\n1. Initializing analysis components...")
    drought_calc = DroughtIndices()
    data_processor = ClimateDataProcessor()
    visualizer = DroughtVisualizer(figsize=(14, 10), dpi=300)
    
    # Load or create climate data
    print("\n2. Preparing climate data...")
    try:
        # Try to load real data if available
        precip, temp = data_processor.prepare_drought_analysis_data(
            start_date='2000-01-01',
            end_date='2023-12-31'
        )
        print("✓ Climate data loaded successfully")
    except Exception as e:
        print(f"⚠ Using sample data: {e}")
        # Create sample data for demonstration
        precip, temp = create_sample_data(
            lon_range=(-20, 60),
            lat_range=(-40, -10),
            time_range=('2000-01-01', '2023-12-31')
        )
        print("✓ Sample climate data created")
    
    # Calculate drought indices
    print("\n3. Calculating drought indices...")
    
    # Calculate SPI for different time scales
    print("   - Calculating 3-month SPI...")
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    
    print("   - Calculating 6-month SPI...")
    spi_6m = drought_calc.calculate_spi(precip, scale=6)
    
    print("   - Calculating 12-month SPI...")
    spi_12m = drought_calc.calculate_spi(precip, scale=12)
    
    # Calculate SPEI (if temperature data available)
    print("   - Calculating 3-month SPEI...")
    spei_3m = drought_calc.calculate_spei(precip, temp, scale=3)
    
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
        
        # Frequency analysis
        freq_3m = drought_calc.calculate_drought_frequency(spi_3m, threshold=threshold)
        freq_6m = drought_calc.calculate_drought_frequency(spi_6m, threshold=threshold)
        freq_12m = drought_calc.calculate_drought_frequency(spi_12m, threshold=threshold)
        
        # Severity analysis
        sev_3m = drought_calc.calculate_drought_severity(spi_3m, threshold=threshold)
        sev_6m = drought_calc.calculate_drought_severity(spi_6m, threshold=threshold)
        sev_12m = drought_calc.calculate_drought_severity(spi_12m, threshold=threshold)
        
        drought_metrics[severity] = {
            'frequency': {'3m': freq_3m, '6m': freq_6m, '12m': freq_12m},
            'severity': {'3m': sev_3m, '6m': sev_6m, '12m': sev_12m}
        }
    
    print("✓ Drought analysis completed")
    
    # Create visualizations
    print("\n5. Creating visualizations...")
    
    # Main Figure 2.1: Comprehensive drought frequency map
    print("   - Creating Figure 2.1: Main drought frequency map...")
    main_figure = visualizer.create_drought_frequency_map(
        drought_metrics['moderate']['frequency']['12m'],
        title="Figure 2.1: Southern Africa Drought Frequency Analysis\n(12-month SPI, Moderate Drought Threshold: -1.0)",
        threshold=-1.0,
        save_path=output_dir / 'figure_2_1_main_drought_frequency.png',
        show=False
    )
    
    # Additional analysis maps
    print("   - Creating multi-scale drought frequency comparison...")
    create_multi_scale_comparison(drought_metrics, visualizer, output_dir)
    
    print("   - Creating drought severity analysis...")
    create_severity_analysis(drought_metrics, visualizer, output_dir)
    
    print("   - Creating interactive map...")
    visualizer.create_interactive_map(
        drought_metrics['moderate']['frequency']['12m'],
        drought_metrics['moderate']['severity']['12m'],
        save_path=output_dir / 'figure_2_1_interactive_map.html'
    )
    
    # Generate summary statistics
    print("\n6. Generating summary statistics...")
    generate_summary_statistics(drought_metrics, output_dir)
    
    # Create time series analysis
    print("\n7. Creating time series analysis...")
    create_time_series_analysis(spi_12m, visualizer, output_dir)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print(f"\nOutput files saved to: {output_dir.absolute()}")
    print("\nGenerated files:")
    for file in output_dir.glob('*'):
        print(f"  - {file.name}")
    
    print(f"\nMain Figure 2.1: {output_dir / 'figure_2_1_main_drought_frequency.png'}")
    print(f"Interactive Map: {output_dir / 'figure_2_1_interactive_map.html'}")


def create_multi_scale_comparison(drought_metrics, visualizer, output_dir):
    """
    Create comparison maps for different time scales
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=300,
                            subplot_kw={'projection': visualizer.projection})
    
    scales = ['3m', '6m', '12m']
    titles = ['3-Month SPI', '6-Month SPI', '12-Month SPI']
    
    for i, (scale, title) in enumerate(zip(scales, titles)):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        
        # Set extent
        ax.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                      visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                     crs=visualizer.projection)
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot drought frequency
        freq_data = drought_metrics['moderate']['frequency'][scale]
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
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=300,
                            subplot_kw={'projection': visualizer.projection})
    
    severities = ['moderate', 'severe', 'extreme']
    titles = ['Moderate Drought\n(SPI < -1.0)', 'Severe Drought\n(SPI < -1.5)', 'Extreme Drought\n(SPI < -2.0)']
    
    for i, (severity, title) in enumerate(zip(severities, titles)):
        ax = axes[i]
        
        # Set extent
        ax.set_extent([visualizer.bounds['lon_min'], visualizer.bounds['lon_max'],
                      visualizer.bounds['lat_min'], visualizer.bounds['lat_max']],
                     crs=visualizer.projection)
        
        # Add map features
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
        ax.add_feature(cfeature.LAND, color='lightgray', alpha=0.2)
        
        # Plot drought frequency
        freq_data = drought_metrics[severity]['frequency']['12m']
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
        for scale, freq_data in metrics['frequency'].items():
            # Calculate statistics
            freq_values = freq_data.values.flatten()
            freq_values = freq_values[~np.isnan(freq_values)]
            
            stats = {
                'Severity': severity,
                'Time_Scale': scale,
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
    scale_order = ['3m', '6m', '12m']
    
    x_pos = np.arange(len(severity_order))
    width = 0.25
    
    for i, scale in enumerate(scale_order):
        means = [stats_df[(stats_df['Severity'] == sev) & 
                         (stats_df['Time_Scale'] == scale)]['Mean_Frequency'].iloc[0] 
                for sev in severity_order]
        
        ax.bar(x_pos + i * width, means, width, label=f'{scale} SPI', alpha=0.8)
    
    ax.set_xlabel('Drought Severity Level', fontsize=12)
    ax.set_ylabel('Mean Drought Frequency (%)', fontsize=12)
    ax.set_title('Mean Drought Frequency by Severity and Time Scale', fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos + width)
    ax.set_xticklabels([s.title() for s in severity_order])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
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
        visualizer.create_time_series_plot(
            spi_data, 
            location_name=location['name'],
            lat=location['lat'],
            lon=location['lon'],
            save_path=None,
            show=False
        )
        
        # Move the plot to subplot
        fig_temp = plt.gcf()
        ax_temp = fig_temp.gca()
        
        # Copy plot to subplot
        axes[i].plot(ax_temp.lines[0].get_xdata(), ax_temp.lines[0].get_ydata(), 
                    linewidth=1.5, color='blue', alpha=0.7)
        
        # Add threshold lines
        axes[i].axhline(y=-1.0, color='orange', linestyle='--', alpha=0.7)
        axes[i].axhline(y=-1.5, color='red', linestyle='--', alpha=0.7)
        axes[i].axhline(y=-2.0, color='darkred', linestyle='--', alpha=0.7)
        axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        axes[i].set_title(f"SPI Time Series - {location['name']}", fontsize=12, fontweight='bold')
        axes[i].set_ylabel('SPI', fontsize=10)
        axes[i].grid(True, alpha=0.3)
        
        plt.close(fig_temp)
    
    axes[-1].set_xlabel('Time', fontsize=12)
    plt.suptitle('SPI Time Series for Key Southern Africa Locations', 
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'figure_2_1_time_series_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
