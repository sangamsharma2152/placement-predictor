"""
Page 1: Data Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from visualizations import (
    create_cgpa_distribution, create_skills_scatter, 
    create_internship_boxplot, create_correlation_heatmap,
    create_placement_pie, create_trend_chart
)
from utils import CacheManager

st.title("📊 Data Dashboard")

train = CacheManager.load_training_data("train.csv")

# Display stats
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(train))
col2.metric("Placement Rate", f"{(train['PlacementStatus'].eq('Placed').sum() / len(train) * 100):.1f}%")
col3.metric("Avg CGPA", f"{train['CGPA'].mean():.2f}")
col4.metric("Avg Skills", f"{train['Skills'].mean():.1f}")

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 Overview", "🔍 Detailed Analysis", "📊 Raw Data"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_cgpa_distribution(train), use_container_width=True)
    with col2:
        st.plotly_chart(create_placement_pie(train), use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_skills_scatter(train), use_container_width=True)
    with col2:
        st.plotly_chart(create_internship_boxplot(train), use_container_width=True)
    
    st.plotly_chart(create_correlation_heatmap(train), use_container_width=True)

with tab3:
    st.subheader(f"All {len(train)} Students Data")
    st.dataframe(train)
    
    # Download data option
    csv = train.to_csv(index=False)
    st.download_button(
        label="Download Full Dataset as CSV",
        data=csv,
        file_name="placement_data.csv",
        mime="text/csv"
    )
    
    # Filter options
    st.subheader("Filter Data")
    placement_filter = st.multiselect("Select Placement Status", train['PlacementStatus'].unique())
    
    if placement_filter:
        filtered = train[train['PlacementStatus'].isin(placement_filter)]
        st.write(f"Filtered Results: {len(filtered)} students")
        st.dataframe(filtered)
