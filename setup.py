#!/usr/bin/env python3
"""
Setup script for Editorial Assistant
Quick environment setup and validation
"""

import os
import subprocess
import sys


def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False


def validate_data_files():
    """Check if data files exist"""
    files = ["mock_catalog.json", "mock_tickets.json"]
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            return False
    return True


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Editorial Assistant Environment\n")
            f.write("# Add your API keys here if needed\n")
            f.write("DEBUG=False\n")
        print("✅ .env file created")
    else:
        print("✅ .env file exists")


def main():
    """Run complete setup"""
    print("🚀 Editorial Assistant Setup")
    print("=" * 30)
    
    if not check_python_version():
        return False
    
    if not validate_data_files():
        print("\n⚠️  Some data files are missing")
        print("Please ensure mock_catalog.json and mock_tickets.json are present")
        return False
    
    create_env_file()
    
    if install_requirements():
        print("\n✅ Setup completed successfully!")
        print("\n📚 Try running: python examples/quick_start.py")
        return True
    else:
        print("\n❌ Setup failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
