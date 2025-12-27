#!/bin/bash
# Setup script for Twitch Sound Alert (macOS/Linux)

echo "=========================================="
echo "  Twitch Sound Alert Setup"
echo "=========================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

# Virtual environment (optional)
if [ "${SKIP_VENV:-0}" = "1" ]; then
    echo "Skipping virtual environment (SKIP_VENV=1). Using system Python."
    PIP_CMD="python3 -m pip"
else
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv

    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source venv/bin/activate
    PIP_CMD="pip"
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
$PIP_CMD install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Check if config exists
if [ ! -f "config.json" ]; then
    echo ""
    echo "Creating default config.json from template..."
    cp config.example.json config.json
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
if [ "${SKIP_VENV:-0}" != "1" ]; then
    echo "1. Activate the virtual environment:"
    echo "   source venv/bin/activate"
else
    echo "1. (Optional) Activate venv later if you create one"
fi
echo ""
echo "2. Get your OAuth token from:"
echo "   https://twitchtokengenerator.com/"
echo ""
echo "3. Set the token as environment variable:"
echo "   export TWITCH_OAUTH_TOKEN=\"oauth:YOUR_TOKEN\""
echo ""
echo "4. Edit config.json with your settings (or use GUI)"
echo ""
echo "5. Run the application:"
echo "   python twitch-alert-gui.py    (GUI version)"
echo "   python twitch-sound-alert.py  (CLI version)"
echo ""
echo "For more information, see README.md"
echo ""
