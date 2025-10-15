#!/usr/bin/env python3
"""
Test DMI Data Sources
This script tests alternative DMI data sources and provides working data
"""

import requests
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

def test_dmi_sources():
    """Test various DMI data sources"""
    print("=" * 60)
    print("TESTING DMI DATA SOURCES")
    print("=" * 60)
    
    # Alternative DMI sources to test
    sources = {
        'noaa_primary': {
            'name': 'NOAA Primary',
            'url': 'https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt',
            'description': 'NOAA Climate Prediction Center'
        },
        'noaa_alternative': {
            'name': 'NOAA Alternative',
            'url': 'https://www.cpc.ncep.noaa.gov/data/indices/iod.txt',
            'description': 'NOAA Alternative URL'
        },
        'bom_primary': {
            'name': 'BOM Primary',
            'url': 'http://www.bom.gov.au/climate/enso/indices/iod.txt',
            'description': 'Bureau of Meteorology, Australia'
        },
        'bom_alternative': {
            'name': 'BOM Alternative',
            'url': 'http://www.bom.gov.au/climate/enso/indices/iod_monthly.txt',
            'description': 'BOM Alternative URL'
        }
    }
    
    working_sources = []
    
    for source, info in sources.items():
        print(f"\nTesting {info['name']}...")
        print(f"URL: {info['url']}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            }
            
            response = requests.get(info['url'], timeout=30, headers=headers)
            
            if response.status_code == 200:
                # Check if response contains data (not HTML)
                if '<html>' not in response.text.lower() and '<!doctype html>' not in response.text.lower():
                    # Try to parse the data
                    lines = response.text.strip().split('\n')
                    data_lines = [line for line in lines if line.strip() and not line.startswith('#')]
                    
                    if len(data_lines) > 0:
                        print(f"  ✓ SUCCESS: {len(data_lines)} data lines found")
                        working_sources.append((source, info, response.text))
                    else:
                        print(f"  ✗ No data lines found")
                else:
                    print(f"  ✗ HTML response (likely maintenance page)")
            else:
                print(f"  ✗ HTTP Error {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return working_sources

def create_working_dmi_data():
    """Create working DMI data from available sources"""
    print("\n" + "=" * 60)
    print("CREATING WORKING DMI DATA")
    print("=" * 60)
    
    # Test sources
    working_sources = test_dmi_sources()
    
    if not working_sources:
        print("⚠️  No working sources found. Creating sample data...")
        return create_sample_dmi_data()
    
    # Process working sources
    processed_files = []
    
    for source, info, data in working_sources:
        print(f"\nProcessing {info['name']}...")
        
        try:
            # Save raw data
            raw_file = Path(f'data/iod/{source}_raw.txt')
            raw_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(raw_file, 'w') as f:
                f.write(data)
            
            # Process the data
            processed_file = process_dmi_data(raw_file, source)
            if processed_file:
                processed_files.append(processed_file)
                print(f"  ✓ Processed data saved to: {processed_file}")
            else:
                print(f"  ✗ Failed to process data")
                
        except Exception as e:
            print(f"  ✗ Error processing {source}: {e}")
    
    return processed_files

def process_dmi_data(file_path, source):
    """Process DMI data file"""
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
                        
                        if 1980 <= year <= 2020:
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
            output_file = Path(f'data/iod/{source}_processed.csv')
            df.to_csv(output_file)
            
            print(f"  ✓ Processed {len(df)} records")
            return str(output_file)
        else:
            print(f"  ✗ No valid data found")
            return None
            
    except Exception as e:
        print(f"  ✗ Error processing file: {e}")
        return None

def create_sample_dmi_data():
    """Create sample DMI data"""
    print("Creating sample DMI data...")
    
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
    sample_file = Path('data/iod/sample_processed.csv')
    sample_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(sample_file)
    
    print(f"✓ Sample DMI data created: {sample_file}")
    return [str(sample_file)]

def main():
    """Main function"""
    print("DMI Data Source Testing and Download")
    print("=" * 50)
    
    # Create working DMI data
    processed_files = create_working_dmi_data()
    
    if processed_files:
        print(f"\n✓ Successfully created {len(processed_files)} DMI data files:")
        for file in processed_files:
            print(f"  - {file}")
        
        # Create combined dataset if multiple sources
        if len(processed_files) > 1:
            print("\nCreating combined dataset...")
            create_combined_dataset(processed_files)
    else:
        print("\n✗ No DMI data files created")

def create_combined_dataset(processed_files):
    """Create combined dataset from multiple sources"""
    try:
        combined_data = {}
        
        for file_path in processed_files:
            if Path(file_path).exists():
                df = pd.read_csv(file_path, index_col=0, parse_dates=True)
                source_name = Path(file_path).stem.replace('_processed', '')
                df = df.rename(columns={'DMI': f'DMI_{source_name}'})
                combined_data[source_name] = df
        
        if combined_data:
            combined_df = pd.concat(combined_data.values(), axis=1)
            
            # Calculate ensemble mean
            dmi_columns = [col for col in combined_df.columns if col.startswith('DMI_')]
            if len(dmi_columns) > 1:
                combined_df['DMI_ensemble'] = combined_df[dmi_columns].mean(axis=1)
            
            # Save combined dataset
            output_file = Path('output/processed/combined_dmi_data.csv')
            output_file.parent.mkdir(parents=True, exist_ok=True)
            combined_df.to_csv(output_file)
            
            print(f"✓ Combined dataset saved to: {output_file}")
            
            # Show basic statistics
            print("\nBasic Statistics:")
            print(combined_df.describe())
            
            return str(output_file)
        else:
            print("✗ No data to combine")
            return None
            
    except Exception as e:
        print(f"✗ Error creating combined dataset: {e}")
        return None

if __name__ == "__main__":
    main()
















