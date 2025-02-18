@echo off
setlocal enabledelayedexpansion

REM Check for Python installation
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo After installation, run this script again
    pause
    exit /b 1
)

:choose_env
echo Choose your preferred environment:
echo 1. Python venv
echo 2. Conda
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo Setting up Python venv...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else if "%choice%"=="2" (
    conda --version > nul 2>&1
    if errorlevel 1 (
        echo Conda is not installed
        echo Please install Conda from https://docs.conda.io/en/latest/miniconda.html
        echo After installation, run this script again
        pause
        exit /b 1
    )
    echo Setting up Conda environment...
    conda create -y -n docstorage python=3.9
    call conda activate docstorage
    pip install -r requirements.txt
) else (
    echo Invalid choice
    goto choose_env
)

echo Setup complete! The environment has been created and dependencies installed.
echo To activate the environment:
if "%choice%"=="1" (
    echo Run: venv\Scripts\activate
) else (
    echo Run: conda activate docstorage
)
pause