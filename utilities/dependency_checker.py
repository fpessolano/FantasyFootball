#!/usr/bin/env python3
"""
Dependency Checker for Fantasy Football Manager
Checks if required dependencies are installed and provides installation guidance.
"""

import sys
import subprocess

def check_faker_dependency():
    """Check if faker library is installed and working."""
    try:
        import faker
        from faker import Faker
        
        # Test basic functionality
        fake = Faker()
        test_name = fake.name()
        
        # Try to get version, fallback if not available
        try:
            version = faker.__version__
        except AttributeError:
            try:
                version = faker.VERSION
            except AttributeError:
                version = "unknown"
        
        print("✅ Faker library is installed and working!")
        print(f"   Version: {version}")
        print(f"   Test name generated: {test_name}")
        return True
        
    except ImportError:
        print("❌ Faker library not found!")
        print("\n📦 Installation Instructions:")
        print("   Run: pip install faker")
        print("   Or: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error with Faker library: {e}")
        return False

def install_dependencies():
    """Attempt to install required dependencies."""
    print("🔧 Attempting to install dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
        print("✅ Faker installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies automatically.")
        print("   Please install manually: pip install faker")
        return False

def main():
    """Main dependency check function."""
    print("🔍 Checking Fantasy Football Manager dependencies...")
    print("=" * 50)
    
    if check_faker_dependency():
        print("\n🎉 All dependencies are ready!")
        print("   You can now use the enhanced name generation features.")
        return True
    else:
        print("\n⚠️  Dependencies missing!")
        
        choice = input("\nWould you like to install them automatically? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            if install_dependencies():
                print("\n🎉 Installation complete! Please restart the application.")
                return True
        
        print("\n📖 Manual Installation:")
        print("   1. pip install faker")
        print("   2. Restart Fantasy Football Manager")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)