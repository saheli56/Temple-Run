"""
Test script to debug the background system
"""

import cv2
import numpy as np
import sys
import os

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.game_config import *
from modules.background import ParallaxBackground

def test_background():
    """Test the background system"""
    print("Testing background system...")
    
    try:
        # Create background instance
        background = ParallaxBackground()
        print("✓ Background created successfully")
        
        # Create test frame
        frame = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        print("✓ Test frame created")
        
        # Test drawing
        frame = background.draw(frame)
        print("✓ Background drawn successfully")
        
        print("Background test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Background test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_background()
