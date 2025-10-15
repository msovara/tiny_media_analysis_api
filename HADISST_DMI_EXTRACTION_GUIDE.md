# DMI Extraction from HadISST Data - Complete Guide

This guide shows you how to extract DMI (Dipole Mode Index) data from your HadISST sea surface temperature dataset for the 1980-2020 period.

## 📊 What is DMI?

The Dipole Mode Index (DMI) measures the Indian Ocean Dipole (IOD) by calculating the difference in sea surface temperature between:
- **Western Indian Ocean** (50°E-70°E, 10°S-10°N)
- **Eastern Indian Ocean** (90°E-110°E, 10°S-0°N)

**Formula**: DMI = Western SST - Eastern SST

## 🎯 Your HadISST Data

Your file contains:
- **Time period**: 1870-present (1867 time steps)
- **Spatial resolution**: 1° × 1° (180 lat × 360 lon)
- **Temporal resolution**: Monthly
- **Study period**: 1980-2020 (492 months)

## 🚀 Quick Start

### Step 1: Prepare Your Environment
```bash
# On Lengau cluster
ssh -X msovara@lengau.chpc.ac.za
cd /path/to/your/DataDownloads

# Make sure HadISST_sst.nc is in your directory
ls -la HadISST_sst.nc
```

### Step 2: Run DMI Extraction
```bash
# Make the script executable
chmod +x run_dmi_extraction_lengau.sh

# Run the extraction
./run_dmi_extraction_lengau.sh
```

### Step 3: Check Results
```bash
# View the extracted DMI data
head -20 output/processed/dmi_hadisst_1980_2020.csv

# View the analysis plot
ls -la output/plots/
```

## 📈 What the Script Does

### 1. **Data Loading**
- Loads HadISST data for 1980-2020 period
- Handles time conversion from days since 1870
- Selects appropriate spatial and temporal subset

### 2. **DMI Calculation**
- Defines Western Indian Ocean region (50°E-70°E, 10°S-10°N)
- Defines Eastern Indian Ocean region (90°E-110°E, 10°S-0°N)
- Calculates area-weighted mean SST for each region
- Computes DMI = Western SST - Eastern SST

### 3. **Data Processing**
- Creates monthly DMI time series
- Adds year and month columns
- Removes any missing values
- Formats data for analysis

### 4. **Analysis**
- Calculates basic statistics (mean, std, min, max)
- Identifies positive and negative IOD events
- Creates seasonal cycle analysis
- Generates annual means

### 5. **Visualization**
- Time series plot with thresholds
- Seasonal cycle analysis
- Distribution histogram
- Annual means plot

## 📁 Output Files

After running the script, you'll get:

```
output/
├── processed/
│   └── dmi_hadisst_1980_2020.csv    # DMI time series data
└── plots/
    └── dmi_analysis_hadisst.png     # Analysis plots

logs/
└── dmi_extraction_YYYYMMDD_HHMMSS.log  # Detailed log file
```

## 📊 DMI Data Format

The output CSV file contains:
```csv
time,month,year,DMI
1980-01-01,1,1980,0.123
1980-02-01,2,1980,-0.456
...
2020-12-01,12,2020,0.789
```

## 🔍 Understanding DMI Values

- **DMI > 0.5**: Positive IOD event (warm western, cool eastern Indian Ocean)
- **DMI < -0.5**: Negative IOD event (cool western, warm eastern Indian Ocean)
- **|DMI| > 1.0**: Strong IOD event
- **|DMI| < 0.5**: Neutral conditions

## 📈 Expected Results

Based on your 1980-2020 period, you should see:

### **Major IOD Events Captured:**
- **1982-83**: Strong positive IOD
- **1997-98**: Strong positive IOD (coincided with El Niño)
- **2006-07**: Strong positive IOD
- **2011-12**: Strong positive IOD
- **2016**: Strong negative IOD

### **Statistical Summary:**
- **Mean DMI**: ~0.0 (neutral)
- **Standard Deviation**: ~0.5-0.8
- **Positive Events**: 15-25 months
- **Negative Events**: 15-25 months
- **Strong Events**: 5-10 months

## 🛠️ Customization Options

### **Modify Time Period**
```python
# In extract_dmi_from_hadisst.py, change:
self.start_year = 1980
self.end_year = 2020
```

### **Modify IOD Regions**
```python
# Western region
self.western_region = {
    'lon_min': 50, 'lon_max': 70,
    'lat_min': -10, 'lat_max': 10
}

# Eastern region
self.eastern_region = {
    'lon_min': 90, 'lon_max': 110,
    'lat_min': -10, 'lat_max': 0
}
```

### **Change Event Thresholds**
```python
# In identify_iod_events method:
threshold = 0.5  # Change to 0.4 or 0.6 as needed
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **File Not Found**
   ```bash
   # Check if HadISST file exists
   ls -la HadISST_sst.nc
   
   # If not found, check the path in the script
   ```

2. **Memory Issues**
   ```bash
   # Load more memory modules
   module load python/3.8.5
   module load gcc/9.3.0
   ```

3. **Time Conversion Issues**
   - The script handles different time formats automatically
   - Check the log file for any time conversion errors

### **Check Results:**
```bash
# View DMI data
head -20 output/processed/dmi_hadisst_1980_2020.csv

# Check data quality
python3 -c "
import pandas as pd
df = pd.read_csv('output/processed/dmi_hadisst_1980_2020.csv', index_col=0, parse_dates=True)
print(f'Records: {len(df)}')
print(f'Period: {df.index.min()} to {df.index.max()}')
print(f'DMI range: {df.DMI.min():.3f} to {df.DMI.max():.3f}')
"
```

## 📊 Data Analysis

After extraction, you can analyze the DMI data:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load DMI data
df = pd.read_csv('output/processed/dmi_hadisst_1980_2020.csv', index_col=0, parse_dates=True)

# Basic statistics
print("DMI Statistics:")
print(df['DMI'].describe())

# Plot time series
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['DMI'], 'b-', linewidth=1)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.7)
plt.axhline(y=-0.5, color='blue', linestyle='--', alpha=0.7)
plt.title('DMI Time Series (1980-2020)')
plt.xlabel('Date')
plt.ylabel('DMI')
plt.grid(True, alpha=0.3)
plt.show()
```

## 🎯 Next Steps

After extracting DMI data:

1. **Integrate with drought analysis** - Use DMI data in your drought correlation studies
2. **Compare with other sources** - Validate against JAMSTEC, NOAA, BOM data
3. **Create correlation analysis** - Analyze DMI-drought relationships
4. **Generate reports** - Create comprehensive analysis reports

## 📚 References

- **HadISST**: Rayner et al. (2003) - Global analyses of sea surface temperature
- **IOD Definition**: Saji et al. (1999) - A dipole mode in the tropical Indian Ocean
- **DMI Calculation**: Webster et al. (1999) - Coupled ocean-atmosphere dynamics

This extraction gives you high-quality DMI data directly from sea surface temperature observations, which is often more reliable than downloaded index data!
















