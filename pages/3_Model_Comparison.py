"""
Page 3: Model Comparison & Performance Analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models import placement_model
from utils import CacheManager

st.set_page_config(page_title="Model Comparison", layout="wide", initial_sidebar_state="expanded")

st.title("Model Comparison & Performance Analytics")

# Cache the comparison data
@st.cache_data
def get_model_comparison_data():
    """Get cached model comparison"""
    return placement_model.get_all_models_comparison()

st.subheader("Machine Learning Models Overview")

# Get comparison
try:
    comparison = get_model_comparison_data()
except Exception as e:
    st.error(f"Error loading model comparison: {str(e)}")
    st.stop()

# Create visualization
try:
    fig = go.Figure()

    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    for metric in metrics:
        if metric in comparison.columns:
            fig.add_trace(go.Bar(
                name=metric,
                x=comparison.index,
                y=comparison[metric],
                text=comparison[metric].apply(lambda x: f'{x:.2%}' if pd.notna(x) and x else 'N/A'),
                textposition='auto'
            ))

    fig.update_layout(
        title="Model Performance Comparison",
        xaxis_title="Models",
        yaxis_title="Score",
        barmode='group',
        height=500,
        hovermode='x unified',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Error creating visualization: {str(e)}")

# Detailed metrics table
st.subheader("Detailed Metrics")
try:
    st.dataframe(comparison.round(4), use_container_width=True)
except Exception as e:
    st.error(f"Error displaying metrics: {str(e)}")

# Best model
st.subheader("Best Model")
try:
    best_model = comparison['Accuracy'].idxmax()
    best_accuracy = comparison.loc[best_model, 'Accuracy']
    best_precision = comparison.loc[best_model, 'Precision']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Best Model", best_model)
    with col2:
        st.metric("Accuracy", f"{best_accuracy:.2%}")
    with col3:
        st.metric("Precision", f"{best_precision:.2%}")

    st.success(f"Recommended Model: {best_model}")
except Exception as e:
    st.error(f"Error determining best model: {str(e)}")

# Feature Importance
st.subheader("Feature Importance (Top 10)")
try:
    feature_imp = placement_model.get_feature_importance(best_model)

    if feature_imp is not None and len(feature_imp) > 0:
        fig_imp = px.bar(
            feature_imp.head(10),
            x='Importance',
            y='Feature',
            orientation='h',
            title=f"Top 10 Important Features - {best_model}",
            color='Importance',
            color_continuous_scale='Viridis'
        )
        fig_imp.update_layout(
            yaxis=dict(autorange="reversed"),
            hovermode='closest',
            template='plotly_white'
        )
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.info("Feature importance not available for this model")
except Exception as e:
    st.error(f"Error retrieving feature importance: {str(e)}")

# Model selection for testing
st.divider()

st.subheader("Test a Model")

test_model = st.selectbox("Select Model to Test", comparison.index)

# Generate sample prediction
col_test_a, col_test_b = st.columns(2)

with col_test_a:
    test_cgpa = st.slider("Test CGPA", 0.0, 10.0, 7.0, step=0.1)
    test_skills = st.slider("Test Skills", 0, 10, 5)
    test_projects = st.number_input("Test Major Projects", 0, 5, 2)

with col_test_b:
    test_comm = st.slider("Test Communication", 0.0, 5.0, 3.0, step=0.1)
    test_mini = st.number_input("Test Mini Projects", 0, 5, 1)
    test_backlogs = st.number_input("Test Backlogs", 0, 10, 0)

if st.button("Test Model", key="test_model_btn"):
    try:
        test_data = {
            'CGPA': test_cgpa,
            'Skills': test_skills,
            'Communication Skill Rating': test_comm,
            'Major Projects': test_projects,
            'Mini Projects': test_mini,
            'Workshops/Certificatios': 1,
            'backlogs': test_backlogs,
            'Internship': 'Yes',
            'Hackathon': 'No',
            '12th Percentage': 75,
            '10th Percentage': 75
        }
        
        pred, conf = placement_model.predict(test_data, test_model)
        
        if pred is not None:
            col_result_a, col_result_b = st.columns(2)
            with col_result_a:
                if pred == 1:
                    st.metric("Prediction", "PLACED")
                else:
                    st.metric("Prediction", "NOT PLACED")
            with col_result_b:
                st.metric("Confidence", f"{conf:.1f}%")
            
            st.success(f"Prediction completed successfully using {test_model}")
        else:
            st.error("Prediction failed. Please check input values.")
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

