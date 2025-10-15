"""
Basic Drought Analysis Example

This example demonstrates how to perform basic drought analysis
using the drought analysis toolkit.

Author: Drought Analysis Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drought_indices import DroughtIndices, create_sample_data
from data_processing import ClimateDataProcessor
from visualization import DroughtVisualizer
import matplotlib.pyplot as plt


def basic_spi_analysis():
    """
    Basic SPI calculation and visualization example
    """
    print("=" * 50)
    print("BASIC SPI ANALYSIS EXAMPLE")
    print("=" * 50)
    
    # Create sample data
    print("\n1. Creating sample climate data...")
    precip, temp = create_sample_data(
        lon_range=(-20, 60),
        lat_range=(-40, -10),
        time_range=('2000-01-01', '2023-12-31')
    )
    
    print(f"   Precipitation data shape: {precip.shape}")
    print(f"   Temperature data shape: {temp.shape}")
    
    # Initialize drought calculator
    print("\n2. Calculating SPI...")
    drought_calc = DroughtIndices()
    
    # Calculate 3-month SPI
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    print(f"   3-month SPI calculated: {spi_3m.shape}")
    
    # Calculate drought frequency
    print("\n3. Analyzing drought frequency...")
    drought_freq = drought_calc.calculate_drought_frequency(spi_3m, threshold=-1.0)
    print(f"   Drought frequency calculated: {drought_freq.shape}")
    
    # Create visualization
    print("\n4. Creating visualization...")
    visualizer = DroughtVisualizer()
    
    # Create drought frequency map
    fig = visualizer.create_drought_frequency_map(
        drought_freq,
        title="Basic SPI Analysis - Southern Africa",
        threshold=-1.0,
        show=True
    )
    
    print("\n✓ Basic analysis completed!")
    return spi_3m, drought_freq


def multi_scale_analysis():
    """
    Multi-scale drought analysis example
    """
    print("\n" + "=" * 50)
    print("MULTI-SCALE DROUGHT ANALYSIS")
    print("=" * 50)
    
    # Create sample data
    precip, temp = create_sample_data()
    
    # Initialize components
    drought_calc = DroughtIndices()
    visualizer = DroughtVisualizer()
    
    # Calculate SPI for different time scales
    scales = [1, 3, 6, 12]
    spi_data = {}
    
    print("\nCalculating SPI for different time scales...")
    for scale in scales:
        print(f"   - {scale}-month SPI...")
        spi_data[scale] = drought_calc.calculate_spi(precip, scale=scale)
    
    # Calculate drought frequency for each scale
    print("\nCalculating drought frequency...")
    freq_data = {}
    for scale in scales:
        freq_data[scale] = drought_calc.calculate_drought_frequency(
            spi_data[scale], threshold=-1.0
        )
    
    # Create comparison plot
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, scale in enumerate(scales):
        freq_data[scale].plot(ax=axes[i], cmap='Reds', vmin=0, vmax=50)
        axes[i].set_title(f'{scale}-Month SPI - Drought Frequency (%)')
    
    plt.suptitle('Multi-Scale Drought Frequency Comparison', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    print("\n✓ Multi-scale analysis completed!")
    return spi_data, freq_data


def spei_analysis():
    """
    SPEI calculation example
    """
    print("\n" + "=" * 50)
    print("SPEI ANALYSIS EXAMPLE")
    print("=" * 50)
    
    # Create sample data
    precip, temp = create_sample_data()
    
    # Initialize drought calculator
    drought_calc = DroughtIndices()
    
    # Calculate SPEI
    print("\nCalculating SPEI...")
    spei_3m = drought_calc.calculate_spei(precip, temp, scale=3)
    print(f"   3-month SPEI calculated: {spei_3m.shape}")
    
    # Calculate drought frequency
    drought_freq = drought_calc.calculate_drought_frequency(spei_3m, threshold=-1.0)
    
    # Create visualization
    visualizer = DroughtVisualizer()
    fig = visualizer.create_drought_frequency_map(
        drought_freq,
        title="SPEI Analysis - Southern Africa",
        threshold=-1.0,
        show=True
    )
    
    print("\n✓ SPEI analysis completed!")
    return spei_3m, drought_freq


def time_series_analysis():
    """
    Time series analysis example
    """
    print("\n" + "=" * 50)
    print("TIME SERIES ANALYSIS")
    print("=" * 50)
    
    # Create sample data
    precip, temp = create_sample_data()
    
    # Calculate SPI
    drought_calc = DroughtIndices()
    spi_12m = drought_calc.calculate_spi(precip, scale=12)
    
    # Create time series plot for specific location
    visualizer = DroughtVisualizer()
    
    # Cape Town location
    fig = visualizer.create_time_series_plot(
        spi_12m,
        location_name="Cape Town",
        lat=-33.9,
        lon=18.4,
        show=True
    )
    
    print("\n✓ Time series analysis completed!")


def main():
    """
    Run all basic analysis examples
    """
    print("SOUTHERN AFRICA DROUGHT ANALYSIS - BASIC EXAMPLES")
    print("=" * 60)
    
    try:
        # Run basic SPI analysis
        spi_3m, drought_freq = basic_spi_analysis()
        
        # Run multi-scale analysis
        spi_data, freq_data = multi_scale_analysis()
        
        # Run SPEI analysis
        spei_3m, spei_freq = spei_analysis()
        
        # Run time series analysis
        time_series_analysis()
        
        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()







