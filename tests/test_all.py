#!/usr/bin/env python3
"""
Test All - Comprehensive Test Suite
Runs all phase tests for the Fantasy Football Manager faker integration.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_all_tests():
    """Run all phase tests in sequence."""
    print("🚀 Fantasy Football Manager - Comprehensive Test Suite")
    print("=" * 60)
    
    test_results = {}
    
    # Phase 1 Tests
    print("\n" + "=" * 20 + " PHASE 1: SETUP " + "=" * 20)
    try:
        from test_phase1_setup import main as phase1_main
        result = phase1_main()
        test_results['Phase 1'] = result
        print(f"📊 Phase 1 Result: {'✅ PASS' if result else '❌ FAIL'}")
    except Exception as e:
        print(f"❌ Phase 1 crashed: {e}")
        test_results['Phase 1'] = False
    
    # Phase 2 Tests
    print("\n" + "=" * 18 + " PHASE 2: MODELS " + "=" * 18)
    try:
        from test_phase2_models import main as phase2_main
        result = phase2_main()
        test_results['Phase 2'] = result
        print(f"📊 Phase 2 Result: {'✅ PASS' if result else '❌ FAIL'}")
    except Exception as e:
        print(f"❌ Phase 2 crashed: {e}")
        test_results['Phase 2'] = False
    
    # Phase 3 Tests
    print("\n" + "=" * 16 + " PHASE 3: INTEGRATION " + "=" * 16)
    try:
        from test_phase3_integration import main as phase3_main
        result = phase3_main()
        test_results['Phase 3'] = result
        print(f"📊 Phase 3 Result: {'✅ PASS' if result else '❌ FAIL'}")
    except Exception as e:
        print(f"❌ Phase 3 crashed: {e}")
        test_results['Phase 3'] = False
    
    # Final Results
    print("\n" + "=" * 22 + " SUMMARY " + "=" * 22)
    all_passed = True
    for phase, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{phase}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 52)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Fantasy Football faker integration ready!")
        print("✅ Setup complete")
        print("✅ Models enhanced")
        print("✅ Integration working")
        print("🚀 Ready for data migration!")
    else:
        print("❌ Some tests failed. Check output above for details.")
        print("🔧 Fix issues before proceeding.")
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)