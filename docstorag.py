#!/usr/bin/env python3
import base64
import os
import re
import yaml
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from openai import OpenAI
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import mimetypes
from PIL import Image
import io
import time
from dataclasses import dataclass
from datetime import datetime
from threading import Lock

@dataclass
class RateLimiter:
    """Token bucket rate limiter for API calls."""
    rate: float  # tokens per second
    capacity: float  # bucket size
    _tokens: float = 0.0
    _last_update: float = 0.0
    _lock: Lock = None

    def __post_init__(self):
        self._tokens = self.capacity
        self._last_update = time.monotonic()
        self._lock = Lock()

    def _update_tokens(self):
        """Update token count based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
        self._last_update = now

    def acquire(self, tokens: float = 1.0) -> float:
        """
        Acquire tokens. Returns the time to wait (in seconds).
        """
        with self._lock:
            self._update_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return 0.0
            wait_time = (tokens - self._tokens) / self.rate
            self._tokens = 0.0
            return wait_time

@dataclass
class ProcessingStats:
    total_files: int = 0
    processed_files: int = 0
    total_images: int = 0
    processed_images: int = 0
    errors: List[str] = None
    start_time: datetime = None
    
    def __post_init__(self):
        self.errors = []
        self.start_time = datetime.now()
    
    def get_summary(self) -> str:
        duration = datetime.now() - self.start_time
        return f"""
