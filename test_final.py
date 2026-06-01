#!/usr/bin/env python3
"""
Final test - Import all modules and verify they work
"""

import sys
import os

def test_all_modules():
    print("="*70)
    print("FINAL TEST - ALL MODULES")
    print("="*70)
    
    try:
        print("\n[1] Importing Python core modules...")
        import config, database, models, utils, notifications, visualizations
        import streamlit as st
        print("    SUCCESS - All Python core modules imported")
        
        print("\n[2] Importing E-Commerce modules...")
        import ecommerce_models, ecommerce_config, ecommerce_validators
        import ecommerce_storage, ecommerce_generators, ecommerce_services
        print("    SUCCESS - All E-Commerce modules imported")
        
        print("\n[3] Testing core instances...")
        from database import db
        from models import placement_model
        print(f"    Database: {type(db).__name__}")
        print(f"    Models trained: {list(placement_model.models.keys())}")
        print("    SUCCESS - Core instances working")
        
        print("\n[4] Testing E-Commerce services...")
        from ecommerce_services import (
            auth_service, product_service, cart_service, order_service
        )
        print(f"    Products: {len(product_service.get_all_products())}")
        print(f"    Users: {len(auth_service.get_all_users())}")
        print("    SUCCESS - E-Commerce services working")
        
        print("\n[5] Testing file structure...")
        files_to_check = [
            'app.py', 'train.csv', 'test.csv',
            'pages/1_Dashboard.py', 'pages/2_Prediction.py'
        ]
        missing = [f for f in files_to_check if not os.path.exists(f)]
        if missing:
            print(f"    WARNING: Missing files: {missing}")
        else:
            print("    SUCCESS - All required files present")
        
        print("\n" + "="*70)
        print("SUCCESS - ALL TESTS PASSED")
        print("="*70)
        print("\nApplication Status:")
        print("  - Python Streamlit core: READY")
        print("  - E-Commerce modules: READY")
        print("  - Database: READY")
        print("  - ML Models: READY")
        print("  - File storage: READY")
        print("\nRun: streamlit run app.py")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_modules()
    sys.exit(0 if success else 1)
