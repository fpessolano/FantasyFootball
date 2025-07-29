#!/usr/bin/env python3
"""
Phase 1 Test: Setup and Dependencies
Tests that faker integration is ready for Fantasy Football Manager.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_file_structure():
    """Test that required files are in place."""
    print("🗂️  Testing file structure...")
    
    required_files = [
        'name_generator.py',
        'requirements.txt', 
        'dependency_checker.py'
    ]
    
    missing_files = []
    for filename in required_files:
        file_path = os.path.join('..', filename) if os.getcwd().endswith('tests') else filename
        if not os.path.exists(file_path):
            missing_files.append(filename)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_faker_dependency():
    """Test faker dependency."""
    print("\n🔧 Testing faker dependency...")
    
    try:
        from name_generator import InternationalNameGenerator
        print("✅ name_generator.py imported successfully")
        
        generator = InternationalNameGenerator(seed=123)
        print("✅ InternationalNameGenerator initialized")
        
        # Test basic name generation
        name_data = generator.generate_name('en_US')
        required_keys = ['full_name', 'first_name', 'last_name', 'locale', 'nationality']
        
        for key in required_keys:
            if key not in name_data:
                print(f"❌ Missing key in name data: {key}")
                return False
        
        print(f"✅ Name generation working: {name_data['full_name']} ({name_data['nationality']})")
        
        # Test random name generation
        random_name = generator.generate_random_name()
        print(f"✅ Random name generation: {random_name['full_name']} ({random_name['nationality']})")
        
        # Test multiple locales
        test_locales = ['fr_FR', 'de_DE', 'es_ES', 'it_IT', 'pt_BR']
        print("✅ Testing multiple nationalities:")
        for locale in test_locales:
            try:
                name = generator.generate_name(locale)
                print(f"   {locale}: {name['full_name']} ({name['nationality']})")
            except Exception as e:
                print(f"❌ Error with locale {locale}: {e}")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Run: python dependency_checker.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_dependency_checker():
    """Test the dependency checker utility."""
    print("\n🔍 Testing dependency checker...")
    
    try:
        from dependency_checker import check_faker_dependency
        result = check_faker_dependency()
        if result:
            print("✅ Dependency checker working correctly")
            return True
        else:
            print("❌ Dependency checker reports problems")
            return False
    except Exception as e:
        print(f"❌ Error testing dependency checker: {e}")
        return False

def test_integration_readiness():
    """Test that everything is ready for integration."""
    print("\n🎯 Testing integration readiness...")
    
    try:
        from name_generator import InternationalNameGenerator
        
        generator = InternationalNameGenerator(seed=456)
        
        # Test batch generation (simulating player pool creation)
        batch_names = generator.generate_multiple_names(5)
        print("✅ Batch name generation working:")
        for i, name_data in enumerate(batch_names, 1):
            print(f"   {i}. {name_data['full_name']} ({name_data['nationality']})")
        
        # Test gender-specific generation (for future use)
        try:
            male_name = generator.generate_male_name('en_GB')
            female_name = generator.generate_female_name('fr_FR')
            print(f"✅ Gender-specific generation: {male_name.get('full_name', 'N/A')}, {female_name.get('full_name', 'N/A')}")
        except:
            print("⚠️  Gender-specific generation may have limited locale support (acceptable)")
        
        # Test locale search
        search_results = generator.search_locales('german')
        print(f"✅ Locale search working: Found {len(search_results)} matches for 'german'")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration readiness test failed: {e}")
        return False

def main():
    """Run all Phase 1 tests."""
    print("🧪 Phase 1: Setup and Dependencies Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Faker Dependency", test_faker_dependency), 
        ("Dependency Checker", test_dependency_checker),
        ("Integration Readiness", test_integration_readiness)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔬 Running: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PHASE 1 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 Phase 1 Complete! Ready to proceed to Phase 2.")
        return True
    else:
        print("\n⚠️  Phase 1 has issues. Please fix before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)