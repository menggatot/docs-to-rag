# Installation Guide

## Prerequisites
- Python 3.x installed
- OpenAI API key
- Git (optional, for cloning the repository)

## Installation Steps

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd docs-to-rag
   ```

2. Run the appropriate setup script:
   ```bash
   # Windows
   setup.bat

   # Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

   The setup script will:
   - Check your Python installation
   - Let you choose between venv or Conda environment
   - Create an isolated environment
   - Install all required dependencies
   - Provide activation instructions

   This is the **recommended** way to install as it ensures proper environment isolation.

3. Configure API Key:
   - Provide your OpenAI API key using the `--api-key` argument when running the tool (see Usage Guide)
   - This is the recommended and secure way to provide your API key

## Alternative Installation (Not Recommended)

While you can install directly using pip:
```bash
pip install -r requirements.txt
```
This is **not recommended** because:
- No environment isolation
- Potential conflicts with other Python projects
- System-wide Python environment pollution
- Harder to manage dependencies

## Verification

Verify your installation by running:
```bash
python docstorag.py --help
```

This should display the help message with available command-line options.

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Permission Issues**
   - Ensure you have write permissions in the media storage directory
   - Run with appropriate permissions for file operations

3. **OpenAI API Key Issues**
   - Verify your API key is valid
   - Check environment variable is properly set
   - Ensure no whitespace in API key string

### System-Specific Notes

#### Windows
- Ensure Python is added to PATH
- Use Windows Terminal or PowerShell for better compatibility
- Run setup.bat as normal user (not administrator)

#### Linux/Mac
- Ensure proper execute permissions on scripts
- Check system Python version matches requirements
- Use setup.sh for automated environment setup