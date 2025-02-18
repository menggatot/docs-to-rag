# Docs to RAG Processor

A Python utility designed to process Markdown (MD) and MDX files for use in Retrieval-Augmented Generation (RAG) systems. This tool streamlines the preparation of documentation for AI-powered knowledge bases by processing content, optimizing images, and maintaining metadata.

## Key Features

- Process MD/MDX files from specified directories
- Intelligent image handling and optimization
- Metadata preservation and structured processing
- Parallel processing for improved performance
- OpenAI Vision API integration
- Detailed logging and progress tracking

## Requirements

- Python 3.x
- OpenAI API Key
- Required Python packages (see requirements.txt)

## Quick Start

1. Clone the repository

2. Set up Python environment and install dependencies:
   ```bash
   # Windows
   setup.bat

   # Linux/macOS
   chmod +x setup.sh
   ./setup.sh
   ```
   The setup script will:
   - Create an isolated Python environment (venv or conda)
   - Install all required dependencies
   - Guide you through the setup process

3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

4. Run the processor:
   ```bash
   python docstorag.py \
       --docs-dir DOCS_DIRECTORY \
       --media-dir media_storage \
       --output processed_content.md
   ```

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use the processor
- [API Documentation](docs/API.md) - API reference and integration details
- [Image Processing Guide](docs/IMAGES.md) - Image handling and optimization

## Technical Specifications

- Image Processing:
  - Maximum size: 20MB (OpenAI API limit)
  - Smart compression strategy
  - Supported formats: JPEG, PNG (input), JPEG (output)
  - Hash-based storage system

- Vision Model:
  - Default model: gpt-4o-mini
  - Configurable model selection
  - Base64 image encoding
  - Rate limiting support

## Example Usage

Basic usage with default settings:
```bash
python docstorag.py --docs-dir ./my-docs --media-dir ./media --output processed.md
```

Advanced usage with all options:
```bash
python docstorag.py \
    --api-key OPENAI_API_KEY \
    --docs-dir DOCS_DIRECTORY \
    --media-dir media_storage \
    --vision-model gpt-4o-mini \
    --max-workers 4 \
    --output processed_content.md
```