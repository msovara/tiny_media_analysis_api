# FlexNet License Server Setup Guide for CHPC

## Overview
This guide covers setting up a FlexNet license server for software products at CHPC using either `chpclic1` or `login1` without requiring root access.

## Prerequisites
- Access to either `chpclic1` or `login1` server
- License server software (RLM - Reprise License Manager)
- MAC address of the network adapter for server identification

## Step 1: Choose Your License Server
Decide which server to use:
- **chpclic1** - Dedicated license server
- **login1** - Login node (alternative option)

## Step 2: Get MAC Address
The MAC address is crucial for FlexNet license server identification.

```bash
# Get MAC address of network interfaces
ifconfig -a

# Or using ip command
ip addr show

# Look for entries like:
# ether 00:15:5d:01:ca:05  # This is your MAC address
```

**Important**: Note down the MAC address of the primary network interface (usually `eth0` or `ens192`).

## Step 3: Install License Server Software

Based on your current directory (`/home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1`), you have RLM installed.

### Check Installation
```bash
cd /home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1
ls -la
```

### Install if needed
```bash
# Run the installation script
./dinst

# Follow the prompts to install RLM
```

## Step 4: Configure License Server

### Create License File
Create a license file (e.g., `license.lic`) with your vendor's license information:

```
SERVER <hostname> <mac_address> <port>
VENDOR <vendor_name> <path_to_vendor_daemon>
FEATURE <feature_name> <vendor_name> <version> <expiry_date> <num_licenses> <hostid=MAC_ADDRESS>
```

### Example License File
```
SERVER chpclic1 00155d01ca05 5053
VENDOR example_vendor /home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1/bin/example_vendor
FEATURE example_feature example_vendor 1.0 31-dec-2025 10 HOSTID=00155d01ca05
```

## Step 5: Start License Server

### Start RLM Daemon
```bash
# Start the license server
./bin/rlm -c /path/to/license.lic -dlog /path/to/rlm.log

# Or run in background
nohup ./bin/rlm -c /path/to/license.lic -dlog /path/to/rlm.log &
```

### Verify Server is Running
```bash
# Check if process is running
ps aux | grep rlm

# Check port is listening
netstat -tlnp | grep 5053
```

## Step 6: Configure Client Applications

### Set Environment Variables
Add to your shell profile (`.bashrc`, `.bash_profile`, etc.):

```bash
export LM_LICENSE_FILE=5053@chpclic1
# or
export LM_LICENSE_FILE=5053@login1
```

### Test License Server
```bash
# Test connection to license server
./bin/rlmutil lmstat -a -c 5053@chpclic1
```

## Step 7: Troubleshooting

### Common Issues
1. **Port already in use**: Change port number in license file
2. **MAC address mismatch**: Verify MAC address is correct
3. **Permission denied**: Check file permissions
4. **Network connectivity**: Ensure firewall allows the port

### Debug Commands
```bash
# Check license server status
./bin/rlmutil lmstat -a -c 5053@chpclic1

# Check license server logs
tail -f /path/to/rlm.log

# Test network connectivity
telnet chpclic1 5053
```

## Step 8: Automation (Optional)

### Create Startup Script
Create a script to automatically start the license server:

```bash
#!/bin/bash
# /home/apps/chpc/earth/RLM-3D/start_license_server.sh

cd /home/apps/chpc/earth/RLM-3D/aksusbd-10.11.1
./bin/rlm -c /path/to/license.lic -dlog /path/to/rlm.log &
echo "License server started with PID: $!"
```

### Make it executable
```bash
chmod +x /home/apps/chpc/earth/RLM-3D/start_license_server.sh
```

## Important Notes

1. **MAC Address**: Must match exactly what's in your license file
2. **Port**: Default is 5053, but can be changed if needed
3. **Hostname**: Use the actual hostname of your chosen server
4. **Logs**: Keep logs for troubleshooting
5. **Backup**: Keep backup of license files and configuration

## Next Steps

1. Get the MAC address of your chosen server
2. Obtain the license file from your software vendor
3. Install and configure the license server
4. Test the setup
5. Configure client applications to use the license server

## Support

For CHPC-specific issues, contact your system administrators.
For FlexNet/RLM issues, refer to the vendor documentation.


