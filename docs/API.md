# API Documentation

## Core Components

### Main Class Methods

```python
class DocProcessor:
    def process_directory(self, docs_dir: str, media_dir: str) -> None:
        """
        Process all MD/MDX files in a directory.
        
        Args:
            docs_dir (str): Path to documentation directory
            media_dir (str): Path to media storage directory
        """

    def optimize_image(self, image_path: str) -> str:
        """
        Optimize image for OpenAI Vision API compatibility.
        
        Args:
            image_path (str): Path to source image
            
        Returns:
            str: Path to optimized image
        """

    def process_mdx(self, file_path: str) -> Dict:
        """
        Process single MDX file.
        
        Args:
            file_path (str): Path to MDX file
            
        Returns:
            Dict: Processed content with metadata
        """
```

## Configuration Parameters

### Command Line Arguments
| Parameter     | Type   | Required | Default        | Description                    |
|--------------|--------|----------|----------------|--------------------------------|
| --api-key    | string | Yes      | None           | OpenAI API key                 |
| --docs-dir   | string | Yes      | None           | Source documentation directory |
| --media-dir  | string | No       | media_storage  | Media storage directory        |
| --vision-model| string | No      | gpt-4o-mini    | OpenAI vision model           |
| --max-workers| int    | No       | 4              | Number of parallel workers     |
| --output     | string | No       | processed_content.md | Output file path         |

### Environment Variables
| Variable         | Required | Description              |
|-----------------|----------|--------------------------|
| OPENAI_API_KEY  | Yes*     | OpenAI API key           |

*Not required if provided via command line

## Rate Limiting Configuration

```python
class RateLimiter:
    def __init__(self, rate_limit: float = 200.0, burst_limit: float = 600.0):
        """
        Initialize rate limiter.
        
        Args:
            rate_limit (float): Requests per second
            burst_limit (float): Maximum burst size
        """
```

## Image Processing Parameters

### Size Limits
- Maximum file size: 20MB
- Format support: JPEG, PNG (input), JPEG (output)

### Optimization Parameters
```python
class ImageOptimizer:
    def __init__(self, 
                 max_size: int = 20 * 1024 * 1024,  # 20MB
                 quality_steps: range = range(95, 15, -5)):
        """
        Initialize image optimizer.
        
        Args:
            max_size (int): Maximum file size in bytes
            quality_steps (range): JPEG quality reduction steps
        """
```

## Error Codes and Handling

### Error Types
```python
class ProcessingError(Exception):
    """Base class for processing errors"""
    pass

class ImageProcessingError(ProcessingError):
    """Image processing related errors"""
    pass

class APIError(ProcessingError):
    """OpenAI API related errors"""
    pass
```

### Error Codes
| Code | Description                    | Resolution                        |
|------|--------------------------------|----------------------------------|
| 1001 | File not found                 | Check file path                  |
| 1002 | Invalid API key               | Verify API key                   |
| 1003 | Image too large               | Check image size limits          |
| 1004 | Rate limit exceeded           | Adjust rate limiting parameters  |
| 1005 | Invalid model selection       | Check available vision models    |

## Logging Configuration

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log'),
        logging.StreamHandler()
    ]
)
```

## Return Types

### Process Directory Result
```python
ProcessResult = Dict[str, Any]
{
    'processed_files': List[str],
    'failed_files': List[str],
    'image_stats': {
        'processed': int,
        'optimized': int,
        'failed': int
    },
    'processing_time': float
}
```

### File Processing Result
```python
FileResult = Dict[str, Any]
{
    'content': str,
    'metadata': Dict[str, Any],
    'images': List[str],
    'success': bool,
    'error': Optional[str]
}
```

## Performance Considerations

### Threading Configuration
- Default workers: 4
- Recommended range: 2-8 workers
- Memory usage: ~200MB per worker

### API Rate Limits
- Default rate: 200 requests/second
- Burst limit: 600 requests
- Automatic backoff on rate limit