"""
Diagnostic script to test all imports work correctly
Run this to verify everything installs properly
"""

import sys

print("Testing Streamlit installation...")
try:
    import streamlit as st
    print("✅ streamlit OK")
except Exception as e:
    print(f"❌ streamlit ERROR: {e}")
    sys.exit(1)

print("Testing pandas...")
try:
    import pandas as pd
    print("✅ pandas OK")
except Exception as e:
    print(f"❌ pandas ERROR: {e}")
    sys.exit(1)

print("Testing numpy...")
try:
    import numpy as np
    print("✅ numpy OK")
except Exception as e:
    print(f"❌ numpy ERROR: {e}")
    sys.exit(1)

print("Testing scikit-learn...")
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    print("✅ scikit-learn OK")
except Exception as e:
    print(f"❌ scikit-learn ERROR: {e}")
    sys.exit(1)

print("Testing plotly...")
try:
    import plotly.express as px
    print("✅ plotly OK")
except Exception as e:
    print(f"❌ plotly ERROR: {e}")
    sys.exit(1)

print("Testing xgboost...")
try:
    import xgboost as xgb
    print("✅ xgboost OK (Optional)")
except ImportError:
    print("⚠️  xgboost NOT installed (Optional - App works without it)")

print("Testing reportlab...")
try:
    from reportlab.lib.pagesizes import letter
    print("✅ reportlab OK")
except ImportError:
    print("⚠️  reportlab NOT installed (Optional - PDF export may not work)")

print("\n" + "="*50)
print("✅ CORE PACKAGES INSTALLED SUCCESSFULLY!")
print("="*50)
print("\nYou can now run: streamlit run app.py")
print("\nNote: Optional packages (xgboost, reportlab) are not required")
print("for the app to function. They add extra features if present.")
