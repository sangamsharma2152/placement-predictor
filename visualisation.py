"""
Visualizations for Placement Predictor
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def create_cgpa_distribution(df):
    """CGPA distribution histogram"""
    fig = px.histogram(df, x="CGPA", color="Placement_Status",
                       nbins=20, title="📊 CGPA Distribution by Placement Status",
                       labels={'CGPA': 'CGPA', 'Placement_Status': 'Status'},
                       color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    return fig


def create_skills_scatter(df):
    """Skills vs Placement scatter plot"""
    fig = px.scatter(df, x="Coding_Skills", y="Communication_Skills",
                    size="CGPA", color="Placement_Status",
                    hover_data={'Age', 'Branch'},
                    title="💡 Coding Skills vs Communication Skills",
                    color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    return fig


def create_internship_boxplot(df):
    """Internship impact on placement"""
    fig = px.box(df, x="Placement_Status", y="Internships",
                color="Placement_Status",
                title="🏢 Internship Distribution by Placement Status",
                color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
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
    counts = df['Placement_Status'].value_counts()
    fig = px.pie(values=counts.values, names=['Not Placed', 'Placed'],
                title="📈 Overall Placement Distribution",
                color_discrete_map={'Placed': '#51cf66', 'Not Placed': '#ff6b6b'},
                hole=0.3)
    return fig


def create_feature_importance(importance_df):
    """Feature importance bar chart"""
    fig = px.bar(importance_df, x="Importance", y="Feature",
                orientation='h', title="🎯 Feature Importance (Top 10)",
                color="Importance", color_continuous_scale='Viridis')
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return fig


def create_branch_placement(df):
    """Placement rate by branch"""
    branch_stats = df.groupby('Branch')['Placement_Status'].agg(['count', 'sum'])
    branch_stats['placement_rate'] = (branch_stats['sum'] / branch_stats['count'] * 100)
    branch_stats = branch_stats.reset_index()
    
    fig = px.bar(branch_stats, x='Branch', y='placement_rate',
                title="🎓 Placement Rate by Branch",
                color='placement_rate', color_continuous_scale='Viridis',
                labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_aptitude_cgpa_scatter(df):
    """Aptitude vs CGPA with placement status"""
    fig = px.scatter(df, x="Aptitude_Test_Score", y="CGPA",
                    color="Placement_Status", size="Internships",
                    hover_data={'Branch'},
                    title="🧠 Aptitude Score vs CGPA",
                    color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    return fig


def create_model_comparison(comparison_df):
    """Model accuracy comparison"""
    fig = px.bar(comparison_df.reset_index(), x='index', y='Accuracy',
                title="📊 Model Comparison - Accuracy",
                labels={'index': 'Model', 'Accuracy': 'Accuracy Score'},
                color='Accuracy', color_continuous_scale='Viridis')
    return fig


def create_gender_placement(df):
    """Placement by gender"""
    gender_stats = df.groupby('Gender')['Placement_Status'].agg(['count', 'sum'])
    gender_stats['placement_rate'] = (gender_stats['sum'] / gender_stats['count'] * 100)
    gender_stats = gender_stats.reset_index()
    
    fig = px.bar(gender_stats, x='Gender', y='placement_rate',
                title="👥 Placement Rate by Gender",
                color='placement_rate', color_continuous_scale='Viridis',
                labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_age_distribution(df):
    """Age distribution"""
    fig = px.histogram(df, x="Age", color="Placement_Status",
                      nbins=10, title="📅 Age Distribution",
                      color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    return fig


def create_backlog_analysis(df):
    """Backlogs impact on placement"""
    backlog_stats = df.groupby('Backlogs')['Placement_Status'].agg(['count', 'sum'])
    backlog_stats['placement_rate'] = (backlog_stats['sum'] / backlog_stats['count'] * 100)
    backlog_stats = backlog_stats.reset_index()
    
    fig = px.bar(backlog_stats, x='Backlogs', y='placement_rate',
                title="❌ Placement Rate by Backlogs",
                color='placement_rate', color_continuous_scale='RdYlGn',
                labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_certificates_analysis(df):
    """Certifications impact"""
    cert_stats = df.groupby('Certifications')['Placement_Status'].agg(['count', 'sum'])
    cert_stats['placement_rate'] = (cert_stats['sum'] / cert_stats['count'] * 100)
    cert_stats = cert_stats.reset_index()
    
    fig = px.line(cert_stats, x='Certifications', y='placement_rate',
                 markers=True, title="📜 Placement Rate by Certifications",
                 labels={'placement_rate': 'Placement Rate (%)'})
    return fig


def create_skills_heatmap(df):
    """Skills distribution"""
    skills_data = df[['Coding_Skills', 'Communication_Skills', 'Placement_Status']].copy()
    skills_grouped = skills_data.groupby('Placement_Status').mean()
    
    fig = px.imshow(skills_grouped, title="🔥 Average Skills by Placement Status",
                   labels={'value': 'Average Score', 'index': 'Status'},
                   color_continuous_scale='Viridis')
    return fig


def create_3d_scatter(df):
    """3D scatter plot"""
    fig = px.scatter_3d(df, x='CGPA', y='Coding_Skills',
                       z='Communication_Skills',
                       color='Placement_Status',
                       size='Aptitude_Test_Score',
                       hover_data={'Branch'},
                       title="🌐 3D Profile Analysis",
                       color_discrete_map={0: '#ff6b6b', 1: '#51cf66'})
    return fig


def create_sankey_diagram(df):
    """Sankey diagram for student flow"""
    # Simplify for Sankey
    branch_placement = df.groupby(['Branch', 'Placement_Status']).size().reset_index(name='count')
    
    source = []
    target = []
    value = []
    
    for idx, row in branch_placement.iterrows():
        source.append(row['Branch'])
        target.append('Placed' if row['Placement_Status'] == 1 else 'Not Placed')
        value.append(row['count'])
    
    all_nodes = list(df['Branch'].unique()) + ['Placed', 'Not Placed']
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(pad=15, line=dict(color='black', width=0.5), label=all_nodes),
        link=dict(
            source=[all_nodes.index(s) for s in source],
            target=[all_nodes.index(t) for t in target],
            value=value,
            color=['#51cf66' if t == 'Placed' else '#ff6b6b' for t in target]
        )
    )])
    
    fig.update_layout(title="🔄 Student Flow from Branch to Placement Status")
    return fig


def create_radar_chart(df, student_profile):
    """Radar chart for student profile comparison"""
    avg_profile = df[['CGPA', 'Coding_Skills', 'Communication_Skills',
                      'Aptitude_Test_Score', 'Internships']].mean()
    
    # Normalize values
    student_profile_norm = {
        'CGPA': student_profile.get('CGPA', 0) / 10 * 100,
        'Coding Skills': student_profile.get('Coding_Skills', 0) / 10 * 100,
        'Communication': student_profile.get('Communication_Skills', 0) / 10 * 100,
        'Aptitude': student_profile.get('Aptitude_Test_Score', 0) / 100 * 100,
        'Internships': min(student_profile.get('Internships', 0) / 5 * 100, 100)
    }
    
    avg_profile_norm = {
        'CGPA': avg_profile['CGPA'] / 10 * 100,
        'Coding Skills': avg_profile['Coding_Skills'] / 10 * 100,
        'Communication': avg_profile['Communication_Skills'] / 10 * 100,
        'Aptitude': avg_profile['Aptitude_Test_Score'] / 100 * 100,
        'Internships': min(avg_profile['Internships'] / 5 * 100, 100)
    }
    
    fig = go.Figure(data=[
        go.Scatterpolar(r=list(student_profile_norm.values()),
                       theta=list(student_profile_norm.keys()),
                       fill='toself', name='Your Profile',
                       line_color='#51cf66'),
        go.Scatterpolar(r=list(avg_profile_norm.values()),
                       theta=list(avg_profile_norm.keys()),
                       fill='toself', name='Average Profile',
                       line_color='#ffd43b')
    ])
    
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                     title="📊 Your Profile vs Average Profile")
    return fig


def create_trend_chart(df):
    """Trend analysis over age groups"""
    age_bins = [18, 20, 22, 24, 26]
    age_labels = ['18-20', '20-22', '22-24', '24+']
    df_copy = df.copy()
    df_copy['Age_Group'] = pd.cut(df_copy['Age'], bins=age_bins, labels=age_labels)
    
    trend = df_copy.groupby('Age_Group')['Placement_Status'].agg(['count', 'sum'])
    trend['placement_rate'] = (trend['sum'] / trend['count'] * 100)
    trend = trend.reset_index()
    
    fig = px.line(trend, x='Age_Group', y='placement_rate',
                 markers=True, title="📈 Placement Trend by Age Group",
                 labels={'placement_rate': 'Placement Rate (%)'})
    return fig
