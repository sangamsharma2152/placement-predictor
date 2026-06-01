#!/usr/bin/env python3
"""
Test script to verify all imports and modules work correctly
"""

import sys
import traceback

def test_imports():
    """Test all critical imports"""
    
    print("=" * 60)
    print("Testing Python Module Imports")
    print("=" * 60)
    
    modules_to_test = [
        ('config', 'Configuration module'),
        ('database', 'Database module'),
        ('models', 'ML Models module'),
        ('utils', 'Utilities module'),
        ('notifications', 'Notifications module'),
        ('visualizations', 'Visualizations module'),
    ]
    
    all_passed = True
    
    for module_name, description in modules_to_test:
        try:
            print(f"\n✓ Testing {description} ({module_name})...", end=" ")
            __import__(module_name)
            print("✅ SUCCESS")
        except Exception as e:
            print(f"❌ FAILED")
            print(f"   Error: {str(e)}")
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 60)
    
    # Test specific classes
    print("\nTesting Specific Classes:")
    print("-" * 60)
    
    try:
        from config import APP_TITLE, DATABASE_PATH, SUPPORTED_LANGUAGES
        print(f"✅ config: APP_TITLE='{APP_TITLE}'")
        print(f"   DATABASE_PATH='{DATABASE_PATH}'")
        print(f"   SUPPORTED_LANGUAGES={list(SUPPORTED_LANGUAGES.keys())}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        all_passed = False
    
    try:
        from database import Database, db
        print(f"✅ database: Database class imported")
        print(f"   Global db instance created: {type(db).__name__}")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        all_passed = False
    
    try:
        from models import PlacementModel, placement_model
        print(f"✅ models: PlacementModel class imported")
        print(f"   Global placement_model instance created: {type(placement_model).__name__}")
        print(f"   Models trained: {list(placement_model.models.keys())}")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        traceback.print_exc()
        all_passed = False
    
    try:
        from utils import (SessionManager, CacheManager, Achievement, 
                          DataValidator, ReportGenerator)
        print(f"✅ utils: All utility classes imported")
        print(f"   - SessionManager")
        print(f"   - CacheManager")
        print(f"   - Achievement ({len(Achievement.ACHIEVEMENTS)} achievements)")
        print(f"   - DataValidator")
        print(f"   - ReportGenerator")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        traceback.print_exc()
        all_passed = False
    
    try:
        from notifications import EmailNotification, ALERT_TEMPLATES
        print(f"✅ notifications: EmailNotification class imported")
        print(f"   Alert templates: {list(ALERT_TEMPLATES.keys())}")
    except Exception as e:
        print(f"❌ Notifications import failed: {e}")
        all_passed = False
    
    try:
        import visualizations
        print(f"✅ visualizations: Module imported successfully")
    except Exception as e:
        print(f"❌ Visualizations import failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("✅ All imports successful!")
        print("Application is ready to run.")
        return 0
    else:
        print("❌ Some imports failed!")
        print("Please fix the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
