#!/usr/bin/env python3
"""
Run All Tests - Fantasy Football Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Batch test runner for all Fantasy Football Manager tests.
"""

import sys
import os
import importlib.util
from pathlib import Path

def load_and_run_test(test_file):
    """Load and run a test file."""
    test_path = Path(__file__).parent / test_file
    
    if not test_path.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    # Load the test module
    spec = importlib.util.spec_from_file_location("test_module", test_path)
    test_module = importlib.util.module_from_spec(spec)
    
    try:
        spec.loader.exec_module(test_module)
        
        # Run the test if it has a run_all_tests function
        if hasattr(test_module, 'run_all_tests'):
            print(f"\n🧪 Running {test_file}...")
            return test_module.run_all_tests()
        else:
            print(f"⚠️  {test_file} does not have a run_all_tests function")
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def main():
    """Run all tests in the tests directory."""
    print("🚀 FANTASY FOOTBALL MANAGER - ALL TESTS")
    print("=" * 60)
    
    # List of test files to run
    test_files = [
        "test_penalty_system.py",
        # Add more test files here as they are created
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if load_and_run_test(test_file):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print("🏁 ALL TESTS SUMMARY")
    print("=" * 60)
    print(f"✅ Test files passed: {passed}")
    print(f"❌ Test files failed: {failed}")
    print(f"📊 Success rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Fantasy Football Manager is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test file(s) failed. Please review the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)