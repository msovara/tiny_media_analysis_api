#!/usr/bin/env python3
"""
Quick Test Script for Drought Analysis on Lengau

This script provides a quick test of the drought analysis functionality
without running the full analysis.

Author: Drought Analysis Toolkit
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from drought_indices import DroughtIndices, create_sample_data
from visualization import DroughtVisualizer


def quick_test():
    """
    Run a quick test of the drought analysis
    """
    print("=" * 60)
    print("QUICK DROUGHT ANALYSIS TEST")
    print("=" * 60)
    
    # Create sample data
    print("\n1. Creating sample data...")
    precip, temp = create_sample_data(
        lon_range=(-20, 60),
        lat_range=(-40, -10),
        time_range=('2020-01-01', '2023-12-31'),  # Shorter period for quick test
        chunk_size={'time': 50, 'lat': 15, 'lon': 15}
    )
    print(f"   ✓ Sample data created: {precip.shape}, {temp.shape}")
    
    # Initialize drought calculator
    print("\n2. Calculating drought indices...")
    drought_calc = DroughtIndices()
    
    # Calculate 3-month SPI
    spi_3m = drought_calc.calculate_spi(precip, scale=3)
    print(f"   ✓ 3-month SPI calculated: {spi_3m.shape}")
    
    # Calculate drought frequency
    drought_freq = drought_calc.calculate_drought_frequency(spi_3m, threshold=-1.0)
    print(f"   ✓ Drought frequency calculated: {drought_freq.shape}")
    
    # Create visualization
    print("\n3. Creating visualization...")
    visualizer = DroughtVisualizer()
    
    # Create output directory
    output_dir = Path('outputs')
    output_dir.mkdir(exist_ok=True)
    
    # Create a simple map
    fig = visualizer.create_drought_frequency_map(
        drought_freq,
        title="Quick Test - Southern Africa Drought Frequency",
        threshold=-1.0,
        save_path=output_dir / 'quick_test_drought_map.png',
        show=False
    )
    
    print("   ✓ Map created and saved")
    
    # Print some statistics
    print("\n4. Analysis Statistics:")
    freq_values = drought_freq.values.flatten()
    freq_values = freq_values[~np.isnan(freq_values)]
    
    print(f"   - Mean drought frequency: {freq_values.mean():.1f}%")
    print(f"   - Max drought frequency: {freq_values.max():.1f}%")
    print(f"   - Min drought frequency: {freq_values.min():.1f}%")
    print(f"   - Grid points analyzed: {len(freq_values)}")
    
    print("\n" + "=" * 60)
    print("QUICK TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nOutput saved to: {output_dir / 'quick_test_drought_map.png'}")
    print("\nTo run the full analysis:")
    print("qsub scripts/submit_drought_analysis.pbs")


if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"\nError during quick test: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)







