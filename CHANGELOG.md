# Changelog

All notable changes to the ARWpost installation project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1] - 2024-08-28

### ✅ Added
- **Production-ready ARWpost installation** on Lengau cluster
- **Clean module system** with single module path `chpc/earth/arwpost/3.1`
- **Intel Parallel Studio XE 16.0.1** compiler optimization
- **NetCDF 4.4.0-C integration** with Intel 16.0.1 build
- **Minimal compilation approach** for core calculation modules
- **Comprehensive documentation** with usage examples
- **PBS job script templates** for cluster computing
- **Environment module integration** with automatic dependency loading
- **Wrapper script** (`run_arwpost`) for easy execution

### 🔧 Fixed
- **Tcl syntax errors** in module file - resolved all variable expansion issues
- **Module dependency conflicts** - optimized loading order (Intel → zlib → HDF5 → NetCDF)
- **NetCDF linking issues** - explicit library paths and linking flags
- **File permission issues** - proper permissions for all files
- **Broken symlinks** - cleaned up module system
- **Duplicate files** - removed backup files and duplicates

### 🚫 Removed
- **Default module symlinks** - simplified to single module path
- **Backup files** - cleaned up module directory
- **Broken symlinks** - removed all broken links
- **Temporary files** - cleaned installation directory
- **Complex module dependencies** - excluded problematic modules

### 📊 Technical Details
- **Compiler**: Intel Parallel Studio XE 16.0.1
- **NetCDF**: 4.4.0-C with Intel 16.0.1
- **HDF5**: 1.8.16 with Intel 16.0.1
- **zlib**: 1.2.8 with Intel 16.0.1
- **Installation Path**: `/home/apps/chpc/earth/ARWpost`
- **Module Path**: `/apps/chpc/scripts/modules/earth/arwpost/3.1`

### 🎯 Available Calculation Modules
- CAPE (Convective Available Potential Energy)
- Cloud fraction calculations
- Radar reflectivity (dBZ)
- Height calculations
- Pressure calculations
- Relative humidity (surface and 2m)
- Sea level pressure
- Temperature conversions
- Dew point calculations
- Potential temperature
- Kinetic energy
- Wind components (u, v)
- Wind direction
- Wind speed

### 📁 File Structure
```
/home/apps/chpc/earth/ARWpost/
├── bin/
│   ├── ARWpost                    # Main executable
│   └── run_arwpost               # Wrapper script
└── share/arwpost/                # Source files and documentation

/apps/chpc/scripts/modules/earth/arwpost/
└── 3.1                          # Module file (only option)
```

### 🔍 Verification Results
- ✅ Module loads cleanly without errors
- ✅ ARWpost executes successfully
- ✅ All calculation modules functional
- ✅ Environment variables set correctly
- ✅ PBS job submission works
- ✅ Production-ready for research use

### 📚 Documentation
- Complete installation guide
- Usage examples and workflows
- PBS job script templates
- Technical specifications
- Troubleshooting information

## [3.0] - 2024-08-21

### 🔧 Initial Development
- Initial repository setup
- Basic installation scripts
- Module file creation
- Documentation framework

---

**Status**: ✅ Production Ready  
**Last Updated**: August 28, 2024  
**Cluster**: Lengau (CHPC)  
**Maintainer**: msovara
