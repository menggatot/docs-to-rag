# System Patterns: Docs to RAG Processor

## Architecture Overview
The system follows a modular architecture with clear separation of concerns:

### Core Components
1. MarkdownProcessor
   - Main class handling file processing
   - Manages worker threads
   - Coordinates image processing
   - Maintains processing statistics
   - Handles vision model integration

2. ProcessingStats
   - Tracks processing metrics
   - Maintains error lists
   - Provides progress summaries

### Key Patterns

1. Thread Pool Pattern
   ```python
   with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
       future_to_file = {executor.submit(self._process_file_safe, file_path): file_path}
   ```
   - Enables parallel processing
   - Manages resource utilization
   - Maintains processing order

2. Progress Tracking Pattern
   ```python
   with tqdm(total=len(mdx_files), desc="Processing files") as pbar:
       for future in as_completed(future_to_file):
           # Process and update progress
   ```
   - Real-time progress visualization
   - Clear completion tracking

3. Error Handling Pattern
   ```python
   try:
       # Processing logic
   except Exception as e:
       self.logger.error(f"Error in process_mdx_files: {str(e)}")
       raise
   ```
   - Comprehensive error catching
   - Detailed logging
   - Clean error propagation

4. Rate Limiting Pattern
    ```python
    @dataclass
    class RateLimiter:
        rate: float  # tokens per second
        capacity: float  # bucket size
        
        def acquire(self, tokens: float = 1.0) -> float:
            # Token bucket algorithm implementation
    ```
    - Thread-safe token bucket algorithm
    - Configurable rate and burst limits
    - Dynamic rate adjustment support
    - Concurrent request handling

5. Smart Image Compression Pattern
    ```python
    def _optimize_image(self, image_path: Path) -> Optional[Path]:
        # Progressive compression strategy
        while True:
            if quality > min_quality:
                quality -= quality_step  # Try reducing quality first
            else:
                # Resort to resizing if quality reduction isn't enough
                reduction_factor = (max_size_bytes / current_size) ** 0.5
                img = resize_with_aspect_ratio(img, reduction_factor)
    ```
    - Progressive quality reduction
    - Smart resize when needed
    - Format conversion to JPEG
    - Size limit enforcement (20MB)

6. Vision Model Integration Pattern
    ```python
    def _generate_image_description(self, alt_text: str, image_path: str) -> str:
        # Base64 encode image
        base64_image = self._encode_image(image_path)
        
        # Vision API request with configurable model
        response = self.client.chat.completions.create(
            model=self.vision_model,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }}
                ]
            }]
        )
    ```
    - Configurable vision model
    - Base64 image encoding
    - Structured API requests
    - Error handling and fallbacks

## Data Flow
1. Input
   - MD/MDX files
   - Images within documents
   - Configuration parameters
   - Vision model settings

2. Processing
   - File parsing
   - Smart image compression
   - Vision model analysis
   - Content combination

3. Output
   - Processed markdown content
   - Optimized images
   - Image descriptions
   - Processing statistics

## Integration Points
1. Vision API
   - Image description generation
   - Model configuration
   - Base64 image handling

2. Image Processing
   - Smart compression
   - Format conversion
   - Quality optimization

3. Filesystem
   - Input file reading
   - Media storage
   - Output file writing