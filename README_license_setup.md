# FlexNet License Server Setup - Quick Reference

This directory contains scripts to help you set up and manage a FlexNet license server at CHPC.

## Scripts Overview

### 1. `get_mac_address.sh`
**Purpose**: Get the MAC address of your server for license file configuration
**Usage**: Run on your chosen license server (chpclic1 or login1)
```bash
chmod +x get_mac_address.sh
./get_mac_address.sh
```

### 2. `start_license_server.sh`
**Purpose**: Start the FlexNet license server
**Usage**: Run on your license server after creating the license file
```bash
chmod +x start_license_server.sh
./start_license_server.sh
```

### 3. `check_license_server.sh`
**Purpose**: Check if the license server is running correctly
**Usage**: Run anytime to verify server status
```bash
chmod +x check_license_server.sh
./check_license_server.sh
```

### 4. `stop_license_server.sh`
**Purpose**: Safely stop the license server
**Usage**: Run when you need to stop the server
```bash
chmod +x stop_license_server.sh
./stop_license_server.sh
```

## Quick Setup Steps

1. **Choose your server**: Decide between `chpclic1` or `login1`

2. **Get MAC address**: 
   ```bash
   ./get_mac_address.sh
   ```

3. **Create license file**: Use the MAC address and hostname in your vendor's license file

4. **Start server**:
   ```bash
   ./start_license_server.sh
   ```

5. **Verify setup**:
   ```bash
   ./check_license_server.sh
   ```

6. **Configure clients**: Set environment variable:
   ```bash
   export LM_LICENSE_FILE=5053@your_server_name
   ```

## Important Notes

- **MAC Address**: Must match exactly in your license file
- **Hostname**: Use the actual hostname of your chosen server
- **Port**: Default is 5053, but can be changed if needed
- **No Root Access**: All scripts work without root privileges

## Troubleshooting

- Use `check_license_server.sh` to diagnose issues
- Check log files for error messages
- Verify MAC address and hostname in license file
- Ensure firewall allows the license port

## Support

For CHPC-specific issues, contact your system administrators.
For FlexNet/RLM issues, refer to the vendor documentation.


