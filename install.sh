#!/bin/bash

# chatMOSP Skills Installation Script
# Version: 2.0.0 (Document-driven architecture)

echo "========================================"
echo "chatMOSP Skills Installer"
echo "========================================"

# Check OpenClaw workspace
WORKSPACE_DIR="$HOME/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE_DIR/skills"

if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "❌ Error: OpenClaw workspace not found at $WORKSPACE_DIR"
    echo "Please install OpenClaw first."
    exit 1
fi

# Create skills directory if needed
mkdir -p "$SKILLS_DIR"

# Copy skill documents
echo "📁 Copying skill documents..."
cp -r skills/chatmosp-* "$SKILLS_DIR/"

# Verify installation
COUNT=$(find "$SKILLS_DIR" -maxdepth 1 -name "chatmosp-*" -type d | wc -l)

if [ "$COUNT" -ge 6 ]; then
    echo "✅ Installation successful! $COUNT chatMOSP skills installed."
    echo ""
    echo "Installed skills:"
    echo "  1. chatmosp-input-coordinator   - Task recognition and routing"
    echo "  2. chatmosp-parameter-builder    - Parameter construction with auto-calculation"
    echo "  3. chatmosp-msr-generator        - Nanoparticle structure generation (MSR)"
    echo "  4. chatmosp-kmc-simulator        - Kinetic Monte Carlo simulation (KMC)"
    echo "  5. chatmosp-literature-search     - Literature parameter extraction"
    echo "  6. chatmosp-file-organizer        - File management and visualization"
    echo ""
    echo "Next steps:"
    echo "  1. Make sure MOSP for chatMOSP is installed:"
    echo "     https://github.com/mosp-catalysis/mosp-for-chatMOSP"
    echo "  2. Restart OpenClaw or wait for skills to auto-load"
else
    echo "⚠️  Warning: Only $COUNT skills found. Expected 6."
    echo "Please check $SKILLS_DIR"
fi

echo "========================================"
