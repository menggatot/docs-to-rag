#!/bin/bash

# Check for Python installation
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed"
    echo "Please install Python using your system's package manager"
    echo "For example:"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  Fedora: sudo dnf install python3"
    echo "  macOS: brew install python3"
    echo "After installation, run this script again"
    exit 1
fi

# Function to choose environment
choose_env() {
    echo "Choose your preferred environment:"
    echo "1. Python venv"
    echo "2. Conda"
    read -p "Enter your choice (1 or 2): " choice

    case $choice in
        1)
            echo "Setting up Python venv..."
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            ;;
        2)
            if ! command -v conda &> /dev/null; then
                echo "Conda is not installed"
                echo "Please install Conda from https://docs.conda.io/en/latest/miniconda.html"
                echo "After installation, run this script again"
                exit 1
            fi
            echo "Setting up Conda environment..."
            conda create -y -n docstorage python=3.9
            source "$(conda info --base)/etc/profile.d/conda.sh"
            conda activate docstorage
            pip install -r requirements.txt
            ;;
        *)
            echo "Invalid choice"
            choose_env
            ;;
    esac
}

# Run the environment selection
choose_env

echo "Setup complete! The environment has been created and dependencies installed."
echo "To activate the environment:"
if [ "$choice" = "1" ]; then
    echo "Run: source venv/bin/activate"
else
    echo "Run: conda activate docstorage"
fi