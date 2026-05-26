#!/bin/bash
# chatMOSP — Installation Script
# License: GNU GPL v3

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
SKILLS_DIR="${WORKSPACE}/skills"

echo "========================================"
echo "chatMOSP — Skill Installation"
echo "========================================"

# Create skills directory
mkdir -p "$SKILLS_DIR"

# Copy skill documents
echo "Copying skill documents..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

for skill_dir in "$SCRIPT_DIR"/skills/chatmosp-*/; do
    skill_name=$(basename "$skill_dir")
    echo "  $skill_name"
    cp -r "$skill_dir" "$SKILLS_DIR/"
done

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "Installed skills:"
ls "$SKILLS_DIR"/chatmosp-*/SKILL.md 2>/dev/null | while read f; do
    echo "  ✅ $(dirname "$f" | xargs basename)"
done
echo ""
echo "Next steps:"
echo "  1. Install MOSP engine: https://github.com/mosp-catalysis/mosp-for-chatMOSP"
echo "  2. Restart OpenClaw"
echo "  3. Try: 'Generate a Pt nanoparticle under CO oxidation'"
echo ""
echo "License: GNU GPL v3"
echo "Citation: Ying L, Zhu B,* Gao Y,* J. Chem. Phys. 2024, 161, 114702"
echo ""

exit 0
