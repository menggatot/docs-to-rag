# Active Context: Docs to RAG Processor

## Current Status
Project is in initial development with core functionality implemented:
- Basic MD/MDX processing
- Image optimization and compression
- Parallel processing
- Progress tracking
- Error handling
- Vision model integration

## Recent Changes
1. Renamed project to docs-to-rag
2. Implemented vision model integration with gpt-4o-mini
3. Enhanced image optimization with smart compression
4. Updated image size limit to 20MB
5. Added configurable vision model support
6. Implemented base64 image encoding for API
7. Added command-line vision model selection

## Active Decisions
1. Image Processing
   - Using PIL for smart image compression
   - Size limit set to 20MB (API limit)
   - JPEG format with quality-based compression
   - Progressive compression strategy (quality reduction before resizing)

2. API Integration
    - Vision model integration using gpt-4o-mini
    - Support for base64 image encoding
    - Token bucket rate limiting with configurable parameters
    - Thread-safe concurrent API request handling
    - Default to low-detail image processing

3. Performance
   - Default to 4 parallel workers
   - Memory-efficient file handling
   - Progress tracking with tqdm
   - Progressive image compression

## Next Steps
1. Testing and Validation
   - Test vision model integration
   - Verify image compression quality
   - Performance testing with large images
   - Error handling verification

2. Feature Enhancement
   - Support for additional vision models
   - Fine-tune compression parameters
   - Enhanced error reporting for API calls

3. Documentation
   - API documentation
   - Vision model configuration
   - Image optimization guidelines