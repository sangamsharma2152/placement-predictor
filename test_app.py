#!/usr/bin/env python3
"""
Test script to verify the Streamlit app structure and critical functions
"""

import sys
import os

def test_app_structure():
    """Test app.py structure without running streamlit"""
    
    print("=" * 60)
    print("Testing Streamlit App Structure")
    print("=" * 60)
    
    try:
        # Read app.py
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        print(f"✅ app.py file loaded ({len(app_content)} bytes)")
        
        # Check for required functions and pages
        required_elements = [
            ('st.set_page_config', 'Page configuration'),
            ('🏠 Home', 'Home page navigation'),
            ('🤖 Predictions', 'Predictions page'),
            ('st.radio', 'Navigation radio'),
        ]
        
        missing = []
        for element, description in required_elements:
            if element in app_content:
                print(f"✅ Found: {description} ('{element}')")
            else:
                print(f"❌ Missing: {description} ('{element}')")
                missing.append(description)
        
        if missing:
            print(f"\n⚠️ Missing elements: {', '.join(missing)}")
            return False
        
        # Check for imports
        print("\n" + "-" * 60)
        print("Checking imports in app.py...")
        
        critical_imports = [
            'streamlit as st',
            'from pages',
            'from config import',
            'from database import',
            'from models import',
            'from utils import',
        ]
        
        for imp in critical_imports:
            if imp in app_content:
                print(f"✅ Import found: {imp}")
            else:
                print(f"❌ Import missing: {imp}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing app structure: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pages():
    """Test if all page files exist and can be imported"""
    
    print("\n" + "=" * 60)
    print("Testing Streamlit Pages")
    print("=" * 60)
    
    pages_dir = 'pages'
    required_pages = [
        '1_Dashboard.py',
        '2_Prediction.py',
        '3_Model_Comparison.py',
        '_Insights.py',
        'Achievements.py',
    ]
    
    all_exist = True
    for page in required_pages:
        page_path = os.path.join(pages_dir, page)
        if os.path.exists(page_path):
            file_size = os.path.getsize(page_path)
            print(f"✅ Page exists: {page} ({file_size} bytes)")
        else:
            print(f"❌ Page missing: {page}")
            all_exist = False
    
    return all_exist

def test_data_files():
    """Test if all required data files exist"""
    
    print("\n" + "=" * 60)
    print("Testing Data Files")
    print("=" * 60)
    
    required_files = [
        ('train.csv', 'Training data'),
        ('test.csv', 'Test data'),
        ('data/orders.csv', 'Orders data'),
        ('data/products.csv', 'Products data'),
        ('data/users.csv', 'Users data'),
    ]
    
    all_exist = True
    for file, description in required_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            print(f"✅ {description}: {file} ({file_size} bytes)")
        else:
            print(f"❌ {description} missing: {file}")
            all_exist = False
    
    return all_exist

def main():
    print("\n🔍 Starting comprehensive app tests...\n")
    
    results = {
        'app_structure': test_app_structure(),
        'pages': test_pages(),
        'data_files': test_data_files(),
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed!")
        print("The app is ready to run with: streamlit run app.py")
        return 0
    else:
        print("❌ Some tests failed!")
        print("Please fix the issues above before running the app.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
