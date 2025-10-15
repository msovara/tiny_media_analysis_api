# DMI Data Download on Lengau Cluster

This guide shows you how to download DMI (Dipole Mode Index) data on the Lengau cluster at CHPC.

## Prerequisites

1. **SSH Access to Lengau Cluster**
   ```bash
   ssh -X msovara@lengau.chpc.ac.za
   ```

2. **Required Files** (already created for you):
   - `download_dmi_lengau.sh` - Main download script
   - `submit_dmi_download.pbs` - PBS job submission script
   - `DMI_LENGAU_CLUSTER_GUIDE.md` - This guide

## Quick Start

### Option 1: Interactive Download (Recommended for testing)

1. **Connect to Lengau cluster:**
   ```bash
   ssh -X msovara@lengau.chpc.ac.za
   ```

2. **Navigate to your project directory:**
   ```bash
   cd /path/to/your/tiny-media-analysis
   ```

3. **Make the script executable:**
   ```bash
   chmod +x download_dmi_lengau.sh
   ```

4. **Run the download script:**
   ```bash
   ./download_dmi_lengau.sh
   ```

### Option 2: Submit as PBS Job (Recommended for production)

1. **Connect to Lengau cluster:**
   ```bash
   ssh -X msovara@lengau.chpc.ac.za
   ```

2. **Navigate to your project directory:**
   ```bash
   cd /path/to/your/tiny-media-analysis
   ```

3. **Submit the job:**
   ```bash
   qsub submit_dmi_download.pbs
   ```

4. **Check job status:**
   ```bash
   qstat -u msovara
   ```

5. **View job output:**
   ```bash
   # Check job output
   cat logs/dmi_download_<JOBID>.out
   
   # Check for errors
   cat logs/dmi_download_<JOBID>.err
   ```

## What the Script Does

### 1. **Environment Setup**
- Loads Python 3.8.5 module
- Sets up required directories
- Configures logging

### 2. **Data Download**
Downloads DMI data from three sources:
- **JAMSTEC**: http://www.jamstec.go.jp/frsgc/research/d1/iod/DATA/dmi.monthly.txt
- **NOAA**: https://www.cpc.ncep.noaa.gov/data/indices/dmi.monthly.txt
- **BOM**: http://www.bom.gov.au/climate/enso/indices/iod.txt

### 3. **Data Processing**
- Converts raw text data to CSV format
- Creates time series with proper date indexing
- Handles different data formats from different sources

### 4. **Data Analysis**
- Calculates basic statistics (mean, std, min, max)
- Identifies positive and negative IOD events
- Creates ensemble mean from multiple sources

### 5. **Output Generation**
- Saves processed data to `output/processed/`
- Creates log files in `logs/`
- Generates summary statistics

## Output Files

After successful completion, you'll find:

```
data/
├── iod/
│   ├── jamstec_raw.txt          # Raw JAMSTEC data
│   ├── noaa_raw.txt             # Raw NOAA data
│   ├── bom_raw.txt              # Raw BOM data
│   ├── jamstec_processed.csv    # Processed JAMSTEC data
│   ├── noaa_processed.csv       # Processed NOAA data
│   ├── bom_processed.csv        # Processed BOM data
│   └── sample_processed.csv     # Sample data (if real download fails)

output/
├── processed/
│   └── combined_dmi_data.csv    # Combined dataset from all sources

logs/
├── dmi_download_YYYYMMDD_HHMMSS.log  # Main log file
├── dmi_download_<JOBID>.out          # PBS output (if using job)
└── dmi_download_<JOBID>.err          # PBS error (if using job)
```

## Job Configuration

The PBS job is configured with:
- **Queue**: normal
- **Nodes**: 1
- **CPUs**: 1
- **Memory**: 4GB
- **Walltime**: 1 hour
- **Modules**: python/3.8.5, gcc/9.3.0

## Monitoring the Job

### Check Job Status
```bash
# View your jobs
qstat -u msovara

# View all jobs in queue
qstat -q

# View job details
qstat -f <JOBID>
```

### Monitor Progress
```bash
# Watch log file in real-time
tail -f logs/dmi_download_<JOBID>.out

# Check data directory
ls -la data/iod/

# Check output directory
ls -la output/processed/
```

### Cancel Job (if needed)
```bash
qdel <JOBID>
```

## Troubleshooting

### Common Issues

1. **Module Loading Issues**
   ```bash
   # Check available modules
   module avail python
   
   # Load specific version
   module load python/3.8.5
   ```

2. **Network Connectivity Issues**
   - The script will automatically create sample data if real download fails
   - Check cluster network connectivity
   - Verify source URLs are accessible

3. **Permission Issues**
   ```bash
   # Make scripts executable
   chmod +x download_dmi_lengau.sh
   chmod +x submit_dmi_download.pbs
   ```

4. **Directory Issues**
   ```bash
   # Create directories manually if needed
   mkdir -p data/iod output/processed logs
   ```

### Checking Results

1. **Verify Download Success**
   ```bash
   # Check if files exist
   ls -la data/iod/
   ls -la output/processed/
   
   # Check file sizes
   du -h data/iod/*
   du -h output/processed/*
   ```

2. **View Data Content**
   ```bash
   # View processed data
   head -20 data/iod/jamstec_processed.csv
   head -20 output/processed/combined_dmi_data.csv
   ```

3. **Check Logs**
   ```bash
   # View main log
   cat logs/dmi_download_*.log
   
   # View PBS output
   cat logs/dmi_download_*.out
   cat logs/dmi_download_*.err
   ```

## Data Analysis

After downloading, you can analyze the DMI data:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load combined data
df = pd.read_csv('output/processed/combined_dmi_data.csv', index_col=0, parse_dates=True)

# Basic statistics
print("DMI Statistics:")
print(df.describe())

# Plot time series
plt.figure(figsize=(12, 6))
for col in df.columns:
    if col.startswith('DMI_'):
        plt.plot(df.index, df[col], label=col, alpha=0.8)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)
plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
plt.axhline(y=-0.5, color='blue', linestyle='--', alpha=0.5)
plt.title('DMI Time Series')
plt.xlabel('Date')
plt.ylabel('DMI')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dmi_time_series.png', dpi=300, bbox_inches='tight')
plt.show()
```

## Next Steps

After successfully downloading DMI data:

1. **Integrate with your drought analysis workflow**
2. **Use the data for IOD-drought correlation analysis**
3. **Create visualizations and reports**
4. **Export data for further analysis**

## Support

If you encounter issues:

1. Check the log files in `logs/`
2. Verify your cluster access and permissions
3. Ensure all required modules are loaded
4. Check network connectivity to data sources

The script includes fallback sample data generation if real data download fails, so you can always test the workflow with sample data.
















