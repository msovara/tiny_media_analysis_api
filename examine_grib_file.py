#!/usr/bin/env python3
"""
Examine GRIB File for IOD Workflow
This script examines the GRIB file to understand its structure and contents
"""

import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

def examine_grib_file(grib_file):
    """Examine the GRIB file structure and contents"""
    print("=" * 80)
    print("EXAMINING GRIB FILE FOR IOD WORKFLOW")
    print("=" * 80)
    
    if not Path(grib_file).exists():
        print(f"✗ GRIB file not found: {grib_file}")
        return None
    
    print(f"GRIB file: {grib_file}")
    print(f"File size: {Path(grib_file).stat().st_size / (1024**3):.2f} GB")
    
    try:
        # Try to open with xarray
        print("\nOpening GRIB file with xarray...")
        ds = xr.open_dataset(grib_file, engine='cfgrib')
        
        print("\nDataset structure:")
        print(f"Variables: {list(ds.data_vars)}")
        print(f"Coordinates: {list(ds.coords)}")
        print(f"Dimensions: {list(ds.dims)}")
        
        # Check each variable
        for var_name in ds.data_vars:
            var = ds[var_name]
            print(f"\nVariable: {var_name}")
            print(f"  Shape: {var.shape}")
            print(f"  Data type: {var.dtype}")
            print(f"  Long name: {var.attrs.get('long_name', 'Not specified')}")
            print(f"  Units: {var.attrs.get('units', 'Not specified')}")
            print(f"  Standard name: {var.attrs.get('standard_name', 'Not specified')}")
            
            # Check data range
            if var.size > 0:
                print(f"  Data range: {var.min().values:.3f} to {var.max().values:.3f}")
                print(f"  Valid data points: {var.count().values}")
                print(f"  Total points: {var.size}")
                print(f"  Missing data: {var.size - var.count().values}")
        
        # Check coordinates
        print(f"\nCoordinates:")
        for coord_name in ds.coords:
            coord = ds[coord_name]
            print(f"  {coord_name}:")
            print(f"    Shape: {coord.shape}")
            print(f"    Range: {coord.min().values:.3f} to {coord.max().values:.3f}")
            print(f"    Units: {coord.attrs.get('units', 'Not specified')}")
        
        # Check time information
        if 'time' in ds.coords:
            time_coord = ds.time
            print(f"\nTime information:")
            print(f"  Time range: {time_coord.min().values} to {time_coord.max().values}")
            print(f"  Number of time steps: {len(time_coord)}")
            print(f"  Time units: {time_coord.attrs.get('units', 'Not specified')}")
        
        # Check spatial information
        if 'latitude' in ds.coords and 'longitude' in ds.coords:
            lat = ds.latitude
            lon = ds.longitude
            print(f"\nSpatial information:")
            print(f"  Latitude range: {lat.min().values:.3f} to {lat.max().values:.3f}")
            print(f"  Longitude range: {lon.min().values:.3f} to {lon.max().values:.3f}")
            print(f"  Spatial resolution: {lat.shape[0]} x {lon.shape[0]}")
        
        return ds
        
    except Exception as e:
        print(f"✗ Error opening GRIB file: {e}")
        print("\nTrying alternative methods...")
        
        # Try with different engines
        try:
            print("Trying with pygrib...")
            import pygrib
            grbs = pygrib.open(grib_file)
            
            print(f"Number of messages: {grbs.messages}")
            
            # Read first few messages
            for i in range(min(5, grbs.messages)):
                grb = grbs[i+1]
                print(f"\nMessage {i+1}:")
                print(f"  Parameter: {grb.parameterName}")
                print(f"  Level: {grb.level}")
                print(f"  Date: {grb.date}")
                print(f"  Time: {grb.time}")
                print(f"  Grid: {grb.gridType}")
                print(f"  Shape: {grb.values.shape}")
                
            grbs.close()
            return "pygrib_success"
            
        except ImportError:
            print("pygrib not available")
        except Exception as e2:
            print(f"pygrib also failed: {e2}")
        
        return None

def check_iod_suitability(ds):
    """Check if the GRIB data is suitable for IOD analysis"""
    print("\n" + "=" * 80)
    print("CHECKING IOD SUITABILITY")
    print("=" * 80)
    
    if ds is None:
        print("✗ Cannot check IOD suitability - no dataset available")
        return False
    
    # Check for sea surface temperature
    sst_vars = []
    for var_name in ds.data_vars:
        var = ds[var_name]
        long_name = var.attrs.get('long_name', '').lower()
        standard_name = var.attrs.get('standard_name', '').lower()
        
        if any(keyword in long_name for keyword in ['sea surface temperature', 'sst', 'temperature']):
            sst_vars.append(var_name)
        elif any(keyword in standard_name for keyword in ['sea_surface_temperature', 'sst']):
            sst_vars.append(var_name)
    
    if sst_vars:
        print(f"✓ Found potential SST variables: {sst_vars}")
    else:
        print("✗ No obvious SST variables found")
        print("Available variables:")
        for var_name in ds.data_vars:
            var = ds[var_name]
            print(f"  {var_name}: {var.attrs.get('long_name', 'No description')}")
    
    # Check spatial coverage
    if 'latitude' in ds.coords and 'longitude' in ds.coords:
        lat = ds.latitude
        lon = ds.longitude
        
        # Check if data covers Indian Ocean
        indian_ocean_lat = (-30 <= lat.min().values <= 30) and (-30 <= lat.max().values <= 30)
        indian_ocean_lon = (20 <= lon.min().values <= 120) or (lon.min().values <= -60 and lon.max().values >= 20)
        
        if indian_ocean_lat and indian_ocean_lon:
            print("✓ Spatial coverage includes Indian Ocean region")
        else:
            print("✗ Spatial coverage may not include Indian Ocean region")
            print(f"  Latitude range: {lat.min().values:.1f} to {lat.max().values:.1f}")
            print(f"  Longitude range: {lon.min().values:.1f} to {lon.max().values:.1f}")
    
    # Check temporal coverage
    if 'time' in ds.coords:
        time_coord = ds.time
        print(f"✓ Temporal coverage: {len(time_coord)} time steps")
        print(f"  From: {time_coord.min().values}")
        print(f"  To: {time_coord.max().values}")
    
    return len(sst_vars) > 0

def main():
    """Main function"""
    grib_file = "efbe0129656fb09397fc72a81ab486f3.grib"
    
    print("GRIB File Examination for IOD Workflow")
    print("=" * 50)
    
    # Examine the GRIB file
    ds = examine_grib_file(grib_file)
    
    # Check IOD suitability
    if ds is not None and ds != "pygrib_success":
        check_iod_suitability(ds)
    
    print("\n" + "=" * 80)
    print("EXAMINATION COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
