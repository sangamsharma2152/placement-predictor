"""
Page 1: Data Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from visualizations import (
    create_cgpa_distribution, create_skills_scatter, 
    create_internship_boxplot, create_correlation_heatmap,
    create_placement_pie, create_trend_chart, create_backlog_analysis,
    create_hackathon_analysis
)
from utils import CacheManager

# Custom page styling with background
st.set_page_config(page_title="Dashboard", layout="wide")

# Add custom CSS for background and styling
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,250,0.95) 100%);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Student Placement Data Dashboard")
st.caption("Comprehensive analysis of 10,000 student placement records")

train = CacheManager.load_training_data("train.csv")

# Clean up dataframe - drop unnecessary columns
cols_to_drop = [col for col in train.columns if col in ['Unnamed: 0', 'StudentId']]
train = train.drop(columns=cols_to_drop, errors='ignore')

# Extended Statistics Section
st.subheader("📈 Key Metrics Overview")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Students", f"{len(train):,}")

# Safe column access with fallback
try:
    placed_count = train['PlacementStatus'].eq('Placed').sum()
    placement_rate = f"{(placed_count / len(train) * 100):.1f}%"
except KeyError:
    placed_count = 0
    placement_rate = "N/A"

col2.metric("Placement Rate", placement_rate, f"{placed_count:,} placed")
col3.metric("Avg CGPA", f"{train['CGPA'].mean():.2f}", f"Range: {train['CGPA'].min():.1f} - {train['CGPA'].max():.1f}")
col4.metric("Avg Skills", f"{train['Skills'].mean():.1f}", f"Max: {train['Skills'].max()}")

# Calculate additional stats
try:
    internship_count = train['Internship'].eq('Yes').sum()
    internship_pct = (internship_count / len(train) * 100)
    col5.metric("Internships", f"{internship_pct:.1f}%", f"{internship_count:,} students")
except:
    col5.metric("Internships", "N/A")

# Additional detailed metrics
st.subheader("📊 Additional Statistics")
col1, col2, col3, col4 = st.columns(4)

try:
    avg_10th = train['10th Percentage'].mean()
    col1.metric("Avg 10th Grade %", f"{avg_10th:.1f}%")
except:
    col1.metric("Avg 10th Grade %", "N/A")

try:
    avg_12th = train['12th Percentage'].mean()
    col2.metric("Avg 12th Grade %", f"{avg_12th:.1f}%")
except:
    col2.metric("Avg 12th Grade %", "N/A")

try:
    avg_projects = train['Major Projects'].mean()
    col3.metric("Avg Major Projects", f"{avg_projects:.1f}")
except:
    col3.metric("Avg Major Projects", "N/A")

try:
    avg_backlogs = train['backlogs'].mean()
    col4.metric("Avg Backlogs", f"{avg_backlogs:.1f}")
except:
    col4.metric("Avg Backlogs", "N/A")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🔍 Detailed Analysis", "📊 Raw Data", "🏆 Advanced Analytics"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_cgpa_distribution(train), use_container_width=True)
    with col2:
        st.plotly_chart(create_placement_pie(train), use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(create_trend_chart(train), use_container_width=True)
    with col4:
        st.markdown("### 📌 Quick Insights")
        placed = train['PlacementStatus'].eq('Placed').sum() if 'PlacementStatus' in train.columns else 0
        st.write(f"✅ **Students Placed:** {placed:,}")
        st.write(f"📍 **Placement Success Rate:** {(placed/len(train)*100):.1f}%")
        st.write(f"⭐ **Avg CGPA (Placed):** {train[train['PlacementStatus'].eq('Placed')]['CGPA'].mean():.2f}" if 'PlacementStatus' in train.columns else "")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_skills_scatter(train), use_container_width=True)
    with col2:
        st.plotly_chart(create_internship_boxplot(train), use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(create_backlog_analysis(train), use_container_width=True)
    with col4:
        st.plotly_chart(create_hackathon_analysis(train), use_container_width=True)
    
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

with tab4:
    st.subheader("🏆 Advanced Analytics & Insights")
    
    # Student Distribution by Status
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Status Distribution")
        status_counts = train['PlacementStatus'].value_counts()
        for status, count in status_counts.items():
            pct = (count / len(train)) * 100
            st.write(f"{status}: **{count}** students ({pct:.1f}%)")
    
    with col2:
        st.markdown("### Performance Ranges")
        st.write(f"🎓 **CGPA Range:** {train['CGPA'].min():.1f} - {train['CGPA'].max():.1f}")
        st.write(f"⭐ **Skills Range:** {int(train['Skills'].min())} - {int(train['Skills'].max())}")
        try:
            st.write(f"📚 **Backlog Range:** {int(train['backlogs'].min())} - {int(train['backlogs'].max())}")
        except:
            pass
    
    st.divider()
    
    # Correlation Analysis
    st.markdown("### 📊 Key Correlations with Placement")
    numeric_cols = train.select_dtypes(include=['float64', 'int64']).columns
    
    try:
        # Calculate correlations with placement outcome
        placement_numeric = train['PlacementStatus'].eq('Placed').astype(int)
        correlations = {}
        
        for col in numeric_cols:
            if col != 'backlogs':  # Skip if it causes issues
                try:
                    corr = train[col].corr(placement_numeric)
                    if pd.notna(corr):
                        correlations[col] = corr
                except:
                    pass
        
        if correlations:
            corr_df = pd.DataFrame(list(correlations.items()), columns=['Feature', 'Correlation'])
            corr_df = corr_df.sort_values('Correlation', ascending=False, key=abs)
            
            for idx, row in corr_df.iterrows():
                strength = "Strong" if abs(row['Correlation']) > 0.5 else "Moderate" if abs(row['Correlation']) > 0.3 else "Weak"
                direction = "Positive" if row['Correlation'] > 0 else "Negative"
                st.write(f"• **{row['Feature']}**: {row['Correlation']:.3f} ({strength} {direction})")
    except Exception as e:
        st.write(f"Could not calculate correlations: {e}")