Processing Summary:
-----------------
Files Processed: {self.processed_files}/{self.total_files}
Images Processed: {self.processed_images}/{self.total_images}
Duration: {duration}
Errors: {len(self.errors)}
"""

class MarkdownProcessor:
    def __init__(
        self,
        openai_api_key: str,
        media_dir: str = "media_storage",
        max_workers: int = 4,
        image_size_limit: int = 20 * 1024 * 1024,  # 20MB
        docs_dir: str = None,
        rate_limit: float = 10.0,  # requests per second
        burst_limit: float = 30.0,  # max burst size
        vision_model: str = "gpt-4o-mini"  # Vision model to use
    ):
        """
        Initialize the Markdown/MDX processor with OpenAI integration
        
        Args:
            openai_api_key: Your OpenAI API key
            media_dir: Directory to store media files
            max_workers: Maximum number of parallel workers
            image_size_limit: Maximum image size in bytes
            docs_dir: Root directory containing documentation files
            rate_limit: Number of API requests allowed per second
            burst_limit: Maximum number of requests allowed in a burst
            vision_model: Vision model to use for image analysis (defaults to gpt-4o-mini)
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.media_dir = media_dir
        self.max_workers = max_workers
        self.image_size_limit = image_size_limit
        self.docs_dir = Path(docs_dir) if docs_dir else None
        self.stats = ProcessingStats()
        self.rate_limiter = RateLimiter(rate=rate_limit, capacity=burst_limit)
        self.vision_model = vision_model
        
        # Setup logging
        self.setup_logging()
        
        # Create media directory
        os.makedirs(self.media_dir, exist_ok=True)
        
        # Initialize processed files set
        self.processed_files: Set[str] = set()
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S',
            handlers=[
                logging.FileHandler(f'docs_processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def process_files(self, directory: str) -> str:
        """Process all Markdown and MDX files in a directory and combine them into a single document."""
        try:
            # Get all Markdown and MDX files
            mdx_files = list(Path(directory).rglob("*.mdx")) + list(Path(directory).rglob("*.md"))
            self.stats.total_files = len(mdx_files)
            
            if not mdx_files:
                raise ValueError(f"No Markdown (.md) or MDX (.mdx) files found in {directory}")
            
            self.logger.info(f"Found {len(mdx_files)} files to process")
            combined_content = []
            # Process files in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {
                    executor.submit(self._process_file_safe, file_path): file_path
                    for file_path in mdx_files
                }
                
                # Show progress bar
                with tqdm(total=len(mdx_files), desc="Processing files") as pbar:
                    for future in as_completed(future_to_file):
                        file_path = future_to_file[future]
                        try:
                            content = future.result()
                            if content:
                                combined_content.append(content)
                            self.stats.processed_files += 1
                        except Exception as e:
                            self.logger.error(f"Error processing {file_path}: {str(e)}")
                            self.stats.errors.append(f"Error processing {file_path}: {str(e)}")
                        pbar.update(1)
            
            # Sort content by file path to ensure consistent output
            combined_content.sort()
            
            # Add processing summary
            summary = self.stats.get_summary()
            combined_content.insert(0, f"<!-- {summary} -->")
            
            return "\n\n---\n\n".join(combined_content)
            
        except Exception as e:
            self.logger.error(f"Error in process_mdx_files: {str(e)}")
            raise
    
    def _process_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely process a single file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add file path as metadata
            metadata = {
                "source_file": str(file_path),
                "type": "documentation",
                "last_processed": datetime.now().isoformat()
            }
            
            return self._process_single_file(content, file_path, metadata)
            
        except Exception as e:
            self.logger.error(f"Error processing {file_path}: {str(e)}")
            self.stats.errors.append(f"Error processing {file_path}: {str(e)}")
            return None

    def _process_single_file(self, content: str, file_path: Path, metadata: Dict) -> Optional[str]:
        """Process a single MDX/MD file."""
        try:
            # Extract frontmatter if present
            frontmatter = {}
            content_without_frontmatter = content
            
            if content.startswith('---'):
                try:
                    # Find the second '---' that closes the frontmatter
                    end_idx = content.find('---', 3)
                    if end_idx != -1:
                        frontmatter_str = content[3:end_idx].strip()
                        frontmatter = yaml.safe_load(frontmatter_str.encode('utf-8').decode('utf-8')) or {}
                        content_without_frontmatter = content[end_idx + 3:].strip()
                except yaml.YAMLError as e:
                    self.logger.warning(f"Error parsing frontmatter in {file_path}: {str(e)}")

            # Process images in content
            def replace_image(match):
                alt_text = match.group(1) or ''
                image_path = match.group(2)
                
                # Handle only local images
                if not image_path.startswith(('http://', 'https://', 'data:')):
                    return self._process_local_image(alt_text, image_path, file_path)
                return match.group(0)  # Keep remote images as-is

            # Process both MDX/MD image formats
            img_pattern = r'!\[(.*?)\]\((.*?)\)'  # ![alt](src)
            processed_content = re.sub(img_pattern, replace_image, content_without_frontmatter)

            # Combine metadata
            combined_metadata = {
                **metadata,
                **frontmatter,
                "word_count": len(content_without_frontmatter.split()),
                "has_images": '![' in content_without_frontmatter
            }

            # Format the output with metadata as frontmatter
            return f"""---
{yaml.dump(combined_metadata, default_flow_style=False, allow_unicode=True)}---

{processed_content}"""

        except Exception as e:
            self.logger.error(f"Error in _process_single_file for {file_path}: {str(e)}")
            return None
    
    def _optimize_image(self, image_path: Path) -> Optional[Path]:
        """Optimize image if it's too large."""
        try:
            if image_path.stat().st_size > self.image_size_limit:
                output_path = image_path.with_suffix('.jpg')
                quality_step = 5
                min_quality = 20

                with Image.open(image_path) as img:
                    # Convert to RGB if needed
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')

                    quality = 95  # Start with high quality

                    # Iteratively reduce quality and resize image until it meets the size requirement
                    while True:
                        # Save the image with the current quality setting
                        img.save(output_path, format='JPEG', quality=quality, optimize=True)
                        current_size = output_path.stat().st_size

                        # Check if the current file size is within the desired limit
                        if current_size <= self.image_size_limit:
                            self.logger.info(f"Compressed image to {current_size / (1024 * 1024):.2f} MB")
                            return output_path

                        # If quality is above the minimum threshold, reduce it
                        if quality > min_quality:
                            quality -= quality_step
                        else:
                            # If quality is at or below the minimum, resize the image
                            reduction_factor = (self.image_size_limit / current_size) ** 0.5
                            width, height = img.size
                            new_dimensions = (int(width * reduction_factor), int(height * reduction_factor))
                            img = img.resize(new_dimensions, Image.Resampling.LANCZOS)
                            quality = 95  # Reset quality after resizing

            return image_path
        except Exception as e:
            self.logger.error(f"Error optimizing image {image_path}: {str(e)}")
            return None
    
    def _process_local_image(self, alt_text: str, image_path: str, file_path: Path) -> str:
        """Process local images with optimization."""
        try:
            # Try multiple possible locations for the image
            possible_paths = []
            
            # First try the exact path as provided
            # Extract just the filename from the path
            image_filename = Path(image_path).name
            
            # Always try the markdown file's directory first:
            # 1. Direct filename in same directory
            # 2. As provided (relative to markdown file)
            possible_paths.append(file_path.parent / image_filename)
            possible_paths.append(file_path.parent / image_path.lstrip('/'))
            
            # For absolute paths, also try relative to docs directory
            if image_path.startswith('/') and self.docs_dir:
                possible_paths.append(self.docs_dir / image_path.lstrip('/'))
            
            # Try each possible path
            full_image_path = None
            for path in possible_paths:
                if path.exists():
                    full_image_path = path
                    break
            
            if not full_image_path:
                self.logger.warning(f"Image not found in any location: {image_path}")
                return f'[Missing Image: {alt_text}]'
            
            self.stats.total_images += 1
            
            # Optimize image
            optimized_path = self._optimize_image(full_image_path)
            if not optimized_path:
                return f'[Failed to process image: {alt_text}]'
            
            # Create a unique filename using hash
            image_hash = hashlib.md5(str(full_image_path).encode()).hexdigest()
            new_filename = f"{image_hash}{optimized_path.suffix}"
            new_path = Path(self.media_dir) / new_filename
            
            # Copy optimized image to media storage
            shutil.copy2(optimized_path, new_path)
            
            # Generate image description with rate limiting
            description = self._generate_image_description(alt_text, str(full_image_path))
            
            self.stats.processed_images += 1
            self.logger.info(f"Successfully processed image: {image_path} -> {new_filename}")
            
            return f'[Image: {description}](media://{new_filename})'
            
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            return f'[Image: {alt_text}]'
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _generate_image_description(self, alt_text: str, image_path: str) -> str:
        """Generate a detailed description of the image using OpenAI with rate limiting."""
        if len(alt_text) > 50:
            return alt_text
            
        try:
            # Log that we're starting to process this image
            self.logger.info(f"Processing image for description: {image_path}")
            
            # Apply rate limiting with token bucket algorithm
            wait_time = self.rate_limiter.acquire()
            if wait_time > 0:
                time.sleep(wait_time)

            # Encode image to base64
            base64_image = self._encode_image(image_path)
            
            # Create vision API request
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Please describe this image from documentation. Original description: {alt_text if alt_text else 'No description provided'}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content or alt_text or "Image"
            
        except Exception as e:
            self.logger.error(f"Error generating image description: {str(e)}")
            return alt_text or "Image"

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process Markdown and MDX files for RAG')
    parser.add_argument('--api-key', required=True, help='OpenAI API key')
    parser.add_argument('--docs-dir', required=True, help='Directory containing MDX files')
    parser.add_argument('--media-dir', default='media_storage', help='Directory for storing media files')
    parser.add_argument('--max-workers', type=int, default=4, help='Maximum number of parallel workers')
    parser.add_argument('--rate-limit', type=float, default=200.0, help='API requests per second')
    parser.add_argument('--burst-limit', type=float, default=600.0, help='Maximum burst size for API requests')
    parser.add_argument('--vision-model', default='gpt-4o-mini', help='Vision model to use for image analysis')
    parser.add_argument('--output', default='processed_content.md', help='Output file path')
    
    args = parser.parse_args()
    processor = None

    try:
        processor = MarkdownProcessor(
            openai_api_key=args.api_key,
            media_dir=args.media_dir,
            max_workers=args.max_workers,
            docs_dir=args.docs_dir,
            rate_limit=args.rate_limit,
            burst_limit=args.burst_limit,
            vision_model=args.vision_model
        )
        
        combined_content = processor.process_files(args.docs_dir)
        
        if combined_content:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(combined_content)
            print(processor.stats.get_summary())
    
    except Exception as e:
        print(f"Error: {str(e)}")
        if processor and processor.stats:
            print(processor.stats.get_summary())
        exit(1)