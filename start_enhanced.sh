#!/bin/bash

echo "🚀 Starting Enhanced Zurich Edge AI Insurance Platform..."
echo "Real OpenAPI Integration Version"
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Start enhanced application
echo "Starting enhanced application on port ${STREAMLIT_PORT:-8502}..."
streamlit run app_enhanced.py --server.port ${STREAMLIT_PORT:-8502}
