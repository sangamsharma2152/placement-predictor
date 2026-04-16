"""
Visualizations for Placement Predictor - Updated for new dataset
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_cgpa_distribution(df):
    """CGPA distribution histogram"""
    try:
        fig = px.histogram(df, x="CGPA", color="PlacementStatus",
                           nbins=20, title="📊 CGPA Distribution by Placement Status",
                           labels={'CGPA': 'CGPA', 'PlacementStatus': 'Status'},
                           color_discrete_map={'Placed': '#51cf66', 'NotPlaced': '#ff6b6b'})
    except KeyError:
        # Fallback if PlacementStatus doesn't exist
        fig = px.histogram(df, x="CGPA",
                           nbins=20, title="📊 CGPA Distribution")
    return fig


def create_skills_scatter(df):
    """Skills vs Communication Rating scatter plot"""
    fig = px.scatter(df, x="Skills", y="Communication Skill Rating",
                    size="CGPA", color="PlacementStatus",
                    title="💡 Skills vs Communication Rating",
                    color_discrete_map={'Placed': '#51cf66', 'NotPlaced': '#ff6b6b'})
    return fig


def create_internship_boxplot(df):
    """Internship impact on placement"""
    try:
        fig = px.box(df, x="PlacementStatus", y="CGPA",
                    color="Internship",
                    title="🏢 CGPA Distribution by Internship Status",
                    color_discrete_map={'Yes': '#51cf66', 'No': '#ffd43b'})
    except KeyError:
        fig = px.box(df, x="Internship", y="CGPA",
                    title="🏢 CGPA Distribution by Internship Status")
    return fig


def create_correlation_heatmap(df):
    """Correlation matrix heatmap"""
    numeric_df = df.select_dtypes(include=[np.number])
    fig = px.imshow(numeric_df.corr(), text_auto=True,
                    title="🔥 Feature Correlation Heatmap",
                    color_continuous_scale='RdBu')
    return fig


def create_placement_pie(df):
    """Placement status pie chart"""
    try:
        counts = df['PlacementStatus'].value_counts()
        fig = px.pie(values=counts.values, names=counts.index,
                    title="📈 Overall Placement Distribution",
                    color_discrete_map={'Placed': '#51cf66', 'NotPlaced': '#ff6b6b'},
                    hole=0.3)
    except KeyError:
        # Fallback if PlacementStatus doesn't exist
        fig = px.pie(values=[1], names=['Data'],
                    title="📈 Placement Distribution (data unavailable)")
    return fig


def create_feature_importance(importance_df):
    """Feature importance bar chart"""
    fig = px.bar(importance_df, x="Importance", y="Feature",
                orientation='h', title="🎯 Feature Importance (Top 10)",
                color="Importance", color_continuous_scale='Viridis')
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def create_projects_analysis(df):
    """Major Projects impact on placement"""
    projects_stats = df.groupby('Major Projects')['PlacementStatus'].value_counts().unstack()
    projects_stats['placement_rate'] = (projects_stats.get('Placed', 0) / 
                                        (projects_stats.get('Placed', 0) + projects_stats.get('NotPlaced', 0)) * 100)
    projects_stats = projects_stats.reset_index()
    
    fig = px.bar(projects_stats, x='Major Projects', y='placement_rate',
                title="📌 Placement Rate by Major Projects",
                color='placement_rate', color_continuous_scale='Viridis',
                labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_percentage_scatter(df):
    """10th and 12th percentage vs CGPA"""
    fig = px.scatter(df, x="10th Percentage", y="12th Percentage",
                    size="CGPA", color="PlacementStatus",
                    title="📚 10th & 12th Percentage Distribution",
                    color_discrete_map={'Placed': '#51cf66', 'NotPlaced': '#ff6b6b'})
    return fig


def create_model_comparison(comparison_df):
    """Model accuracy comparison"""
    fig = px.bar(comparison_df.reset_index(), x='index', y='Accuracy',
                title="📊 Model Comparison - Accuracy",
                labels={'index': 'Model', 'Accuracy': 'Accuracy Score'},
                color='Accuracy', color_continuous_scale='Viridis')
    return fig


def create_backlog_analysis(df):
    """Backlogs impact on placement"""
    backlog_stats = df.groupby('backlogs')['PlacementStatus'].apply(
        lambda x: (x == 'Placed').sum() / len(x) * 100
    ).reset_index()
    backlog_stats.columns = ['backlogs', 'placement_rate']
    
    fig = px.bar(backlog_stats, x='backlogs', y='placement_rate',
                title="❌ Placement Rate by Backlogs",
                color='placement_rate', color_continuous_scale='RdYlGn',
                labels={'placement_rate': 'Placement Rate (%)', 'backlogs': 'Number of Backlogs'})
    return fig


def create_certificates_analysis(df):
    """Workshops/Certificates impact"""
    cert_stats = df.groupby('Workshops/Certificatios')['PlacementStatus'].apply(
        lambda x: (x == 'Placed').sum() / len(x) * 100
    ).reset_index()
    cert_stats.columns = ['Workshops/Certificatios', 'placement_rate']
    
    fig = px.line(cert_stats, x='Workshops/Certificatios', y='placement_rate',
                 markers=True, title="📜 Placement Rate by Workshops/Certificates",
                 labels={'placement_rate': 'Placement Rate (%)', 
                        'Workshops/Certificatios': 'Number of Workshops'})
    return fig


def create_hackathon_analysis(df):
    """Hackathon participation impact"""
    hackathon_stats = df.groupby('Hackathon')['PlacementStatus'].apply(
        lambda x: (x == 'Placed').sum() / len(x) * 100
    ).reset_index()
    hackathon_stats.columns = ['Hackathon', 'placement_rate']
    
    fig = px.bar(hackathon_stats, x='Hackathon', y='placement_rate',
                title="🏆 Placement Rate by Hackathon Participation",
                color='placement_rate', color_continuous_scale='Viridis',
                labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_trend_chart(df):
    """Placement trend by CGPA ranges"""
    df['CGPA_Range'] = pd.cut(df['CGPA'], bins=[0, 6, 7, 8, 9, 10], 
                               labels=['< 6.0', '6-7', '7-8', '8-9', '> 9'])
    cgpa_stats = df.groupby('CGPA_Range')['PlacementStatus'].apply(
        lambda x: (x == 'Placed').sum() / len(x) * 100
    ).reset_index()
    cgpa_stats.columns = ['CGPA_Range', 'placement_rate']
    
    fig = px.line(cgpa_stats, x='CGPA_Range', y='placement_rate',
                 markers=True, title="📈 Placement Trend by CGPA Range",
                 labels={'placement_rate': 'Placement Rate (%)'})
    return fig
