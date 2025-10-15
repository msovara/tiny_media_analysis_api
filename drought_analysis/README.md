# Southern Africa Drought Analysis - Lengau Cluster

A comprehensive Python toolkit for analyzing drought frequency and severity across Southern Africa using historical drought index data (SPI, SPEI). Optimized for the Lengau cluster at CHPC.

## Quick Start on Lengau

### 1. Setup the Project
```bash
# Make setup script executable and run it
chmod +x setup_lengau.sh
./setup_lengau.sh
```

### 2. Test the Installation
```bash
python test_setup.py
```

### 3. Submit the Analysis Job
```bash
qsub scripts/submit_drought_analysis.pbs
```

### 4. Monitor the Job
```bash
# Check job status
qstat -u $USER

# View job output
tail -f outputs/drought_analysis.out

# View job errors
tail -f outputs/drought_analysis.err
```

### 5. View Results
```bash
# List generated files
ls -la outputs/

# View the main drought frequency map
# (Download to your local machine to view)
```

## Project Structure

```
drought_analysis/
├── drought_indices.py              # Core drought calculation functions
├── visualization.py                # Mapping and visualization functions
├── figure_2_1_drought_analysis.py  # Main analysis script
├── setup_lengau.sh                 # Setup script for Lengau
├── test_setup.py                   # Installation test script
├── scripts/
│   └── submit_drought_analysis.pbs # PBS job submission script
├── data/                           # Data directory
├── outputs/                        # Output directory
└── examples/                       # Example scripts
```

## Job Configuration

The analysis is configured to run on the Lengau cluster with:
- **Queue**: normal
- **Resources**: 1 node, 8 CPUs, 32GB RAM
- **Walltime**: 2 hours
- **Modules**: Intel compilers, NetCDF, HDF5, Python 3.8

## Output Files

After successful completion, you'll find in the `outputs/` directory:

### Main Analysis
- `figure_2_1_main_drought_frequency.png` - Main drought frequency map
- `figure_2_1_interactive_map.html` - Interactive web map
- `figure_2_1_composite_map.png` - Composite frequency/severity map

### Additional Analysis
- `figure_2_1_multi_scale_comparison.png` - Multi-scale comparison
- `figure_2_1_severity_analysis.png` - Severity level analysis
- `figure_2_1_time_series_analysis.png` - Time series for key locations
- `figure_2_1_summary_statistics.png` - Statistical summary
- `figure_2_1_summary_statistics.csv` - Raw statistics data

### Job Information
- `drought_analysis.out` - Job output log
- `drought_analysis.err` - Job error log
- `analysis_summary.txt` - Analysis summary report

## Customizing the Analysis

### Modify Job Resources
Edit `scripts/submit_drought_analysis.pbs`:
```bash
#PBS -l select=1:ncpus=16:mem=64GB  # More resources
#PBS -l walltime=04:00:00           # Longer runtime
```

### Use Your Own Data
Modify `figure_2_1_drought_analysis.py` to load your data:
```python
# Replace sample data with your data
precip = xr.open_dataset('path/to/your/precipitation.nc')['precip']
temp = xr.open_dataset('path/to/your/temperature.nc')['temp']
```

### Adjust Analysis Parameters
```python
# Different time scales
scales = [1, 3, 6, 12, 24]  # months

# Different drought thresholds
thresholds = {
    'moderate': -1.0,
    'severe': -1.5,
    'extreme': -2.0
}
```

## Troubleshooting

### Common Issues

1. **Module loading errors**:
   ```bash
   # Check available modules
   module avail chpc/python
   module avail chpc/netcdf
   ```

2. **Python package installation issues**:
   ```bash
   # Install packages with user flag
   pip install --user package_name
   ```

3. **Job fails to start**:
   ```bash
   # Check queue status
   qstat -q
   
   # Check resource availability
   qstat -f
   ```

4. **Memory issues**:
   - Increase memory in PBS script: `#PBS -l mem=64GB`
   - Reduce chunk size in analysis script

5. **Long runtime**:
   - Increase walltime: `#PBS -l walltime=04:00:00`
   - Use more CPUs: `#PBS -l ncpus=16`

### Getting Help

1. **Check job logs**:
   ```bash
   cat outputs/drought_analysis.out
   cat outputs/drought_analysis.err
   ```

2. **Test individual components**:
   ```bash
   python -c "from drought_indices import DroughtIndices; print('OK')"
   ```

3. **Run interactive session**:
   ```bash
   qsub -I -l select=1:ncpus=4:mem=16GB -l walltime=01:00:00
   ```

## Data Sources

The toolkit can work with various climate data sources:

- **CHIRPS**: Climate Hazards Group InfraRed Precipitation with Station data
- **ERA5**: ECMWF Reanalysis v5
- **CRU**: Climate Research Unit datasets
- **Local station data**: CSV files with precipitation/temperature data

## Performance Tips

1. **For large datasets**:
   - Use appropriate chunk sizes for dask processing
   - Increase memory allocation
   - Use more CPUs for parallel processing

2. **For faster processing**:
   - Reduce spatial resolution
   - Process smaller time periods
   - Use fewer map features

## Citation

If you use this toolkit in your research:

```
Southern Africa Drought Analysis Toolkit
[Your Name/Institution]
[Year]
```

## Support

For questions or issues:
1. Check the job logs in `outputs/`
2. Run the test script: `python test_setup.py`
3. Check the troubleshooting section above

---

**Ready to run?** Execute `./setup_lengau.sh` to get started!







