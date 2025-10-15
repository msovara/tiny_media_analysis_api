"""
Test Installation Script

This script tests if all dependencies are properly installed and
the drought analysis toolkit is working correctly.

Author: Drought Analysis Toolkit
"""

import sys
import importlib
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")
    
    required_packages = [
        'numpy', 'pandas', 'scipy', 'matplotlib', 'seaborn',
        'xarray', 'netcdf4', 'rasterio', 'geopandas', 'shapely',
        'cartopy', 'folium', 'plotly'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✓ {package}")
        except ImportError as e:
            print(f"  ✗ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\nFailed to import: {failed_imports}")
        print("Please install missing packages with: pip install -r requirements.txt")
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
        from data_processing import ClimateDataProcessor
        print("  ✓ data_processing")
    except ImportError as e:
        print(f"  ✗ data_processing: {e}")
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
        
        # Test drought frequency
        print("  - Calculating drought frequency...")
        freq = drought_calc.calculate_drought_frequency(spi, threshold=-1.0)
        print(f"    ✓ Drought frequency calculated: {freq.shape}")
        
        # Test visualization
        print("  - Testing visualization...")
        from visualization import DroughtVisualizer
        visualizer = DroughtVisualizer()
        print("    ✓ Visualizer created")
        
        print("\n✓ Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"\n✗ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_output_directory():
    """Test if output directory can be created"""
    print("\nTesting output directory...")
    
    try:
        output_dir = Path('outputs')
        output_dir.mkdir(exist_ok=True)
        print(f"  ✓ Output directory created: {output_dir.absolute()}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create output directory: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SOUTHERN AFRICA DROUGHT ANALYSIS - INSTALLATION TEST")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("Custom Modules", test_drought_modules),
        ("Basic Functionality", test_basic_functionality),
        ("Output Directory", test_output_directory)
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
        print("1. Run: python figure_2_1_drought_analysis.py")
        print("2. Check the outputs/ directory for generated maps")
        print("3. Open outputs/figure_2_1_interactive_map.html in your browser")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check that you're in the correct directory")
        print("3. Ensure all files are present")

if __name__ == "__main__":
    main()







