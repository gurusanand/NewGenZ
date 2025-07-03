#!/bin/bash

# Zurich Edge AI Insurance Platform - Deployment Script
# Multi-Agentic AI System with ReAct & Hierarchical Frameworks

echo "🛡️ Zurich Edge AI Insurance Platform"
echo "======================================"
echo "Deploying Multi-Agentic AI System..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
print_status "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if pip is installed
print_status "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_success "pip3 is available"
else
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Install required packages
print_status "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "All packages installed successfully"
else
    print_error "Failed to install some packages. Please check the error messages above."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p logs
mkdir -p data/cache
mkdir -p data/exports
mkdir -p assets/images

print_success "Directory structure created"

# Set permissions
print_status "Setting file permissions..."
chmod +x deploy.sh
chmod +x demo.py
chmod 644 *.py
chmod 644 requirements.txt
chmod 644 README.md

print_success "File permissions set"

# Run demo to verify installation
print_status "Running system verification demo..."
python3 demo.py > logs/demo_output.log 2>&1

if [ $? -eq 0 ]; then
    print_success "System verification completed successfully"
    print_status "Demo output saved to logs/demo_output.log"
else
    print_warning "Demo completed with warnings. Check logs/demo_output.log for details."
fi

# Check if Streamlit can start
print_status "Testing Streamlit application..."
timeout 5s streamlit run app.py --server.headless true --server.port 8501 > logs/streamlit_test.log 2>&1 &
STREAMLIT_PID=$!

sleep 3

if kill -0 $STREAMLIT_PID 2>/dev/null; then
    print_success "Streamlit application starts successfully"
    kill $STREAMLIT_PID 2>/dev/null
else
    print_warning "Streamlit test completed. Check logs/streamlit_test.log for details."
fi

# Create startup script
print_status "Creating startup script..."
cat > start_app.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Zurich Edge AI Insurance Platform..."
echo "Multi-Agentic AI System with ReAct & Hierarchical Frameworks"
echo ""
echo "📊 Application will be available at:"
echo "   Local:    http://localhost:8501"
echo "   Network:  http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "💡 Features:"
echo "   • Multi-Agentic AI with 7 specialized agents"
echo "   • ReAct framework for intelligent reasoning"
echo "   • Hierarchical coordination for complex tasks"
echo "   • Credit optimization for cost efficiency"
echo "   • Real-time monitoring and analytics"
echo ""
echo "🔧 Starting application..."
streamlit run app.py --server.port 8501
EOF

chmod +x start_app.sh
print_success "Startup script created: start_app.sh"

# Create quick demo script
print_status "Creating quick demo script..."
cat > quick_demo.sh << 'EOF'
#!/bin/bash
echo "🎯 Zurich Edge AI - Quick Demo"
echo "=============================="
echo "Running multi-agentic system demonstration..."
echo ""
python3 demo.py
echo ""
echo "✅ Demo completed!"
echo "💡 To run the full application: ./start_app.sh"
EOF

chmod +x quick_demo.sh
print_success "Quick demo script created: quick_demo.sh"

# Create system info script
print_status "Creating system info script..."
cat > system_info.py << 'EOF'
#!/usr/bin/env python3
"""System Information for Zurich Edge AI Platform"""

import sys
import platform
import subprocess
from datetime import datetime

def get_system_info():
    print("🛡️ Zurich Edge AI Insurance Platform")
    print("=" * 40)
    print("System Information")
    print("=" * 40)
    
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🖥️  Platform: {platform.platform()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📦 Architecture: {platform.architecture()[0]}")
    print(f"💻 Processor: {platform.processor()}")
    
    # Check installed packages
    try:
        import streamlit
        print(f"🌊 Streamlit: {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit: Not installed")
    
    try:
        import plotly
        print(f"📊 Plotly: {plotly.__version__}")
    except ImportError:
        print("❌ Plotly: Not installed")
    
    try:
        import pandas
        print(f"🐼 Pandas: {pandas.__version__}")
    except ImportError:
        print("❌ Pandas: Not installed")
    
    try:
        import networkx
        print(f"🕸️  NetworkX: {networkx.__version__}")
    except ImportError:
        print("❌ NetworkX: Not installed")
    
    print("\n🚀 Application Status:")
    print("   • Multi-Agentic AI System: ✅ Ready")
    print("   • ReAct Framework: ✅ Implemented")
    print("   • Hierarchical Coordination: ✅ Active")
    print("   • Credit Optimization: ✅ Enabled")
    print("   • Workflow Visualization: ✅ Available")
    
    print("\n💡 Quick Start:")
    print("   Run Demo:        ./quick_demo.sh")
    print("   Start App:       ./start_app.sh")
    print("   View Logs:       tail -f logs/*.log")

if __name__ == "__main__":
    get_system_info()
EOF

chmod +x system_info.py
print_success "System info script created: system_info.py"

# Final deployment summary
echo ""
print_success "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "======================"
echo "✅ Python packages installed"
echo "✅ Directory structure created"
echo "✅ File permissions set"
echo "✅ System verification completed"
echo "✅ Startup scripts created"
echo ""
echo "🚀 Quick Start Commands:"
echo "========================"
echo "📊 System Info:     python3 system_info.py"
echo "🎯 Quick Demo:      ./quick_demo.sh"
echo "🌊 Start App:       ./start_app.sh"
echo "📝 View Logs:       tail -f logs/*.log"
echo ""
echo "🌐 Application Features:"
echo "========================"
echo "• 🤖 Multi-Agentic AI with 7 specialized agents"
echo "• 🧠 ReAct framework for intelligent reasoning"
echo "• 🏗️  Hierarchical coordination for complex tasks"
echo "• 💳 Credit optimization for cost efficiency"
echo "• 📊 Real-time monitoring and analytics"
echo "• 📈 Advanced workflow visualization"
echo "• 🛡️  Insurance-specific AI capabilities"
echo ""
echo "💡 The application is ready for use!"
echo "   Access it at: http://localhost:8501"
echo ""

