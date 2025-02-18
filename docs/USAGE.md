# Usage Guide

## Basic Usage

The basic command structure is:
```bash
python docstorag.py --api-key YOUR_API_KEY --docs-dir YOUR_DOCS_DIR
```

## Command Line Arguments

### Required Arguments
- `--api-key`: Your OpenAI API key
- `--docs-dir`: Directory containing MD/MDX files to process

### Optional Arguments
- `--media-dir`: Directory for storing optimized images (default: media_storage)
- `--vision-model`: OpenAI vision model to use (default: gpt-4o-mini)
- `--max-workers`: Number of parallel workers (default: 4)
- `--output`: Output file for processed content (default: processed_content.md)

## Examples

### Basic Processing
Process documents with default settings:
```bash
python docstorag.py \
    --api-key YOUR_API_KEY \
    --docs-dir ./documentation
```

### Advanced Processing
Process with custom settings:
```bash
python docstorag.py \
    --api-key YOUR_API_KEY \
    --docs-dir ./documentation \
    --media-dir ./optimized_media \
    --vision-model gpt-4o-mini \
    --max-workers 8 \
    --output ./processed/final.md
```

## Performance Optimization

### Parallel Processing
- Adjust `--max-workers` based on your system capabilities
- Default is 4 workers
- Example for high-performance systems:
  ```bash
  python docstorag.py \
      --api-key YOUR_API_KEY \
      --docs-dir ./docs \
      --max-workers 8
  ```

### Rate Limiting
The tool implements token bucket rate limiting:
- 200 requests per second default rate
- 600 requests burst limit
- Automatically manages API call pacing

## Image Processing

### Size Limits
- Maximum image size: 20MB (OpenAI API limit)
- Images exceeding limit are automatically optimized

### Optimization Strategy
1. Quality reduction (95% → 20% in 5% steps)
2. Smart resizing if needed
3. Format conversion to JPEG

### Example with Image Processing Focus
```bash
python docstorag.py \
    --api-key YOUR_API_KEY \
    --docs-dir ./image_heavy_docs \
    --media-dir ./optimized_images \
    --max-workers 4
```

## Progress Tracking

The tool provides progress information via:
- Console output with progress bars
- Detailed logging (see logs/ directory)
- Final processing summary

## Error Handling

### Common Error Messages
1. "File not found": Check path to docs directory
2. "API key invalid": Verify OpenAI API key
3. "Image too large": Image exceeding size limits

### Logging
- Check logs/ directory for detailed error information
- Console output shows real-time processing status

## Best Practices

1. **Directory Structure**
   - Keep source docs in separate directory
   - Use clean media directory for optimized images

2. **Performance**
   - Start with default worker count
   - Increase if system resources allow
   - Monitor system resource usage

3. **Image Handling**
   - Pre-optimize large images if possible
   - Use supported image formats
   - Monitor media directory size

4. **Error Recovery**
   - Tool can resume interrupted processing
   - Keep original files backed up
   - Monitor logs for issues