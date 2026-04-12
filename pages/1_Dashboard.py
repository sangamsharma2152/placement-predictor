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
col2.metric("Placement Rate", f"{(train['Placement_Status'].sum() / len(train) * 100):.1f}%")
col3.metric("Avg CGPA", f"{train['CGPA'].mean():.2f}")
col4.metric("Avg Aptitude", f"{train['Aptitude_Test_Score'].mean():.1f}")

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
    st.dataframe(train.head(20))
    
    # Filter options
    st.subheader("Filter Data")
    branch_filter = st.multiselect("Select Branches", train['Branch'].unique())
    status_filter = st.multiselect("Select Placement Status", [0, 1])
    
    if branch_filter or status_filter:
        filtered = train
        if branch_filter:
            filtered = filtered[filtered['Branch'].isin(branch_filter)]
        if status_filter:
            filtered = filtered[filtered['Placement_Status'].isin(status_filter)]
        st.write(filtered)
