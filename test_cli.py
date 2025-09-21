#!/usr/bin/env python3
"""
Simple test script to verify CLI functionality.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.cli.main import main
    print("✅ CLI imports successful!")
    
    # Test basic CLI functionality
    print("Testing CLI help...")
    main(["--help"])
    
except Exception as e:
    print(f"❌ CLI test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
