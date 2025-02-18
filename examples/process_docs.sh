#!/usr/bin/env bash

# Docs to RAG example usage script

# Configuration
DOCS_LOCATION="docs"           # The root directory containing your markdown files
PROJECT_NAME="my-project"      # Name of your project/documentation
WORKERS=4                      # Number of parallel workers

# Create output directories if they don't exist
mkdir -p "output/$PROJECT_NAME"

# Process documentation
# Note: Replace with your actual OpenAI API key
docstorag \
    --api-key=YOUR_OPENAI_API_KEY \
    --docs-dir=$(pwd)/$DOCS_LOCATION \
    --output=$(pwd)/output/$PROJECT_NAME/$PROJECT_NAME.md \
    --media-dir=$(pwd)/output/$PROJECT_NAME/media \
    --max-workers=$WORKERS \
    --vision-model=gpt-4o-mini