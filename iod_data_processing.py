"""
IOD Data Processing and Analysis Workflow

This script processes IOD (Indian Ocean Dipole) data from multiple sources
and prepares it for correlation analysis with drought indices.

Author: Mthetho Sovara
Date: June 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import requests
import warnings
from datetime import datetime, timedelta
import urllib.parse
import json

warnings.filterwarnings('ignore')

class IODDataProcessor:
    """Main class for processing IOD data from multiple sources"""
    
    def __init__(self, data_dir='data', output_dir='output'):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create output subdirectories
        (self.output_dir / 'iod').mkdir(exist_ok=True)
        (self.output_dir / 'processed').mkdir(exist_ok=True)
        (self.output_dir / 'plots').mkdir(exist_ok=True)
        
        # Study period
        self.start_year = 1980
        self.end_year = 2020
        
        # IOD data sources
        self.iod_sources = {
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
    
    def download_iod_data(self):
        """
        Download IOD data from multiple sources
        """
        print("=" * 60)
        print("DOWNLOADING IOD DATA FROM MULTIPLE SOURCES")
        print("=" * 60)
        
        downloaded_files = {}
        
        for source, info in self.iod_sources.items():
            print(f"\nDownloading {info['name']}...")
            print(f"Source: {info['description']}")
            print(f"URL: {info['url']}")
            
            try:
                response = requests.get(info['url'], timeout=30)
                
                if response.status_code == 200:
                    # Save raw data
                    raw_file = self.data_dir / 'iod' / f'{source}_raw.txt'
                    with open(raw_file, 'w') as f:
                        f.write(response.text)
                    
                    # Process the data
                    processed_file = self._process_iod_file(raw_file, source)
                    if processed_file:
                        downloaded_files[source] = processed_file
                        print(f"✓ Successfully downloaded and processed {source} data")
                    else:
                        print(f"✗ Failed to process {source} data")
                else:
                    print(f"✗ Failed to download {source} data (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"✗ Error downloading {source} data: {e}")
        
        print(f"\nIOD Download Summary:")
        print(f"✓ Successfully downloaded: {len(downloaded_files)} sources")
        
        return downloaded_files
    
    def _process_iod_file(self, file_path, source):
        """
        Process IOD data file and convert to standard format
        """
        try:
            # Read the file
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Process based on source
            if source == 'jamstec':
                return self._process_jamstec_data(lines, source)
            elif source == 'noaa':
                return self._process_noaa_data(lines, source)
            elif source == 'bom':
                return self._process_bom_data(lines, source)
            else:
                print(f"Unknown source: {source}")
                return None
                
        except Exception as e:
            print(f"Error processing {source} file: {e}")
            return None
    
    def _process_jamstec_data(self, lines, source):
        """
        Process JAMSTEC IOD data
        """
        print("  Processing JAMSTEC data...")
        
        data_rows = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # JAMSTEC format: YYYY MM DMI
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
            output_file = self.data_dir / 'iod' / f'{source}_processed.csv'
            df.to_csv(output_file)
            
            print(f"  ✓ Processed {len(df)} records from JAMSTEC")
            return str(output_file)
        else:
            print("  ✗ No valid data found in JAMSTEC file")
            return None
    
    def _process_noaa_data(self, lines, source):
        """
        Process NOAA IOD data
        """
        print("  Processing NOAA data...")
        
        data_rows = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # NOAA format: YYYY MM DMI
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
            output_file = self.data_dir / 'iod' / f'{source}_processed.csv'
            df.to_csv(output_file)
            
            print(f"  ✓ Processed {len(df)} records from NOAA")
            return str(output_file)
        else:
            print("  ✗ No valid data found in NOAA file")
            return None
    
    def _process_bom_data(self, lines, source):
        """
        Process BOM IOD data
        """
        print("  Processing BOM data...")
        
        data_rows = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # BOM format: YYYY MM DMI
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
            output_file = self.data_dir / 'iod' / f'{source}_processed.csv'
            df.to_csv(output_file)
            
            print(f"  ✓ Processed {len(df)} records from BOM")
            return str(output_file)
        else:
            print("  ✗ No valid data found in BOM file")
            return None
    
    def create_combined_iod_dataset(self, iod_files):
        """
        Create a combined IOD dataset from multiple sources
        """
        print("\n" + "=" * 60)
        print("CREATING COMBINED IOD DATASET")
        print("=" * 60)
        
        combined_data = {}
        
        for source, file_path in iod_files.items():
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
            output_file = self.output_dir / 'processed' / 'combined_iod_data.csv'
            combined_df.to_csv(output_file)
            print(f"  ✓ Combined dataset saved to: {output_file}")
            
            return str(output_file)
        else:
            print("  ✗ No data to combine")
            return None
    
    def analyze_iod_statistics(self, iod_file):
        """
        Analyze IOD statistics and create summary plots
        """
        print("\n" + "=" * 60)
        print("ANALYZING IOD STATISTICS")
        print("=" * 60)
        
        if not Path(iod_file).exists():
            print(f"✗ IOD file not found: {iod_file}")
            return None
        
        # Load data
        df = pd.read_csv(iod_file, index_col=0, parse_dates=True)
        
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
        print("\nIOD Statistics Summary:")
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
        
        # Create plots
        self._create_iod_plots(df)
        
        return stats_summary
    
    def _create_iod_plots(self, df):
        """
        Create IOD analysis plots
        """
        print("\nCreating IOD analysis plots...")
        
        # Time series plot
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Time series
        ax1 = axes[0, 0]
        for col in df.columns:
            if col.startswith('DMI_'):
                ax1.plot(df.index, df[col], label=col, alpha=0.7)
        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Positive threshold')
        ax1.axhline(y=-0.5, color='blue', linestyle='--', alpha=0.5, label='Negative threshold')
        ax1.set_title('IOD Time Series')
        ax1.set_ylabel('DMI')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Seasonal cycle
        ax2 = axes[0, 1]
        for col in df.columns:
            if col.startswith('DMI_'):
                monthly_mean = df[col].groupby(df.index.month).mean()
                ax2.plot(monthly_mean.index, monthly_mean.values, label=col, marker='o')
        ax2.set_title('IOD Seasonal Cycle')
        ax2.set_xlabel('Month')
        ax2.set_ylabel('Mean DMI')
        ax2.set_xticks(range(1, 13))
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Distribution
        ax3 = axes[1, 0]
        for col in df.columns:
            if col.startswith('DMI_'):
                data = df[col].dropna()
                ax3.hist(data, bins=30, alpha=0.7, label=col, density=True)
        ax3.set_title('IOD Distribution')
        ax3.set_xlabel('DMI')
        ax3.set_ylabel('Density')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Correlation between sources
        ax4 = axes[1, 1]
        dmi_columns = [col for col in df.columns if col.startswith('DMI_')]
        if len(dmi_columns) >= 2:
            corr_matrix = df[dmi_columns].corr()
            im = ax4.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
            ax4.set_xticks(range(len(dmi_columns)))
            ax4.set_yticks(range(len(dmi_columns)))
            ax4.set_xticklabels(dmi_columns, rotation=45)
            ax4.set_yticklabels(dmi_columns)
            ax4.set_title('IOD Sources Correlation')
            
            # Add correlation values
            for i in range(len(dmi_columns)):
                for j in range(len(dmi_columns)):
                    text = ax4.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                   ha="center", va="center", color="black")
            
            plt.colorbar(im, ax=ax4)
        
        plt.tight_layout()
        
        # Save plot
        output_file = self.output_dir / 'plots' / 'iod_analysis.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ IOD analysis plot saved to: {output_file}")
        plt.close()
    
    def identify_iod_events(self, iod_file, threshold=0.5):
        """
        Identify IOD events from the data
        """
        print(f"\nIdentifying IOD events (threshold: {threshold})...")
        
        if not Path(iod_file).exists():
            print(f"✗ IOD file not found: {iod_file}")
            return None
        
        # Load data
        df = pd.read_csv(iod_file, index_col=0, parse_dates=True)
        
        events = {}
        
        for col in df.columns:
            if col.startswith('DMI_'):
                data = df[col].dropna()
                
                # Identify positive events
                positive_events = []
                negative_events = []
                
                # Find consecutive periods above/below threshold
                above_threshold = data > threshold
                below_threshold = data < -threshold
                
                # Find event start and end dates
                pos_starts = data.index[above_threshold & ~above_threshold.shift(1).fillna(False)]
                pos_ends = data.index[above_threshold & ~above_threshold.shift(-1).fillna(False)]
                
                neg_starts = data.index[below_threshold & ~below_threshold.shift(1).fillna(False)]
                neg_ends = data.index[below_threshold & ~below_threshold.shift(-1).fillna(False)]
                
                # Create event records
                for start, end in zip(pos_starts, pos_ends):
                    if end > start:
                        event_data = data.loc[start:end]
                        positive_events.append({
                            'start': start,
                            'end': end,
                            'duration': len(event_data),
                            'max_intensity': event_data.max(),
                            'mean_intensity': event_data.mean()
                        })
                
                for start, end in zip(neg_starts, neg_ends):
                    if end > start:
                        event_data = data.loc[start:end]
                        negative_events.append({
                            'start': start,
                            'end': end,
                            'duration': len(event_data),
                            'min_intensity': event_data.min(),
                            'mean_intensity': event_data.mean()
                        })
                
                events[col] = {
                    'positive_events': positive_events,
                    'negative_events': negative_events
                }
        
        # Print event summary
        print("\nIOD Events Summary:")
        print("-" * 50)
        for source, source_events in events.items():
            pos_events = source_events['positive_events']
            neg_events = source_events['negative_events']
            
            print(f"\n{source}:")
            print(f"  Positive events: {len(pos_events)}")
            print(f"  Negative events: {len(neg_events)}")
            
            if pos_events:
                print("  Strong positive events:")
                for event in pos_events:
                    print(f"    {event['start'].strftime('%Y-%m')} to {event['end'].strftime('%Y-%m')} "
                          f"(Duration: {event['duration']} months, Max: {event['max_intensity']:.2f})")
            
            if neg_events:
                print("  Strong negative events:")
                for event in neg_events:
                    print(f"    {event['start'].strftime('%Y-%m')} to {event['end'].strftime('%Y-%m')} "
                          f"(Duration: {event['duration']} months, Min: {event['min_intensity']:.2f})")
        
        return events
    
    def run_iod_processing_workflow(self):
        """
        Run the complete IOD data processing workflow
        """
        print("=" * 80)
        print("IOD DATA PROCESSING WORKFLOW")
        print("=" * 80)
        
        # Download IOD data
        print("\n1. Downloading IOD data from multiple sources...")
        iod_files = self.download_iod_data()
        
        if not iod_files:
            print("✗ No IOD data downloaded. Creating sample data...")
            sample_file = self._create_sample_iod_data()
            iod_files = {'sample': sample_file}
        
        # Create combined dataset
        print("\n2. Creating combined IOD dataset...")
        combined_file = self.create_combined_iod_dataset(iod_files)
        
        if combined_file:
            # Analyze statistics
            print("\n3. Analyzing IOD statistics...")
            stats = self.analyze_iod_statistics(combined_file)
            
            # Identify events
            print("\n4. Identifying IOD events...")
            events = self.identify_iod_events(combined_file)
            
            print("\n" + "=" * 80)
            print("IOD PROCESSING WORKFLOW COMPLETE")
            print("=" * 80)
            print("Output files saved to:")
            print(f"  Raw data: {self.data_dir / 'iod'}")
            print(f"  Processed data: {self.output_dir / 'processed'}")
            print(f"  Plots: {self.output_dir / 'plots'}")
            print("=" * 80)
            
            return {
                'combined_file': combined_file,
                'statistics': stats,
                'events': events
            }
        else:
            print("✗ Failed to create combined IOD dataset")
            return None
    
    def _create_sample_iod_data(self):
        """
        Create sample IOD data for testing
        """
        print("Creating sample IOD data...")
        
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
        sample_file = self.data_dir / 'iod' / 'sample_processed.csv'
        df.to_csv(sample_file)
        
        print(f"✓ Sample IOD data created: {sample_file}")
        return str(sample_file)

def main():
    """Main function to run the IOD processing workflow"""
    processor = IODDataProcessor()
    
    # Ask user if they want to use sample data
    use_sample = input("Use sample IOD data for testing? (y/n): ").lower().strip() == 'y'
    
    if use_sample:
        print("Using sample IOD data for demonstration...")
        sample_file = processor._create_sample_iod_data()
        iod_files = {'sample': sample_file}
        
        # Create combined dataset
        combined_file = processor.create_combined_iod_dataset(iod_files)
        
        if combined_file:
            # Analyze statistics
            stats = processor.analyze_iod_statistics(combined_file)
            
            # Identify events
            events = processor.identify_iod_events(combined_file)
    else:
        print("Processing real IOD data...")
        processor.run_iod_processing_workflow()

if __name__ == "__main__":
    main()


















