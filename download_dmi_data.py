#!/usr/bin/env python3
"""
Simple DMI (Dipole Mode Index) Data Download Script

This script downloads DMI data from multiple sources and processes it
for analysis. Based on the existing IOD data processing infrastructure.

Author: Mthetho Sovara
Date: June 2025
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add the current directory to Python path to import our modules
sys.path.append('.')

from iod_data_processing import IODDataProcessor

def download_dmi_data():
    """
    Download DMI data from multiple sources
    """
    print("=" * 80)
    print("DMI (DIPOLE MODE INDEX) DATA DOWNLOAD")
    print("=" * 80)
    print("This script will download DMI data from multiple sources:")
    print("• JAMSTEC (Japan Agency for Marine-Earth Science and Technology)")
    print("• NOAA (National Oceanic and Atmospheric Administration)")
    print("• BOM (Bureau of Meteorology, Australia)")
    print("=" * 80)
    
    # Initialize the IOD data processor
    processor = IODDataProcessor(data_dir='data', output_dir='output')
    
    # Download DMI data from all sources
    print("\n1. Downloading DMI data from all sources...")
    iod_files = processor.download_iod_data()
    
    if not iod_files:
        print("⚠️  No real data downloaded. This might be due to:")
        print("   • Network connectivity issues")
        print("   • Source servers being unavailable")
        print("   • URL changes")
        print("\nCreating sample DMI data for demonstration...")
        
        # Create sample data
        sample_file = processor._create_sample_iod_data()
        iod_files = {'sample': sample_file}
        print(f"✓ Sample DMI data created: {sample_file}")
    
    # Create combined dataset
    print("\n2. Creating combined DMI dataset...")
    combined_file = processor.create_combined_iod_dataset(iod_files)
    
    if combined_file:
        print(f"✓ Combined DMI dataset created: {combined_file}")
        
        # Analyze the data
        print("\n3. Analyzing DMI statistics...")
        stats = processor.analyze_iod_statistics(combined_file)
        
        # Identify DMI events
        print("\n4. Identifying DMI events...")
        events = processor.identify_iod_events(combined_file)
        
        # Create a simple summary
        print("\n" + "=" * 80)
        print("DMI DATA DOWNLOAD COMPLETE")
        print("=" * 80)
        print(f"Data saved to: {Path(combined_file).parent}")
        print(f"Combined dataset: {combined_file}")
        print(f"Analysis plots: output/plots/")
        print("=" * 80)
        
        return combined_file
    else:
        print("✗ Failed to create combined DMI dataset")
        return None

def show_dmi_data_info(data_file):
    """
    Display information about the downloaded DMI data
    """
    if not Path(data_file).exists():
        print(f"✗ Data file not found: {data_file}")
        return
    
    print("\n" + "=" * 60)
    print("DMI DATA INFORMATION")
    print("=" * 60)
    
    # Load the data
    df = pd.read_csv(data_file, index_col=0, parse_dates=True)
    
    print(f"Data file: {data_file}")
    print(f"Time period: {df.index.min().strftime('%Y-%m')} to {df.index.max().strftime('%Y-%m')}")
    print(f"Number of records: {len(df)}")
    print(f"Data columns: {list(df.columns)}")
    
    # Show basic statistics
    print("\nBasic Statistics:")
    print("-" * 30)
    for col in df.columns:
        if col.startswith('DMI_'):
            data = df[col].dropna()
            if len(data) > 0:
                print(f"\n{col}:")
                print(f"  Mean: {data.mean():.3f}")
                print(f"  Std: {data.std():.3f}")
                print(f"  Min: {data.min():.3f}")
                print(f"  Max: {data.max():.3f}")
                print(f"  Positive events (>0.5): {len(data[data > 0.5])}")
                print(f"  Negative events (<-0.5): {len(data[data < -0.5])}")

def create_dmi_quick_plot(data_file):
    """
    Create a quick plot of the DMI data
    """
    if not Path(data_file).exists():
        print(f"✗ Data file not found: {data_file}")
        return
    
    print("\nCreating DMI time series plot...")
    
    # Load the data
    df = pd.read_csv(data_file, index_col=0, parse_dates=True)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    
    for col in df.columns:
        if col.startswith('DMI_'):
            plt.plot(df.index, df[col], label=col, alpha=0.8, linewidth=1.5)
    
    # Add reference lines
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Positive threshold')
    plt.axhline(y=-0.5, color='blue', linestyle='--', alpha=0.7, label='Negative threshold')
    
    plt.title('Dipole Mode Index (DMI) Time Series', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('DMI', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    plot_file = Path(data_file).parent / 'dmi_time_series.png'
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"✓ DMI plot saved to: {plot_file}")
    plt.show()

def main():
    """
    Main function to run the DMI download workflow
    """
    print("DMI (Dipole Mode Index) Data Download Tool")
    print("=" * 50)
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. Download DMI data from all sources")
    print("2. Download DMI data and show information")
    print("3. Download DMI data and create plots")
    print("4. Just show information about existing data")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        print("\nDownloading DMI data...")
        data_file = download_dmi_data()
        if data_file:
            print(f"\n✓ DMI data successfully downloaded to: {data_file}")
        else:
            print("\n✗ Failed to download DMI data")
    
    elif choice == '2':
        print("\nDownloading DMI data and showing information...")
        data_file = download_dmi_data()
        if data_file:
            show_dmi_data_info(data_file)
        else:
            print("\n✗ Failed to download DMI data")
    
    elif choice == '3':
        print("\nDownloading DMI data and creating plots...")
        data_file = download_dmi_data()
        if data_file:
            show_dmi_data_info(data_file)
            create_dmi_quick_plot(data_file)
        else:
            print("\n✗ Failed to download DMI data")
    
    elif choice == '4':
        print("\nChecking for existing DMI data...")
        # Look for existing data files
        data_dir = Path('data/iod')
        output_dir = Path('output/processed')
        
        existing_files = []
        if data_dir.exists():
            existing_files.extend(list(data_dir.glob('*_processed.csv')))
        if output_dir.exists():
            existing_files.extend(list(output_dir.glob('*iod*.csv')))
        
        if existing_files:
            print(f"Found {len(existing_files)} existing DMI data files:")
            for i, file in enumerate(existing_files, 1):
                print(f"  {i}. {file}")
            
            if len(existing_files) == 1:
                show_dmi_data_info(str(existing_files[0]))
            else:
                file_choice = input(f"\nWhich file would you like to examine? (1-{len(existing_files)}): ").strip()
                try:
                    idx = int(file_choice) - 1
                    if 0 <= idx < len(existing_files):
                        show_dmi_data_info(str(existing_files[idx]))
                    else:
                        print("Invalid choice")
                except ValueError:
                    print("Invalid choice")
        else:
            print("No existing DMI data files found.")
            print("Run option 1, 2, or 3 to download DMI data first.")
    
    else:
        print("Invalid choice. Please run the script again and select 1-4.")

if __name__ == "__main__":
    main()
















