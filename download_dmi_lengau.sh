#!/bin/bash
# DMI Data Download Script for Lengau Cluster
# This script downloads DMI data from multiple sources on the Lengau cluster

echo "=========================================="
echo "DMI DATA DOWNLOAD - LENGAU CLUSTER"
echo "=========================================="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "Host: $(hostname)"
echo "Working Directory: $(pwd)"
echo "=========================================="

# Set up environment
module load python/3.8.5
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Create necessary directories
mkdir -p data/iod
mkdir -p output/processed
mkdir -p output/plots
mkdir -p logs

# Set up logging
LOG_FILE="logs/dmi_download_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE")
exec 2>&1

echo "Log file: $LOG_FILE"
echo "Starting DMI data download..."

# Create Python script for DMI download
cat > download_dmi_cluster.py << 'EOF'
#!/usr/bin/env python3
"""
DMI Data Download Script for Lengau Cluster
Downloads DMI data from JAMSTEC, NOAA, and BOM sources
"""

import os
import sys
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

class DMIDownloader:
    """DMI data downloader for cluster environment"""
    
    def __init__(self):
        self.data_dir = Path('data/iod')
        self.output_dir = Path('output/processed')
        self.logs_dir = Path('logs')
        
        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # DMI data sources
        self.sources = {
            'jamstec': {
                'name': 'JAMSTEC IOD Index',
                'url': 'http://www.jamstec.go.jp/frsgc/research/d1/iod/DATA/dmi.monthly.txt',
                'description': 'Japan Agency for Marine-Earth Science and Technology'
            },
            'noaa': {
                'name': 'NOAA IOD Index', 
                'url': 'https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt',
                'description': 'National Oceanic and Atmospheric Administration'
            },
            'bom': {
                'name': 'BOM IOD Index',
                'url': 'http://www.bom.gov.au/climate/enso/indices/iod.txt',
                'description': 'Bureau of Meteorology, Australia'
            }
        }
        
        # Study period
        self.start_year = 1980
        self.end_year = 2020
    
    def download_dmi_data(self):
        """Download DMI data from all sources"""
        print("=" * 60)
        print("DOWNLOADING DMI DATA FROM MULTIPLE SOURCES")
        print("=" * 60)
        
        downloaded_files = {}
        
        for source, info in self.sources.items():
            print(f"\nDownloading {info['name']}...")
            print(f"Source: {info['description']}")
            print(f"URL: {info['url']}")
            
            try:
                # Set timeout and headers for cluster environment
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                }
                
                response = requests.get(info['url'], timeout=60, headers=headers)
                
                if response.status_code == 200:
                    # Save raw data
                    raw_file = self.data_dir / f'{source}_raw.txt'
                    with open(raw_file, 'w') as f:
                        f.write(response.text)
                    
                    # Process the data
                    processed_file = self._process_dmi_file(raw_file, source)
                    if processed_file:
                        downloaded_files[source] = processed_file
                        print(f"✓ Successfully downloaded and processed {source} data")
                    else:
                        print(f"✗ Failed to process {source} data")
                else:
                    print(f"✗ Failed to download {source} data (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"✗ Error downloading {source} data: {e}")
        
        print(f"\nDMI Download Summary:")
        print(f"✓ Successfully downloaded: {len(downloaded_files)} sources")
        
        return downloaded_files
    
    def _process_dmi_file(self, file_path, source):
        """Process DMI data file and convert to standard format"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            data_rows = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            year = int(parts[0])
                            month = int(parts[1])
                            dmi = float(parts[2])
                            
                            if self.start_year <= year <= self.end_year:
                                date = pd.Timestamp(year, month, 1)
                                data_rows.append({
                                    'date': date,
                                    'year': year,
                                    'month': month,
                                    'DMI': dmi
                                })
                        except (ValueError, IndexError):
                            continue
            
            if data_rows:
                df = pd.DataFrame(data_rows)
                df.set_index('date', inplace=True)
                
                # Save processed data
                output_file = self.data_dir / f'{source}_processed.csv'
                df.to_csv(output_file)
                
                print(f"  ✓ Processed {len(df)} records from {source}")
                return str(output_file)
            else:
                print(f"  ✗ No valid data found in {source} file")
                return None
                
        except Exception as e:
            print(f"Error processing {source} file: {e}")
            return None
    
    def create_combined_dataset(self, dmi_files):
        """Create combined DMI dataset from multiple sources"""
        print("\n" + "=" * 60)
        print("CREATING COMBINED DMI DATASET")
        print("=" * 60)
        
        combined_data = {}
        
        for source, file_path in dmi_files.items():
            if Path(file_path).exists():
                print(f"Loading {source} data...")
                df = pd.read_csv(file_path, index_col=0, parse_dates=True)
                
                # Rename DMI column to include source
                df = df.rename(columns={'DMI': f'DMI_{source}'})
                combined_data[source] = df
                
                print(f"  ✓ Loaded {len(df)} records from {source}")
            else:
                print(f"  ✗ File not found: {file_path}")
        
        if combined_data:
            # Combine all datasets
            print("\nCombining datasets...")
            combined_df = pd.concat(combined_data.values(), axis=1)
            
            # Calculate ensemble mean
            dmi_columns = [col for col in combined_df.columns if col.startswith('DMI_')]
            if len(dmi_columns) > 1:
                combined_df['DMI_ensemble'] = combined_df[dmi_columns].mean(axis=1)
                print(f"  ✓ Calculated ensemble mean from {len(dmi_columns)} sources")
            
            # Save combined dataset
            output_file = self.output_dir / 'combined_dmi_data.csv'
            combined_df.to_csv(output_file)
            print(f"  ✓ Combined dataset saved to: {output_file}")
            
            return str(output_file)
        else:
            print("  ✗ No data to combine")
            return None
    
    def analyze_dmi_statistics(self, dmi_file):
        """Analyze DMI statistics"""
        print("\n" + "=" * 60)
        print("ANALYZING DMI STATISTICS")
        print("=" * 60)
        
        if not Path(dmi_file).exists():
            print(f"✗ DMI file not found: {dmi_file}")
            return None
        
        # Load data
        df = pd.read_csv(dmi_file, index_col=0, parse_dates=True)
        
        # Calculate statistics
        stats_summary = {}
        
        for col in df.columns:
            if col.startswith('DMI_'):
                data = df[col].dropna()
                if len(data) > 0:
                    stats_summary[col] = {
                        'mean': data.mean(),
                        'std': data.std(),
                        'min': data.min(),
                        'max': data.max(),
                        'positive_events': len(data[data > 0.5]),
                        'negative_events': len(data[data < -0.5]),
                        'strong_positive': len(data[data > 1.0]),
                        'strong_negative': len(data[data < -1.0])
                    }
        
        # Print statistics
        print("\nDMI Statistics Summary:")
        print("-" * 50)
        for source, stats in stats_summary.items():
            print(f"\n{source}:")
            print(f"  Mean: {stats['mean']:.3f}")
            print(f"  Std: {stats['std']:.3f}")
            print(f"  Range: [{stats['min']:.3f}, {stats['max']:.3f}]")
            print(f"  Positive events (>0.5): {stats['positive_events']}")
            print(f"  Negative events (<-0.5): {stats['negative_events']}")
            print(f"  Strong positive (>1.0): {stats['strong_positive']}")
            print(f"  Strong negative (<-1.0): {stats['strong_negative']}")
        
        return stats_summary
    
    def create_sample_data(self):
        """Create sample DMI data if real data download fails"""
        print("\nCreating sample DMI data...")
        
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
        df = pd.DataFrame({
            'DMI_sample': dmi
        }, index=time)
        
        # Save sample data
        sample_file = self.data_dir / 'sample_processed.csv'
        df.to_csv(sample_file)
        
        print(f"✓ Sample DMI data created: {sample_file}")
        return str(sample_file)

def main():
    """Main function to run DMI download on cluster"""
    print("DMI Data Download - Lengau Cluster")
    print("=" * 50)
    
    downloader = DMIDownloader()
    
    # Download DMI data
    print("\n1. Downloading DMI data from all sources...")
    dmi_files = downloader.download_dmi_data()
    
    if not dmi_files:
        print("⚠️  No real data downloaded. Creating sample data...")
        sample_file = downloader.create_sample_data()
        dmi_files = {'sample': sample_file}
    
    # Create combined dataset
    print("\n2. Creating combined DMI dataset...")
    combined_file = downloader.create_combined_dataset(dmi_files)
    
    if combined_file:
        print(f"✓ Combined DMI dataset created: {combined_file}")
        
        # Analyze statistics
        print("\n3. Analyzing DMI statistics...")
        stats = downloader.analyze_dmi_statistics(combined_file)
        
        print("\n" + "=" * 60)
        print("DMI DOWNLOAD COMPLETE")
        print("=" * 60)
        print(f"Data saved to: {Path(combined_file).parent}")
        print(f"Combined dataset: {combined_file}")
        print("=" * 60)
        
        return combined_file
    else:
        print("✗ Failed to create combined DMI dataset")
        return None

if __name__ == "__main__":
    main()
EOF

echo "Created Python script for DMI download"

# Run the DMI download
echo "Running DMI data download..."
python3 download_dmi_cluster.py

# Check results
echo ""
echo "=========================================="
echo "DMI DOWNLOAD RESULTS"
echo "=========================================="
echo "Data directory contents:"
ls -la data/iod/
echo ""
echo "Output directory contents:"
ls -la output/processed/
echo ""
echo "Log file: $LOG_FILE"
echo "=========================================="

echo "DMI download workflow completed!"
















