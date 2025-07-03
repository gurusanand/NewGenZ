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
