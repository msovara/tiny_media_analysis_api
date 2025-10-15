#!/bin/bash
# Install RLM3D in system location with temporary world-writable permissions

echo "=== Installing RLM3D in System Location ==="

# Create directory structure
mkdir -p /home/apps/chpc/earth/rlm3d/bin
mkdir -p /home/apps/chpc/earth/rlm3d/lib
mkdir -p /home/apps/chpc/earth/rlm3d/include

# Set temporary world-writable permissions
chmod 777 /home/apps/chpc/earth/rlm3d
chmod 777 /home/apps/chpc/earth/rlm3d/bin
chmod 777 /home/apps/chpc/earth/rlm3d/lib
chmod 777 /home/apps/chpc/earth/rlm3d/include

echo "✓ Created directory structure with world-writable permissions"

# Copy RLM3D executable
cp RLM3D_v3.3.2 /home/apps/chpc/earth/rlm3d/bin/
chmod 755 /home/apps/chpc/earth/rlm3d/bin/RLM3D_v3.3.2

echo "✓ Copied RLM3D executable"

# Remove world-writable permissions
chmod 755 /home/apps/chpc/earth/rlm3d
chmod 755 /home/apps/chpc/earth/rlm3d/bin
chmod 755 /home/apps/chpc/earth/rlm3d/lib
chmod 755 /home/apps/chpc/earth/rlm3d/include

echo "✓ Removed world-writable permissions"

# Update module file with correct filename
cp rlm3d_module_file /apps/chpc/scripts/modules/earth/rlm3d/3.3.2

echo "✓ Updated module file"

echo "=== Installation Complete ==="
echo "RLM3D installed at: /home/apps/chpc/earth/rlm3d/"
echo "Module available as: module load chpc/earth/rlm3d/3.3.2"

























