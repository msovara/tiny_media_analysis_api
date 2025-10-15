#!/bin/bash
# Script to get MAC address for FlexNet license server setup
# Run this on the server you want to use as license server (chpclic1 or login1)

echo "=== MAC Address Finder for FlexNet License Server ==="
echo ""

# Get hostname
HOSTNAME=$(hostname)
echo "Current hostname: $HOSTNAME"
echo ""

# Get all network interfaces and their MAC addresses
echo "Network interfaces and MAC addresses:"
echo "====================================="

# Method 1: Using ip command (modern)
echo "Method 1 - Using 'ip addr show':"
ip addr show | grep -E "^[0-9]+:|ether" | grep -B1 "ether" | grep -v "^--$" | while read line; do
    if [[ $line =~ ^[0-9]+: ]]; then
        echo ""
        echo -n "Interface: "
        echo $line | cut -d: -f2 | cut -d@ -f1
    elif [[ $line =~ ether ]]; then
        echo -n "MAC Address: "
        echo $line | awk '{print $2}'
    fi
done

echo ""
echo "Method 2 - Using 'ifconfig':"
ifconfig -a | grep -E "^[a-zA-Z0-9]+|ether" | while read line; do
    if [[ $line =~ ^[a-zA-Z0-9]+ ]]; then
        echo ""
        echo -n "Interface: "
        echo $line | cut -d: -f1
    elif [[ $line =~ ether ]]; then
        echo -n "MAC Address: "
        echo $line | awk '{print $2}'
    fi
done

echo ""
echo "=== Recommended MAC Address ==="
echo "For FlexNet license server, use the MAC address of your primary network interface."
echo "This is usually:"
echo "  - eth0 (older systems)"
echo "  - ens192, ens224, or similar (newer systems)"
echo "  - The interface that shows an IP address when you run 'ip addr show'"
echo ""

# Show interfaces with IP addresses
echo "Interfaces with IP addresses:"
ip addr show | grep -E "^[0-9]+:|inet " | grep -B1 "inet " | grep -v "^--$" | while read line; do
    if [[ $line =~ ^[0-9]+: ]]; then
        echo ""
        echo -n "Interface: "
        echo $line | cut -d: -f2 | cut -d@ -f1
    elif [[ $line =~ inet ]]; then
        echo -n "IP Address: "
        echo $line | awk '{print $2}'
    fi
done

echo ""
echo "=== Next Steps ==="
echo "1. Choose the MAC address of your primary network interface"
echo "2. Use this MAC address in your FlexNet license file"
echo "3. Make sure the hostname matches: $HOSTNAME"
echo ""
echo "Example license file entry:"
echo "SERVER $HOSTNAME <MAC_ADDRESS> 5053"


