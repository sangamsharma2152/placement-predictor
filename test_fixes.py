#!/usr/bin/env python
"""Test all model functions after fixes"""

from models import placement_model

print("Testing Model Comparison & Metrics...\n")

# Test 1: Model Comparison
comp = placement_model.get_all_models_comparison()
print("1. Model Comparison Results:")
print(comp)
print("\n" + "="*60 + "\n")

# Test 2: Feature Importance
print("2. Feature Importance (Random Forest - Top 5):")
fi = placement_model.get_feature_importance('Random Forest')
print(fi.head(5))
print("\n" + "="*60 + "\n")

# Test 3: Prediction
print("3. Testing Prediction Function:")
test_data = {
    'CGPA': 7.5,
    'Skills': 7,
    'Communication Skill Rating': 3.5,
    'Major Projects': 2,
    'Mini Projects': 1,
    'Workshops/Certificatios': 1,
    'backlogs': 0,
    'Internship': 'Yes',
    'Hackathon': 'No',
    '12th Percentage': 85,
    '10th Percentage': 88
}

pred, conf = placement_model.predict(test_data, 'Random Forest')
status = "PLACED" if pred == 1 else "NOT PLACED"
print(f"   Prediction: {status}")
print(f"   Confidence: {conf:.1f}%")
print("\n" + "="*60 + "\n")

# Test 4: Anomaly Detection
print("4. Testing Anomaly Detection:")
anomalies = placement_model.detect_anomalies(test_data)
if anomalies:
    for anomaly in anomalies:
        print(f"   - {anomaly}")
else:
    print("   No anomalies detected")
print("\n" + "="*60 + "\n")

# Test 5: Improvement Suggestions
print("5. Testing Improvement Suggestions:")
suggestions = placement_model.get_improvement_suggestions(test_data, pred)
if suggestions:
    for idx, sug in enumerate(suggestions, 1):
        print(f"   {idx}. [{sug['priority']}] {sug['suggestion']}")
        print(f"      Impact: {sug['impact']}")
else:
    print("   No suggestions available")

print("\n" + "="*60)
print("All tests completed successfully!")
print("="*60)
