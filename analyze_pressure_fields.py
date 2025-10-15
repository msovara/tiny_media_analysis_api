#!/usr/bin/env python3
"""
Comprehensive analysis of GRIB pressure field datasets for AI weather training.
"""

import xarray as xr
import numpy as np
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

def analyze_grib_file(filepath):
    """Analyze a single GRIB file and return comprehensive information."""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {os.path.basename(filepath)}")
    print(f"{'='*60}")
    
    try:
        # Load dataset
        ds = xr.open_dataset(filepath, engine='cfgrib')
        
        # Basic information
        print(f"\n📊 BASIC INFORMATION")
        print(f"Variables: {list(ds.data_vars.keys())}")
        print(f"Dimensions: {dict(ds.dims)}")
        print(f"Shape: {ds.sizes}")
        print(f"File size: {os.path.getsize(filepath) / (1024**3):.2f} GB")
        
        # Time information
        print(f"\n⏰ TIME INFORMATION")
        print(f"Time range: {ds.time.min().values} to {ds.time.max().values}")
        print(f"Time steps: {len(ds.time)}")
        print(f"Time frequency: ~{len(ds.time) / 15:.1f} timesteps per year")
        
        # Spatial information
        print(f"\n🌍 SPATIAL INFORMATION")
        print(f"Latitude range: {ds.latitude.min().values:.2f}° to {ds.latitude.max().values:.2f}°")
        print(f"Longitude range: {ds.longitude.min().values:.2f}° to {ds.longitude.max().values:.2f}°")
        print(f"Resolution: ~{180/ds.latitude.size:.3f}° x {360/ds.longitude.size:.3f}°")
        print(f"Grid points: {ds.latitude.size} x {ds.longitude.size}")
        
        # Variable analysis
        print(f"\n📈 VARIABLE ANALYSIS")
        variable_info = {
            'z': 'Geopotential height (m²/s²)',
            't': 'Temperature (K)',
            'u': 'Zonal wind (m/s)',
            'v': 'Meridional wind (m/s)',
            'w': 'Vertical wind (m/s)',
            'r': 'Relative humidity (%)',
            'q': 'Specific humidity (kg/kg)'
        }
        
        for var in ds.data_vars:
            if var in variable_info:
                print(f"\n{var.upper()} - {variable_info[var]}")
                data = ds[var]
                print(f"  Shape: {data.shape}")
                print(f"  Data type: {data.dtype}")
                print(f"  Min: {data.min().values:.3f}")
                print(f"  Max: {data.max().values:.3f}")
                print(f"  Mean: {data.mean().values:.3f}")
                print(f"  Std: {data.std().values:.3f}")
                
                # Check for missing values
                missing = data.isnull().sum().values
                print(f"  Missing values: {missing}")
                
                # Check for infinite values
                inf_count = np.isinf(data).sum().values
                print(f"  Infinite values: {inf_count}")
        
        # Data quality summary
        print(f"\n✅ DATA QUALITY SUMMARY")
        total_points = ds.sizes['time'] * ds.sizes['latitude'] * ds.sizes['longitude']
        print(f"Total data points per variable: {total_points:,}")
        
        # Check for any missing data
        has_missing = False
        for var in ds.data_vars:
            if ds[var].isnull().any():
                has_missing = True
                break
        
        if has_missing:
            print("⚠️  WARNING: Some variables contain missing values")
        else:
            print("✅ No missing values detected")
        
        # Memory usage estimate
        memory_gb = sum(ds[var].nbytes for var in ds.data_vars) / (1024**3)
        print(f"Estimated memory usage: {memory_gb:.2f} GB")
        
        return ds
        
    except Exception as e:
        print(f"❌ ERROR reading {filepath}: {e}")
        return None

