"""
Utility functions for Placement Predictor
"""

import streamlit as st
from io import BytesIO
from datetime import datetime
import pandas as pd
import base64
import json

# Optional imports for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    """Generate PDF reports"""
    
    def __init__(self):
        if REPORTLAB_AVAILABLE:
            self.styles = getSampleStyleSheet()
        else:
            self.styles = None
    
    def generate_prediction_report(self, student_data, prediction, confidence, suggestions):
        """Generate PDF report for prediction"""
        if not REPORTLAB_AVAILABLE:
            return None  # Return None if reportlab not available
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00ffff'),
            spaceAfter=30,
            alignment=1
        )
        
        elements.append(Paragraph("🎓 Placement Prediction Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Student Info
        elements.append(Paragraph("Student Information", self.styles['Heading2']))
        student_data_list = [
            ['Field', 'Value'],
            ['Name', student_data.get('name', 'N/A')],
            ['Email', student_data.get('email', 'N/A')],
            ['Branch', student_data.get('branch', 'N/A')],
            ['CGPA', f"{student_data.get('cgpa', 0):.2f}"],
        ]
        
        student_table = Table(student_data_list)
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00ffff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(student_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Prediction Result
        elements.append(Paragraph("Prediction Result", self.styles['Heading2']))
        prediction_text = "✅ PLACED" if prediction == 1 else "❌ NOT PLACED"
        prediction_style = ParagraphStyle(
            'Prediction',
            parent=self.styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#51cf66') if prediction == 1 else colors.HexColor('#ff6b6b'),
            spaceAfter=12
        )
        elements.append(Paragraph(f"Result: {prediction_text}", prediction_style))
        elements.append(Paragraph(f"Confidence Score: {confidence:.2f}%", self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Suggestions
        elements.append(Paragraph("Improvement Suggestions", self.styles['Heading2']))
        for suggestion in suggestions:
            priority = suggestion.get('priority', '')
            text = suggestion.get('suggestion', '')
            elements.append(Paragraph(f"<b>{priority}:</b> {text}", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(footer_text, self.styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer


class DataValidator:
    """Validate and clean data"""
    
    @staticmethod
    def validate_student_data(data):
        """Validate student input data"""
        errors = []
        
        cgpa = data.get('cgpa', 0)
        if cgpa < 0 or cgpa > 10:
            errors.append("CGPA must be between 0 and 10")
        
        aptitude = data.get('aptitude_score', 0)
        if aptitude < 0 or aptitude > 100:
            errors.append("Aptitude score must be between 0 and 100")
        
        for skill in ['coding_skills', 'communication_skills']:
            value = data.get(skill, 0)
            if value < 0 or value > 10:
                errors.append(f"{skill} must be between 0 and 10")
        
        for field in ['internships', 'projects', 'certifications', 'backlogs']:
            value = data.get(field, 0)
            if value < 0:
                errors.append(f"{field} cannot be negative")
        
        return errors
    
    @staticmethod
    def clean_data(df):
        """Clean dataset"""
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Handle missing values
        numeric_cols = df_clean.select_dtypes(include=['number']).columns
        df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
        
        return df_clean


class CacheManager:
    """Manage caching"""
    
    @staticmethod
    @st.cache_data
    def load_training_data(filepath):
        """Load training data with caching and cleanup"""
        df = pd.read_csv(filepath)
        # Clean up unnecessary columns
        cols_to_drop = [col for col in df.columns if col in ['Unnamed: 0', 'StudentId']]
        df = df.drop(columns=cols_to_drop, errors='ignore')
        return df
    
    @staticmethod
    @st.cache_data
    def compute_statistics(df):
        """Compute statistics with caching"""
        stats = {
            'total_students': len(df),
            'placement_rate': (df['PlacementStatus'].eq('Placed').sum() / len(df) * 100),
            'avg_cgpa': df['CGPA'].mean(),
            'avg_skills': df['Skills'].mean(),
            'total_placed': df['PlacementStatus'].eq('Placed').sum(),
            'total_not_placed': df['PlacementStatus'].eq('NotPlaced').sum()
        }
        return stats


class ExcelExporter:
    """Export data to Excel"""
    
    @staticmethod
    def export_predictions(predictions_list):
        """Export predictions to Excel"""
        df = pd.DataFrame(predictions_list)
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Predictions', index=False)
        
        buffer.seek(0)
        return buffer


class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def init_session_state():
        """Initialize session state"""
        if 'predictions_history' not in st.session_state:
            st.session_state.predictions_history = []
        
        if 'current_student_id' not in st.session_state:
            st.session_state.current_student_id = None
        
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
        
        if 'language' not in st.session_state:
            st.session_state.language = 'en'
        
        if 'achievements' not in st.session_state:
            st.session_state.achievements = []
    
    @staticmethod
    def add_prediction_history(student_id, prediction_result):
        """Add to prediction history"""
        st.session_state.predictions_history.append({
            'student_id': student_id,
            'result': prediction_result,
            'timestamp': datetime.now()
        })
    
    @staticmethod
    def get_prediction_history():
        """Get prediction history"""
        return st.session_state.predictions_history


class Achievement:
    """Achievement system"""
    
    ACHIEVEMENTS = {
        'first_prediction': {
            'name': '🎯 First Prediction',
            'description': 'Made your first placement prediction',
            'icon': '🎯'
        },
        'high_scorer': {
            'name': '⭐ High Scorer',
            'description': 'CGPA above 8.5',
            'icon': '⭐'
        },
        'coding_master': {
            'name': '💻 Coding Master',
            'description': 'Coding skills above 8',
            'icon': '💻'
        },
        'placement_ready': {
            'name': '🚀 Placement Ready',
            'description': 'All metrics above recommended threshold',
            'icon': '🚀'
        },
        'skill_builder': {
            'name': '🏗️ Skill Builder',
            'description': 'Completed 3+ certifications',
            'icon': '🏗️'
        },
        'intern_pro': {
            'name': '🏢 Intern Pro',
            'description': 'Completed 3+ internships',
            'icon': '🏢'
        },
        'communicator': {
            'name': '🗣️ Great Communicator',
            'description': 'Communication skills above 8',
            'icon': '🗣️'
        },
        'perfect_profile': {
            'name': '🌟 Perfect Profile',
            'description': 'All scores at maximum',
            'icon': '🌟'
        }
    }
    
    @staticmethod
    def check_achievements(student_data, previous_achievements=None):
        """Check which achievements to unlock"""
        if previous_achievements is None:
            previous_achievements = []
        
        unlocked = []
        
        cgpa = student_data.get('cgpa', 0)
        if cgpa > 8.5 and 'high_scorer' not in previous_achievements:
            unlocked.append('high_scorer')
        
        coding = student_data.get('coding_skills', 0)
        if coding > 8 and 'coding_master' not in previous_achievements:
            unlocked.append('coding_master')
        
        comm = student_data.get('communication_skills', 0)
        if comm > 8 and 'communicator' not in previous_achievements:
            unlocked.append('communicator')
        
        certs = student_data.get('certifications', 0)
        if certs >= 3 and 'skill_builder' not in previous_achievements:
            unlocked.append('skill_builder')
        
        internships = student_data.get('internships', 0)
        if internships >= 3 and 'intern_pro' not in previous_achievements:
            unlocked.append('intern_pro')
        
        return unlocked
