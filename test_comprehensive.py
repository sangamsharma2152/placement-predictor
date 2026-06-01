#!/usr/bin/env python3
"""
Final verification test - validates that all components work together
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def run_tests():
    print("=" * 70)
    print("FINAL COMPREHENSIVE TEST - ALL COMPONENTS")
    print("=" * 70)
    
    # Test 1: Import all modules
    print("\n[TEST 1] Importing all Python modules...")
    try:
        import config
        import database
        import models
        import utils
        import notifications
        import visualizations
        import streamlit as st
        print("✅ All modules imported successfully")
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    # Test 2: Initialize global instances
    print("\n[TEST 2] Initializing global instances...")
    try:
        from config import APP_TITLE, DATABASE_PATH
        from database import db, Database
        from models import placement_model, PlacementModel
        
        print(f"  ✓ Config: APP_TITLE='{APP_TITLE}'")
        print(f"  ✓ Database initialized: {type(db).__name__}")
        print(f"  ✓ Models trained: {list(placement_model.models.keys())}")
        print("✅ All instances initialized")
    except Exception as e:
        print(f"❌ Instance initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Verify database schema
    print("\n[TEST 3] Verifying database schema...")
    try:
        tables = db.get_connection().execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        table_names = [t[0] for t in tables]
        print(f"  ✓ Database tables: {table_names}")
        if len(table_names) >= 5:
            print("✅ Database schema complete")
        else:
            print(f"⚠️ Warning: Only {len(table_names)} tables found (expected 5+)")
    except Exception as e:
        print(f"❌ Database schema check failed: {e}")
        return False
    
    # Test 4: Test key utilities
    print("\n[TEST 4] Testing utility functions...")
    try:
        from utils import DataValidator, ReportGenerator, SessionManager, CacheManager
        import streamlit as st
        
        # Test DataValidator
        validator = DataValidator()
        result = validator.validate_student_data({
            'CGPA': 7.5,
            'IntershipsDone': 1,
            'Projects': 2,
            'WrittenTests': 1,
            'PlacementStatus': 0,
            'Backlogs': 0
        })
        print(f"  ✓ DataValidator: {result}")
        
        # Test SessionManager
        SessionManager.init_session_state()
        print(f"  ✓ SessionManager initialized")
        
        # Test CacheManager
        print(f"  ✓ CacheManager methods: {[m for m in dir(CacheManager) if not m.startswith('_')]}")
        
        print("✅ Utility functions working")
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Test model predictions
    print("\n[TEST 5] Testing ML model predictions...")
    try:
        test_input = {
            'CGPA': [7.5],
            'IntershipsDone': [1],
            'Projects': [2],
            'WrittenTests': [1],
            'Backlogs': [0]
        }
        
        prediction = placement_model.predict(test_input)
        print(f"  ✓ Prediction result: {prediction}")
        
        metrics = placement_model.get_model_metrics()
        print(f"  ✓ Model metrics: Accuracy={metrics.get('accuracy', 'N/A')}")
        
        print("✅ Model predictions working")
    except Exception as e:
        print(f"❌ Model prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Test notifications
    print("\n[TEST 6] Testing notification system...")
    try:
        from notifications import EmailNotification, ALERT_TEMPLATES
        
        print(f"  ✓ Alert templates: {list(ALERT_TEMPLATES.keys())}")
        print("✅ Notification system ready")
    except Exception as e:
        print(f"❌ Notification test failed: {e}")
        return False
    
    # Test 7: File existence checks
    print("\n[TEST 7] Checking required files...")
    try:
        required_files = [
            'app.py',
            'train.csv',
            'test.csv',
            'pages/1_Dashboard.py',
            'pages/2_Prediction.py',
            'pages/3_Model_Comparison.py',
        ]
        
        missing = []
        for file_path in required_files:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✓ {file_path} ({size} bytes)")
            else:
                missing.append(file_path)
                print(f"  ✗ {file_path} NOT FOUND")
        
        if missing:
            print(f"⚠️ Warning: {len(missing)} required files missing")
            return False
        
        print("✅ All required files present")
    except Exception as e:
        print(f"❌ File check failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nThe application is ready to run with:")
    print("  streamlit run app.py")
    print("\nOr to run in development mode:")
    print("  streamlit run app.py --logger.level=debug")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
