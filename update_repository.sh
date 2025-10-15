#!/bin/bash

# Update Repository Script
# This script updates the GitHub repository with new documentation

set -e

echo "🔄 === Updating GitHub Repository ==="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Not in the repository root directory"
    echo "Please run this script from the repository root"
    exit 1
fi

echo "✅ In repository root directory"

# Backup current README
echo "📁 === Backing Up Current Files ==="
if [ -f "README.md" ]; then
    cp README.md README.md.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ README.md backed up"
fi

if [ -f "CHANGELOG.md" ]; then
    cp CHANGELOG.md CHANGELOG.md.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ CHANGELOG.md backed up"
fi

# Update README
echo ""
echo "📝 === Updating README.md ==="
if [ -f "README_UPDATED.md" ]; then
    cp README_UPDATED.md README.md
    echo "✅ README.md updated with production-ready content"
else
    echo "❌ README_UPDATED.md not found"
    exit 1
fi

# Update CHANGELOG
echo ""
echo "📝 === Updating CHANGELOG.md ==="
if [ -f "CHANGELOG_UPDATED.md" ]; then
    cp CHANGELOG_UPDATED.md CHANGELOG.md
    echo "✅ CHANGELOG.md updated with current status"
else
    echo "❌ CHANGELOG_UPDATED.md not found"
    exit 1
fi

# Add success documentation
echo ""
echo "📝 === Adding Success Documentation ==="
if [ -f "ARWPOST_INSTALLATION_SUCCESS.md" ]; then
    cp ARWPOST_INSTALLATION_SUCCESS.md docs/INSTALLATION_SUCCESS.md
    echo "✅ Success documentation added to docs/"
else
    echo "⚠ ARWPOST_INSTALLATION_SUCCESS.md not found"
fi

# Check git status
echo ""
echo "🔍 === Git Status ==="
git status

# Add files to git
echo ""
echo "📦 === Adding Files to Git ==="
git add README.md
git add CHANGELOG.md
if [ -f "docs/INSTALLATION_SUCCESS.md" ]; then
    git add docs/INSTALLATION_SUCCESS.md
fi
echo "✅ Files added to git"

# Commit changes
echo ""
echo "💾 === Committing Changes ==="
git commit -m "Update documentation to reflect production-ready status

- Update README with clean module system (chpc/earth/arwpost/3.1 only)
- Add production-ready status and success metrics
- Update CHANGELOG with current version 3.1
- Add installation success documentation
- Remove references to backup files and symlinks
- Update module loading instructions
- Add verification results and testing information

Status: Production Ready
Cluster: Lengau (CHPC)
Compiler: Intel Parallel Studio XE 16.0.1"

echo "✅ Changes committed"

# Show what will be pushed
echo ""
echo "📤 === Ready to Push ==="
echo "The following changes will be pushed to GitHub:"
echo ""
echo "Modified files:"
echo "- README.md (updated with production-ready status)"
echo "- CHANGELOG.md (updated with version 3.1)"
echo ""
echo "New files:"
if [ -f "docs/INSTALLATION_SUCCESS.md" ]; then
    echo "- docs/INSTALLATION_SUCCESS.md"
fi
echo ""
echo "To push to GitHub, run:"
echo "  git push origin main"
echo ""
echo "Repository update completed successfully! 🎉"
