def compare_files(ds1, ds2, file1, file2):
    """Compare two datasets."""
    print(f"\n{'='*60}")
    print("COMPARING DATASETS")
    print(f"{'='*60}")
    
    if ds1 is None or ds2 is None:
        print("❌ Cannot compare - one or both datasets failed to load")
        return
    
    # Compare structures
    print(f"\n🔍 STRUCTURE COMPARISON")
    print(f"Same variables: {set(ds1.data_vars.keys()) == set(ds2.data_vars.keys())}")
    print(f"Same dimensions: {ds1.sizes == ds2.sizes}")
    print(f"Same coordinates: {set(ds1.coords.keys()) == set(ds2.coords.keys())}")
    
    # Compare time ranges
    print(f"\n⏰ TIME COMPARISON")
    print(f"File 1 time range: {ds1.time.min().values} to {ds1.time.max().values}")
    print(f"File 2 time range: {ds2.time.min().values} to {ds2.time.max().values}")
    
    # Check for overlap
    time_overlap = not (ds1.time.max() < ds2.time.min() or ds2.time.max() < ds1.time.min())
    print(f"Time overlap: {time_overlap}")
    
    if time_overlap:
        print("⚠️  WARNING: Time periods overlap - may contain duplicate data")

def create_training_summary(ds):
    """Create a summary suitable for AI training pipeline."""
    print(f"\n{'='*60}")
    print("AI TRAINING PIPELINE SUMMARY")
    print(f"{'='*60}")
    
    if ds is None:
        print("❌ No dataset available for training summary")
        return
    
    # Training dataset characteristics
    print(f"\n🤖 TRAINING DATASET CHARACTERISTICS")
    print(f"Time period: {ds.time.min().values} to {ds.time.max().values}")
    print(f"Total timesteps: {len(ds.time)}")
    print(f"Spatial resolution: {ds.latitude.size} x {ds.longitude.size}")
    print(f"Variables: {len(ds.data_vars)} atmospheric variables")
    print(f"Data type: {list(ds.data_vars.values())[0].dtype}")
    
    # Memory requirements
    total_size_gb = sum(ds[var].nbytes for var in ds.data_vars) / (1024**3)
    print(f"\n💾 MEMORY REQUIREMENTS")
    print(f"Single file size: {total_size_gb:.2f} GB")
    print(f"Both files size: {total_size_gb * 2:.2f} GB")
    
    # Training recommendations
    print(f"\n🎯 TRAINING RECOMMENDATIONS")
    print(f"• Use data chunking for memory efficiency")
    print(f"• Consider temporal subsampling (e.g., 6-hourly)")
    print(f"• Implement spatial downsampling if needed")
    print(f"• Use mixed precision training (float16)")
    print(f"• Consider data augmentation techniques")
    
    # Variable importance for weather prediction
    print(f"\n🌦️  VARIABLE IMPORTANCE FOR WEATHER PREDICTION")
    importance = {
        'z': 'High - Geopotential height (pressure patterns)',
        't': 'High - Temperature (thermal dynamics)',
        'u': 'High - Zonal wind (horizontal motion)',
        'v': 'High - Meridional wind (vertical motion)',
        'w': 'Medium - Vertical wind (convection)',
        'r': 'Medium - Relative humidity (moisture)',
        'q': 'Medium - Specific humidity (moisture)'
    }
    
    for var in ds.data_vars:
        if var in importance:
            print(f"• {var.upper()}: {importance[var]}")

def main():
    """Main analysis function."""
    print("🌦️  PRESSURE FIELD DATASET ANALYSIS")
    print("=" * 60)
    
    # Find GRIB files
    grib_files = [f for f in os.listdir('.') if f.endswith('.grib')]
    print(f"Found {len(grib_files)} GRIB files: {grib_files}")
    
    if not grib_files:
        print("❌ No GRIB files found in current directory")
        return
    
    # Analyze each file
    datasets = []
    for i, file in enumerate(grib_files):
        ds = analyze_grib_file(file)
        datasets.append(ds)
    
    # Compare files if we have multiple
    if len(datasets) == 2:
        compare_files(datasets[0], datasets[1], grib_files[0], grib_files[1])
    
    # Create training summary
    if datasets[0] is not None:
        create_training_summary(datasets[0])
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()













