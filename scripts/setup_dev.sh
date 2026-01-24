#!/bin/bash
set -e

# DataEngOS Development Setup Script
# Version: 1.0.0

echo "🚀 Starting DataEngOS Setup..."

# 1. System Dependency Check
echo "🔍 Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found."
    exit 1
fi

# Check for venv module (Common issue on Debian/Ubuntu)
if ! python3 -c "import venv" &> /dev/null; then
    echo "⚠️  Python venv module missing."
    if [ -f /etc/debian_version ]; then
        echo "💡 Detected Debian/Ubuntu. Trying to install..."
        echo "👉 sudo apt install python3-venv -y"
        sudo apt install python3-venv -y
    else
        echo "❌ Please install 'python3-venv' package manually."
        exit 1
    fi
fi

# 2. Virtual Environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment exists."
fi

# 3. Installation
echo "⬇️  Installing DataEngOS (Editable Mode)..."
source .venv/bin/activate

# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -e .

echo "--------------------------------------------------"
echo "✅ Setup Complete!"
echo "--------------------------------------------------"
echo "👉 To activate: source .venv/bin/activate"
echo "👉 To verify:   dataeng-os --help"
