# Technical Context: Docs to RAG Processor

## Technology Stack

### Core Technologies
- Python 3.x
- OpenAI Vision API
- PIL (Python Imaging Library)
- YAML processing

### Key Dependencies
```python
import os
import re
import yaml
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from openai import OpenAI
import shutil
import base64
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from PIL import Image
```

## Development Setup

### Required Environment Variables
- OPENAI_API_KEY: API key for OpenAI integration

### Command-Line Arguments
```bash
python docstorag.py \
    --api-key OPENAI_API_KEY \
    --docs-dir DOCS_DIRECTORY \
    --media-dir media_storage \
    --vision-model gpt-4o-mini \
    --max-workers 4 \
    --output processed_content.md
```

## Technical Constraints

### Image Processing
- Maximum image size: 20MB (OpenAI API limit)
- Compression strategy:
  1. Quality reduction (95% → 20% in 5% steps)
  2. Smart resizing if needed
- Supported formats:
  - Input: Common image formats (JPEG, PNG, etc.)
  - Output: JPEG for optimized images
- Storage: Unique hash-based filenames

### Vision Model Integration
- Default model: gpt-4o-mini
- Image format: Base64-encoded JPEG
- Size limit enforced: 20MB
- Configurable model selection

### Performance
- Parallel processing with configurable worker count
- Memory-efficient file handling
- Token bucket rate limiting for API calls
  ```python
  # Rate limiting configuration
  rate_limit: float = 200.0  # requests per second
  burst_limit: float = 600.0  # max burst size
  ```

### File Handling
- UTF-8 encoding for text files
- Support for MD and MDX formats
- Frontmatter parsing and preservation
- Base64 image encoding

## Logging and Monitoring
- Detailed logging with timestamps
- File-based and console output
- Progress tracking with tqdm
- Comprehensive error reporting

## Future Considerations
1. Vision Model Enhancements
   - Support for more vision models (o1, gpt-4o)
   - Model-specific optimizations
   - Cost optimization strategies

2. Image Processing
   - Enhanced compression algorithms
   - Additional format support
   - Metadata preservation

3. Additional Format Support
   - Support for other documentation formats
   - Enhanced metadata extraction