"""
Page 3: Model Comparison & Performance Analytics
"""

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from models import placement_model
from visualizations import create_model_comparison
from utils import CacheManager

st.title("📈 Model Comparison & Performance Analytics")

train = CacheManager.load_training_data("train.csv")

st.subheader("🤖 Machine Learning Models Overview")

# Get comparison
comparison = placement_model.get_all_models_comparison()

# Create visualization
fig = go.Figure()

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
for metric in metrics:
    if metric in comparison.columns:
        fig.add_trace(go.Bar(
            name=metric,
            x=comparison.index,
            y=comparison[metric],
            text=comparison[metric].apply(lambda x: f'{x:.2%}' if x else 'N/A'),
            textposition='auto'
        ))

fig.update_layout(
    title="Model Performance Comparison",
    xaxis_title="Models",
    yaxis_title="Score",
    barmode='group',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Detailed metrics table
st.subheader("📊 Detailed Metrics")
st.dataframe(comparison.round(4))

# Best model
st.subheader("🏆 Best Model")
best_model = comparison['Accuracy'].idxmax()
best_accuracy = comparison.loc[best_model, 'Accuracy']

col1, col2, col3 = st.columns(3)
col1.metric("Best Model", best_model)
col2.metric("Accuracy", f"{best_accuracy:.2%}")
col3.metric("Precision", f"{comparison.loc[best_model, 'Precision']:.2%}")

st.success(f"🎯 Recommended Model: {best_model}")

# Feature Importance
st.subheader("🎯 Feature Importance (Top 10)")
feature_imp = placement_model.get_feature_importance(best_model)

if feature_imp is not None:
    fig_imp = px.bar(
        feature_imp.head(10),
        x='Importance',
        y='Feature',
        orientation='h',
        title="Top 10 Important Features",
        color='Importance',
        color_continuous_scale='Viridis'
    )
    fig_imp.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_imp, use_container_width=True)

# Model selection for testing
st.divider()

st.subheader("🧪 Test a Model")

test_model = st.selectbox("Select Model to Test", comparison.index)

# Generate sample prediction
col_test_a, col_test_b = st.columns(2)

with col_test_a:
    test_cgpa = st.slider("Test CGPA", 0.0, 10.0, 7.0)
    test_coding = st.slider("Test Coding", 0, 10, 5)
    test_intern = st.number_input("Test Internships", 0, 10, 2)

with col_test_b:
    test_aptitude = st.slider("Test Aptitude", 0, 100, 50)
    test_comm = st.slider("Test Communication", 0, 10, 5)
    test_projects = st.number_input("Test Projects", 0, 10, 2)

if st.button("🚀 Test Model"):
    test_data = {
        'Gender': 'M',
        'Degree': 'B.Tech',
        'Branch': 'CSE',
        'CGPA': test_cgpa,
        'Internships': test_intern,
        'Projects': test_projects,
        'Coding_Skills': test_coding,
        'Communication_Skills': test_comm,
        'Aptitude_Test_Score': test_aptitude,
        'Certifications': 1,
        'Backlogs': 0,
        'Age': 22
    }
    
    pred, conf = placement_model.predict(test_data, test_model)
    
    col_result_a, col_result_b = st.columns(2)
    with col_result_a:
        st.metric("Prediction", "✅ PLACED" if pred == 1 else "❌ NOT PLACED")
    with col_result_b:
        st.metric("Confidence", f"{conf:.1f}%")

