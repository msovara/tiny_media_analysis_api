"""
IOD-Drought Analysis Workflow Setup Script

This script sets up the complete workflow environment and installs dependencies.

Author: Mthetho Sovara
Date: June 2025
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

class WorkflowSetup:
    """Setup class for the IOD-drought analysis workflow"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.data_dir = self.project_dir / 'data'
        self.output_dir = self.project_dir / 'output'
        
        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.data_dir / 'chirps').mkdir(exist_ok=True)
        (self.data_dir / 'era5').mkdir(exist_ok=True)
        (self.data_dir / 'modis').mkdir(exist_ok=True)
        (self.data_dir / 'iod').mkdir(exist_ok=True)
        (self.data_dir / 'processed').mkdir(exist_ok=True)
        
        (self.output_dir / 'spi').mkdir(exist_ok=True)
        (self.output_dir / 'spei').mkdir(exist_ok=True)
        (self.output_dir / 'ndvi').mkdir(exist_ok=True)
        (self.output_dir / 'maps').mkdir(exist_ok=True)
        (self.output_dir / 'plots').mkdir(exist_ok=True)
        (self.output_dir / 'processed').mkdir(exist_ok=True)
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("✗ Python 3.8 or higher is required")
            print(f"Current version: {version.major}.{version.minor}.{version.micro}")
            return False
        
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("\nInstalling dependencies...")
        
        # Check if requirements file exists
        requirements_file = self.project_dir / 'requirements_iod_analysis.txt'
        if not requirements_file.exists():
            print("✗ Requirements file not found")
            return False
        
        try:
            # Install packages
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ])
            print("✓ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            return False
    
    def create_config_file(self):
        """Create configuration file for the workflow"""
        print("\nCreating configuration file...")
        
        config_content = """# IOD-Drought Analysis Workflow Configuration

# Data directories
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

# Study period
START_YEAR = 1980
END_YEAR = 2020

# Southern Africa bounds
SOUTHERN_AFRICA_BOUNDS = {
    'lon_min': 10, 'lon_max': 40,
    'lat_min': -35, 'lat_max': -10
}

# Subregions
SUBREGIONS = {
    'southeastern': {'lat_min': -35, 'lat_max': -20, 'lon_min': 25, 'lon_max': 40},
    'central': {'lat_min': -25, 'lat_max': -15, 'lon_min': 20, 'lon_max': 30},
    'northwestern': {'lat_min': -20, 'lat_max': -10, 'lon_min': 10, 'lon_max': 25},
    'southwestern': {'lat_min': -35, 'lat_max': -20, 'lon_min': 10, 'lon_max': 25}
}

# Seasons
SEASONS = {
    'DJF': [12, 1, 2],
    'MAM': [3, 4, 5],
    'JJA': [6, 7, 8],
    'SON': [9, 10, 11]
}

# Drought index thresholds
DROUGHT_THRESHOLDS = {
    'extremely_dry': -2.0,
    'severely_dry': -1.5,
    'moderately_dry': -1.0,
    'mildly_dry': -0.5,
    'near_normal': 0.5,
    'moderately_wet': 1.0,
    'severely_wet': 1.5,
    'extremely_wet': 2.0
}

# IOD thresholds
IOD_THRESHOLDS = {
    'positive': 0.5,
    'negative': -0.5,
    'strong_positive': 1.0,
    'strong_negative': -1.0
}
"""
        
        config_file = self.project_dir / 'config.py'
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        print(f"✓ Configuration file created: {config_file}")
        return True
    
    def create_sample_data(self):
        """Create sample data for testing"""
        print("\nCreating sample data...")
        
        try:
            # Import and run sample data creation
            from data_download_workflow import DataDownloader
            
            downloader = DataDownloader(str(self.data_dir), str(self.output_dir))
            sample_files = downloader.create_sample_data()
            
            print("✓ Sample data created successfully")
            print("Sample files:")
            for data_type, file_path in sample_files.items():
                print(f"  {data_type}: {file_path}")
            
            return True
        except Exception as e:
            print(f"✗ Failed to create sample data: {e}")
            return False
    
    def run_test(self):
        """Run a quick test of the workflow"""
        print("\nRunning workflow test...")
        
        try:
            # Import and run main workflow
            from main_workflow import MainWorkflow
            
            workflow = MainWorkflow(str(self.data_dir), str(self.output_dir))
            success = workflow.run_quick_test()
            
            if success:
                print("✓ Workflow test completed successfully")
                return True
            else:
                print("✗ Workflow test failed")
                return False
        except Exception as e:
            print(f"✗ Workflow test failed: {e}")
            return False
    
    def create_readme(self):
        """Create README file with setup instructions"""
        print("\nCreating README file...")
        
        readme_content = """# IOD-Drought Correlation Analysis Workflow

## Quick Start

1. **Setup the workflow**:
   ```bash
   python setup_workflow.py
   ```

2. **Run the analysis**:
   ```bash
   python main_workflow.py
   ```

3. **Check results**:
   - Results are saved in the `output/` directory
   - Review the analysis report: `output/analysis_report.txt`

## Workflow Components

- `data_download_workflow.py` - Downloads climate and IOD data
- `drought_indices_calculation.py` - Calculates drought indices
- `iod_data_processing.py` - Processes IOD data
- `main_workflow.py` - Main orchestration script

## Data Sources

- **CHIRPS**: Precipitation data
- **ERA5**: Temperature data
- **MODIS**: NDVI data
- **JAMSTEC/NOAA/BOM**: IOD index data

## Requirements

- Python 3.8+
- See `requirements_iod_analysis.txt` for package dependencies

## Documentation

See `WORKFLOW_DOCUMENTATION.md` for detailed documentation.

## Support

For questions and issues, check the troubleshooting section in the documentation.
"""
        
        readme_file = self.project_dir / 'README.md'
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"✓ README file created: {readme_file}")
        return True
    
    def run_setup(self):
        """Run the complete setup process"""
        print("=" * 80)
        print("IOD-DROUGHT ANALYSIS WORKFLOW SETUP")
        print("=" * 80)
        
        # Check Python version
        if not self.check_python_version():
            print("Setup failed: Python version incompatible")
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            print("Setup failed: Could not install dependencies")
            return False
        
        # Create configuration file
        if not self.create_config_file():
            print("Setup failed: Could not create configuration file")
            return False
        
        # Create sample data
        if not self.create_sample_data():
            print("Setup failed: Could not create sample data")
            return False
        
        # Create README
        if not self.create_readme():
            print("Setup failed: Could not create README file")
            return False
        
        # Run test
        print("\n" + "=" * 80)
        print("RUNNING WORKFLOW TEST")
        print("=" * 80)
        
        if not self.run_test():
            print("Setup completed with warnings: Workflow test failed")
            print("You can still run the workflow manually")
        else:
            print("Setup completed successfully!")
        
        print("\n" + "=" * 80)
        print("SETUP COMPLETE")
        print("=" * 80)
        print("Next steps:")
        print("1. Run the workflow: python main_workflow.py")
        print("2. Check results in the output/ directory")
        print("3. Review the documentation: WORKFLOW_DOCUMENTATION.md")
        print("=" * 80)
        
        return True

def main():
    """Main function to run the setup"""
    print("IOD-Drought Analysis Workflow Setup")
    print("=" * 50)
    
    # Initialize setup
    setup = WorkflowSetup()
    
    # Ask user if they want to run the setup
    run_setup = input("Run the complete setup? (y/n): ").lower().strip() == 'y'
    
    if run_setup:
        setup.run_setup()
    else:
        print("Setup cancelled. You can run it later with: python setup_workflow.py")

if __name__ == "__main__":
    main()


















