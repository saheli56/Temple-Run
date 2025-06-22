#!/usr/bin/env python3
"""
Test connection to phone camera via IP Webcam
"""

import requests
import sys

def test_connection():
    ip_webcam_url = "http://100.102.121.116:8080"
    video_url = ip_webcam_url + "/video"
    
    print(f"🔄 Testing connection to: {video_url}")
    
    try:
        response = requests.get(video_url, timeout=10, stream=True)
        if response.status_code == 200:
            print("✅ SUCCESS: Phone camera connection working!")
            print(f"📱 Status: {response.status_code}")
            print(f"📊 Content Type: {response.headers.get('content-type', 'Unknown')}")
            return True
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Could not connect within 10 seconds")
        print("💡 Make sure your phone's IP Webcam app is running")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Could not reach the phone")
        print("💡 Check if phone and computer are on same WiFi network")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("📱 Phone Camera Connection Test")
    print("=" * 40)
    success = test_connection()
    
    if success:
        print("\n🎉 Ready to use phone camera with Temple Run!")
        print("💡 Run 'python main_enhanced.py' to start the game")
    else:
        print("\n📋 Troubleshooting steps:")
        print("1. Make sure IP Webcam app is running on your phone")
        print("2. Verify phone and computer are on same WiFi network")
        print("3. Check the IP address is correct: http://100.102.121.116:8080")
        print("4. Try opening the URL in a web browser first")
