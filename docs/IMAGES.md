# Image Processing Guide

## Overview

The MDX to RAG Processor includes sophisticated image handling capabilities designed to optimize images for use with OpenAI's Vision API while maintaining quality and reducing file size.

## Technical Specifications

### Size Limits
- Maximum file size: 20MB (OpenAI API requirement)
- Recommended size: < 10MB for optimal processing
- Automatic optimization for oversized images

### Supported Formats

#### Input Formats
- JPEG/JPG
- PNG
- GIF (first frame only)
- BMP
- WEBP

#### Output Format
- JPEG (optimized for Vision API)

## Optimization Strategy

### Quality Reduction Pipeline
1. Initial quality check (95% quality)
2. Stepwise reduction:
   - Decrements of 5% per step
   - Range: 95% → 20%
   - Stops when size requirement met

```python
quality_steps = range(95, 15, -5)  # [95, 90, 85, ..., 20]
```

### Smart Resizing Algorithm
If quality reduction alone doesn't achieve target size:

1. Calculate aspect ratio
2. Maintain aspect ratio during resize
3. Iterative dimension reduction
4. Quality optimization post-resize

## Storage Strategy

### File Organization
```
media_storage/
├── original/           # Original images backup
├── optimized/         # Processed images
└── metadata/          # Image metadata JSON files
```

### Filename Generation
- Based on content hash (SHA-256)
- Ensures uniqueness
- Prevents duplicates
- Format: `{hash}.jpg`

Example:
```python
image_hash = hashlib.sha256(image_data).hexdigest()
filename = f"{image_hash}.jpg"
```

## Best Practices

### Pre-processing Recommendations

1. **Image Preparation**
   - Start with high-quality source images
   - Remove unnecessary metadata
   - Use appropriate image dimensions

2. **Format Selection**
   - Use JPEG for photographs
   - Use PNG for screenshots/diagrams
   - Avoid animated GIFs (only first frame used)

3. **Size Optimization**
   - Pre-optimize large images
   - Consider image dimensions
   - Remove unnecessary metadata

### Implementation Tips

1. **Error Prevention**
   ```python
   try:
       with Image.open(image_path) as img:
           # Process image
   except OSError:
       # Handle corrupt images
   ```

2. **Memory Management**
   - Process one image at a time
   - Close file handles properly
   - Use context managers

3. **Backup Strategy**
   - Keep original images
   - Store optimization metadata
   - Track image relationships

## Error Handling

### Common Issues

1. **Corrupt Images**
   - Validation before processing
   - Skip and log corrupted files
   - Maintain processing pipeline

2. **Memory Issues**
   - Implement streaming for large files
   - Monitor memory usage
   - Clean up temporary files

3. **Format Incompatibility**
   - Verify format support
   - Convert unsupported formats
   - Log conversion errors

### Error Logging
```python
{
    "image_path": str,
    "error_type": str,
    "error_message": str,
    "optimization_attempts": int,
    "final_size": int
}
```

## Performance Optimization

### Parallel Processing
- Configure worker count
- Balance CPU/memory usage
- Monitor system resources

### Caching Strategy
1. Cache optimized images
2. Store optimization metadata
3. Skip previously processed images

### Memory Management
- Stream large files
- Clean up temporary files
- Monitor memory usage

## Metadata Handling

### Stored Information
```json
{
    "original": {
        "filename": "original_image.png",
        "size": 25000000,
        "dimensions": [1920, 1080],
        "format": "PNG",
        "hash": "abc123..."
    },
    "optimized": {
        "filename": "abc123.jpg",
        "size": 15000000,
        "dimensions": [1920, 1080],
        "quality": 85,
        "format": "JPEG",
        "optimization_steps": [
            {"quality": 95, "size": 23000000},
            {"quality": 90, "size": 19000000},
            {"quality": 85, "size": 15000000}
        ]
    },
    "processing": {
        "timestamp": "2025-02-18T15:30:00Z",
        "duration": 1.5,
        "success": true
    }
}
```

### Metadata Usage
- Track optimization history
- Support image deduplication
- Enable optimization auditing
- Facilitate processing resumption

## Vision API Integration

### Image Preparation
1. Optimize image
2. Convert to Base64
3. Validate final size
4. Cache processed result

### API Request Format
```python
{
    "image": {
        "data": base64_image,
        "format": "jpeg",
        "size": image_size
    }
}
```

### Best Practices
1. Validate images before API submission
2. Implement retry logic
3. Monitor API usage
4. Cache API responses