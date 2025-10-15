# DMI (Dipole Mode Index) Data Download Guide

This guide shows you how to download DMI (Dipole Mode Index) data from multiple sources using your existing project infrastructure.

## What is DMI?

The Dipole Mode Index (DMI) is a measure of the Indian Ocean Dipole (IOD), which is a climate phenomenon that affects weather patterns in the Indian Ocean region and beyond. The IOD is characterized by:

- **Positive IOD**: Warmer sea surface temperatures in the western Indian Ocean and cooler temperatures in the eastern Indian Ocean
- **Negative IOD**: Cooler sea surface temperatures in the western Indian Ocean and warmer temperatures in the eastern Indian Ocean

## Available DMI Data Sources

Your project can download DMI data from three major sources:

### 1. JAMSTEC (Japan Agency for Marine-Earth Science and Technology)
- **URL**: http://www.jamstec.go.jp/frsgc/research/d1/iod/DATA/dmi.monthly.txt
- **Description**: Japanese research institution providing IOD data
- **Data Format**: Monthly DMI values
- **Time Period**: 1980-present

### 2. NOAA (National Oceanic and Atmospheric Administration)
- **URL**: https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt
- **Description**: US government agency providing climate data
- **Data Format**: Monthly DMI values
- **Time Period**: 1980-present

### 3. BOM (Bureau of Meteorology, Australia)
- **URL**: http://www.bom.gov.au/climate/enso/indices/iod.txt
- **Description**: Australian government meteorological service
- **Data Format**: Monthly DMI values
- **Time Period**: 1980-present

## How to Download DMI Data

### Method 1: Using the Simple DMI Download Script

I've created a simple script specifically for downloading DMI data:

```bash
python download_dmi_data.py
```

This script provides 4 options:
1. **Download DMI data from all sources** - Downloads from JAMSTEC, NOAA, and BOM
2. **Download and show information** - Downloads data and displays statistics
3. **Download and create plots** - Downloads data, shows info, and creates visualizations
4. **Show existing data info** - Displays information about already downloaded data

### Method 2: Using the Main Workflow

You can also use your existing main workflow:

```bash
python main_workflow.py
```

Select option 3 to run the complete workflow with sample data, which includes DMI data processing.

### Method 3: Using the IOD Data Processing Module Directly

```python
from iod_data_processing import IODDataProcessor

# Initialize the processor
processor = IODDataProcessor(data_dir='data', output_dir='output')

# Download DMI data from all sources
iod_files = processor.download_iod_data()

# Create combined dataset
combined_file = processor.create_combined_iod_dataset(iod_files)

# Analyze the data
stats = processor.analyze_iod_statistics(combined_file)
events = processor.identify_iod_events(combined_file)
```

## Data Processing Features

Your DMI download system includes:

### 1. **Multi-Source Download**
- Downloads from JAMSTEC, NOAA, and BOM simultaneously
- Handles network errors gracefully
- Creates fallback sample data if real data is unavailable

### 2. **Data Processing**
- Converts raw text data to structured CSV format
- Handles different data formats from different sources
- Creates time series with proper date indexing

### 3. **Data Analysis**
- Calculates basic statistics (mean, std, min, max)
- Identifies positive and negative IOD events
- Creates ensemble mean from multiple sources
- Generates correlation analysis between sources

### 4. **Visualization**
- Time series plots
- Seasonal cycle analysis
- Distribution histograms
- Correlation matrices between sources

## Output Files

After downloading, your data will be saved in:

```
data/
├── iod/
│   ├── jamstec_raw.txt          # Raw JAMSTEC data
│   ├── noaa_raw.txt             # Raw NOAA data
│   ├── bom_raw.txt              # Raw BOM data
│   ├── jamstec_processed.csv    # Processed JAMSTEC data
│   ├── noaa_processed.csv       # Processed NOAA data
│   └── bom_processed.csv        # Processed BOM data

output/
├── processed/
│   └── combined_iod_data.csv    # Combined dataset
└── plots/
    └── iod_analysis.png         # Analysis plots
```

## Understanding DMI Values

- **DMI > 0.5**: Positive IOD event (warm western, cool eastern Indian Ocean)
- **DMI < -0.5**: Negative IOD event (cool western, warm eastern Indian Ocean)
- **|DMI| > 1.0**: Strong IOD event
- **|DMI| < 0.5**: Neutral conditions

## Common IOD Events

Your data includes several well-known IOD events:

- **1997-1998**: Strong positive IOD (coincided with strong El Niño)
- **2006-2007**: Strong positive IOD
- **2011-2012**: Strong positive IOD
- **2016**: Strong negative IOD

## Troubleshooting

### If Download Fails
1. Check your internet connection
2. Verify the source URLs are accessible
3. The script will automatically create sample data for testing

### If Data Processing Fails
1. Check that the data files exist in `data/iod/`
2. Verify the file formats match expected structure
3. Use the sample data option for testing

### If Plots Don't Generate
1. Ensure matplotlib is installed: `pip install matplotlib`
2. Check that the data files contain valid data
3. Verify the output directory exists and is writable

## Next Steps

After downloading DMI data, you can:

1. **Analyze IOD events** - Identify periods of positive/negative IOD
2. **Correlate with drought** - Use the data in your drought analysis workflow
3. **Create forecasts** - Use historical data for prediction models
4. **Compare sources** - Analyze differences between JAMSTEC, NOAA, and BOM data

## Example Usage

```python
# Quick start - download and analyze DMI data
from iod_data_processing import IODDataProcessor

processor = IODDataProcessor()
iod_files = processor.download_iod_data()
combined_file = processor.create_combined_iod_dataset(iod_files)
stats = processor.analyze_iod_statistics(combined_file)
events = processor.identify_iod_events(combined_file)

print(f"DMI data saved to: {combined_file}")
print(f"Found {len(events)} IOD events")
```

This guide should help you successfully download and analyze DMI data for your research!
















