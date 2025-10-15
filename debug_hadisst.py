#!/usr/bin/env python3
"""
Debug HadISST Data
This script helps debug the HadISST data structure and coordinates
"""

import xarray as xr
import numpy as np
import pandas as pd

def debug_hadisst():
    """Debug HadISST data structure"""
    print("=" * 60)
    print("DEBUGGING HADISST DATA")
    print("=" * 60)
    
    # Load the data
    ds = xr.open_dataset('HadISST_sst.nc')
    
    print("Dataset info:")
    print(f"Variables: {list(ds.data_vars)}")
    print(f"Coordinates: {list(ds.coords)}")
    print(f"Dimensions: {list(ds.dims)}")
    
    # Check SST data
    sst = ds.sst
    print(f"\nSST data:")
    print(f"Shape: {sst.shape}")
    print(f"Data type: {sst.dtype}")
    print(f"Fill value: {sst.attrs.get('_FillValue', 'Not specified')}")
    print(f"Missing value: {sst.attrs.get('missing_value', 'Not specified')}")
    
    # Check coordinates
    print(f"\nCoordinates:")
    print(f"Time: {sst.time.min().values} to {sst.time.max().values}")
    print(f"Latitude: {sst.latitude.min().values:.1f} to {sst.latitude.max().values:.1f}")
    print(f"Longitude: {sst.longitude.min().values:.1f} to {sst.longitude.max().values:.1f}")
    
    # Check data values
    print(f"\nData values:")
    print(f"SST range: {sst.min().values:.3f} to {sst.max().values:.3f}")
    print(f"Valid data points: {sst.count().values}")
    print(f"Total points: {sst.size}")
    print(f"Missing data: {sst.size - sst.count().values}")
    
    # Check specific regions
    print(f"\nIOD Regions:")
    
    # Western region (50°E-70°E, 10°S-10°N)
    western_sst = sst.sel(
        longitude=slice(50, 70),
        latitude=slice(-10, 10)
    )
    print(f"Western region shape: {western_sst.shape}")
    print(f"Western region valid points: {western_sst.count().values}")
    
    # Eastern region (90°E-110°E, 10°S-0°N)
    eastern_sst = sst.sel(
        longitude=slice(90, 110),
        latitude=slice(-10, 0)
    )
    print(f"Eastern region shape: {eastern_sst.shape}")
    print(f"Eastern region valid points: {eastern_sst.count().values}")
    
    # Check a specific time slice
    print(f"\nSample data (first time step):")
    sample_sst = sst.isel(time=0)
    print(f"Sample SST range: {sample_sst.min().values:.3f} to {sample_sst.max().values:.3f}")
    print(f"Sample valid points: {sample_sst.count().values}")
    
    # Check IOD regions for first time step
    western_sample = western_sst.isel(time=0)
    eastern_sample = eastern_sst.isel(time=0)
    
    print(f"\nIOD regions (first time step):")
    print(f"Western sample valid points: {western_sample.count().values}")
    print(f"Eastern sample valid points: {eastern_sample.count().values}")
    
    if western_sample.count().values > 0:
        print(f"Western sample SST range: {western_sample.min().values:.3f} to {western_sample.max().values:.3f}")
    else:
        print("Western region has no valid data!")
        
    if eastern_sample.count().values > 0:
        print(f"Eastern sample SST range: {eastern_sample.min().values:.3f} to {eastern_sample.max().values:.3f}")
    else:
        print("Eastern region has no valid data!")
    
    # Check if we need to convert longitude
    print(f"\nLongitude conversion check:")
    if sst.longitude.min().values >= 0:
        print("Longitude is in 0-360 format")
        print("IOD regions should be:")
        print("Western: 50°E-70°E (50-70)")
        print("Eastern: 90°E-110°E (90-110)")
    else:
        print("Longitude is in -180 to 180 format")
        print("IOD regions should be:")
        print("Western: 50°E-70°E (50-70)")
        print("Eastern: 90°E-110°E (90-110)")
    
    return ds

if __name__ == "__main__":
    debug_hadisst()
















