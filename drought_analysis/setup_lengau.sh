#!/bin/bash
# Setup script for Southern Africa Drought Analysis on Lengau Cluster

echo "=========================================="
echo "Setting up Drought Analysis on Lengau"
echo "=========================================="

# Create necessary directories
echo "Creating project directories..."
mkdir -p {data,outputs,examples,scripts}

# Make scripts executable
chmod +x scripts/*.pbs

# Load required modules
echo "Loading required modules..."
module load chpc/parallel_studio_xe/16.0.1/2016.1.150
module load chpc/netcdf/4.4.3-F/intel/16.0.1
module load chpc/hdf5/1.8.16/intel/16.0.1
module load chpc/python/3.8.0

# Check Python environment
echo "Checking Python environment..."
python --version

# Install required Python packages
echo "Installing Python packages..."
pip install --user numpy pandas scipy matplotlib seaborn
pip install --user xarray netcdf4 rasterio geopandas shapely
pip install --user cartopy pyproj folium plotly
pip install --user cftime dask requests tqdm

# Test installation
echo "Testing installation..."
python -c "
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib
import cartopy
print('✓ All packages imported successfully!')
"

# Create a simple test script
cat > test_setup.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify the drought analysis setup on Lengau
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    required_packages = [
        'numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn',
        'xarray', 'netcdf4', 'cartopy', 'folium'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError as e:
            print(f"  ✗ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {failed_imports}")
        return False
    else:
        print("\n✓ All packages imported successfully!")
        return True

def test_drought_modules():
    """Test if our custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from drought_indices import DroughtIndices, create_sample_data
        print("  ✓ drought_indices")
    except ImportError as e:
        print(f"  ✗ drought_indices: {e}")
        return False
    
    try:
        from visualization import DroughtVisualizer
        print("  ✓ visualization")
    except ImportError as e:
        print(f"  ✗ visualization: {e}")
        return False
    
    print("\n✓ All custom modules imported successfully!")
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test sample data creation
        from drought_indices import create_sample_data, DroughtIndices
        
        print("  - Creating sample data...")
        precip, temp = create_sample_data()
        print(f"    ✓ Sample data created: {precip.shape}, {temp.shape}")
        
        # Test SPI calculation
        print("  - Calculating SPI...")
        drought_calc = DroughtIndices()
        spi = drought_calc.calculate_spi(precip, scale=3)
        print(f"    ✓ SPI calculated: {spi.shape}")
        
        print("\n✓ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("DROUGHT ANALYSIS SETUP TEST - LENGAU CLUSTER")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Custom Modules", test_drought_modules),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The toolkit is ready to use.")
        print("\nNext steps:")
        print("1. Submit job: qsub scripts/submit_drought_analysis.pbs")
        print("2. Check job status: qstat -u $USER")
        print("3. View results in outputs/ directory")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()
EOF

chmod +x test_setup.py

echo "=========================================="
echo "Setup completed!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test the setup: python test_setup.py"
echo "2. Submit the analysis job: qsub scripts/submit_drought_analysis.pbs"
echo "3. Check job status: qstat -u \$USER"
echo "4. View results in outputs/ directory"
echo ""
echo "Project structure:"
echo "├── drought_indices.py          # Core drought calculation functions"
echo "├── visualization.py            # Mapping and visualization functions"
echo "├── figure_2_1_drought_analysis.py  # Main analysis script"
echo "├── scripts/submit_drought_analysis.pbs  # Job submission script"
echo "├── test_setup.py               # Setup test script"
echo "├── data/                       # Data directory"
echo "├── outputs/                    # Output directory"
echo "└── examples/                   # Example scripts"
echo ""
echo "For help, check the README.md file"







