"""
Placement Predictor - Main Application
Advanced Streamlit App with Multiple Features
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from config import APP_TITLE, APP_DESCRIPTION, SUPPORTED_LANGUAGES
from database import db
from models import placement_model
from utils import SessionManager, CacheManager, ReportGenerator, Achievement, DataValidator
from notifications import EmailNotification

# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
SessionManager.init_session_state()

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .prediction-card-placed {
        background: linear-gradient(135deg, #51cf66 0%, #2f9e44 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 24px;
        margin: 10px 0;
    }
    .prediction-card-not {
        background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 24px;
        margin: 10px 0;
    }
    .suggestion-box {
        background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%);
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%);
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎓 Navigation")
    
    page = st.radio(
        "Select Page",
        [
            "🏠 Home",
            "🤖 Predictions",
            "📊 Analytics",
            "📈 Batch Upload",
            "📋 Leaderboard",
            "🎯 Goal Tracker",
            "🏆 Achievements",
            "📚 Learning Resources",
            "📊 Reports",
            "⚙️ Settings",
            "🔧 Admin Panel"
        ]
    )
    
    st.markdown("---")
    
    # Theme Toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark"):
            st.session_state.theme = 'dark'
    with col2:
        if st.button("☀️ Light"):
            st.session_state.theme = 'light'
    
    st.markdown("---")
    st.caption("Placement Predictor v2.0 Advanced")

# Main Content
if page == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Students</h3><p>Analyzing student data</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Placement Rate</h3><p>50%+ Chance</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Predictions Made</h3><p>Real-time Analysis</p></div>', unsafe_allow_html=True)
    
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)
    
    st.info("📌 **Quick Start**: Navigate to 'Predictions' to make your first placement prediction!")

elif page == "🤖 Predictions":
    st.title("🤖 Student Placement Prediction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Student Details")
        
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Student Name")
            email = st.text_input("Email Address")
            branch = st.selectbox("Branch", ["CSE", "ECE", "ME", "IT"])
            cgpa = st.slider("CGPA", 0.0, 10.0, 7.0, 0.1)
            internships = st.number_input("Internships", 0, 10, 1)
            projects = st.number_input("Projects", 0, 10, 2)
        
        with col_b:
            age = st.number_input("Age", 18, 30, 22)
            gender = st.selectbox("Gender", ["M", "F"])
            coding_skills = st.slider("Coding Skills", 0, 10, 5)
            communication_skills = st.slider("Communication Skills", 0, 10, 5)
            aptitude_score = st.slider("Aptitude Score", 0, 100, 50)
            certifications = st.number_input("Certifications", 0, 10, 1)
            backlogs = st.number_input("Backlogs", 0, 10, 0)
        
        student_data = {
            'name': name,
            'email': email, 
            'Age': age,
            'Gender': gender,
            'branch': branch,
            'Degree': 'B.Tech',
            'Branch': branch,
            'CGPA': cgpa,
            'Internships': internships,
            'Projects': projects,
            'Coding_Skills': coding_skills,
            'Communication_Skills': communication_skills,
            'Aptitude_Test_Score': aptitude_score,
            'Certifications': certifications,
            'Backlogs': backlogs
        }
        
        if st.button("🚀 Predict Placement", use_container_width=True):
            # Validate data
            errors = DataValidator.validate_student_data(student_data)
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Make prediction
                prediction, confidence = placement_model.predict(student_data)
                salary = placement_model.predict_salary(prediction, cgpa, coding_skills, internships, certifications)
                
                # Save to database
                db_data = {
                    'student_id': f"{email}_{datetime.now().timestamp()}",
                    'name': name,
                    'email': email,
                    'branch': branch,
                    'cgpa': cgpa,
                    'internships': internships,
                    'projects': projects,
                    'coding_skills': coding_skills,
                    'communication_skills': communication_skills,
                    'aptitude_score': aptitude_score,
                    'certifications': certifications,
                    'backlogs': backlogs,
                    'prediction': prediction,
                    'confidence': confidence,
                    'predicted_salary': salary
                }
                db.save_prediction(db_data)
                
                # Display result
                if prediction == 1:
                    st.markdown(f'<div class="prediction-card-placed">✅ PLACEMENT PREDICTED<br>Confidence: {confidence:.1f}%</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="prediction-card-not">❌ NOT PLACED<br>Confidence: {100-confidence:.1f}%</div>', unsafe_allow_html=True)
                
                st.success(f"Predicted Salary: {salary}")
                
                # Show suggestions
                suggestions = placement_model.get_improvement_suggestions(student_data, prediction)
                
                st.subheader("💡 Personalized Suggestions")
                for sug in suggestions:
                    with st.container():
                        st.markdown(f"<div class='suggestion-box'><b>{sug['priority']}</b> - {sug['suggestion']}<br><small>{sug['impact']}</small></div>", unsafe_allow_html=True)
                
                # Check achievements
                unlocked = Achievement.check_achievements(student_data, st.session_state.achievements)
                if unlocked:
                    st.subheader("🏆 Achievements Unlocked!")
                    for ach in unlocked:
                        achievement_info = Achievement.ACHIEVEMENTS[ach]
                        st.markdown(f"<div class='achievement-badge'>{achievement_info['icon']} {achievement_info['name']}</div>", unsafe_allow_html=True)
                        st.session_state.achievements.append(ach)
                
                # Option to download report
                st.subheader("📄 Download Report")
                report_gen = ReportGenerator()
                pdf_buffer = report_gen.generate_prediction_report(student_data, prediction, confidence, suggestions)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"placement_report_{name}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    with col2:
        st.subheader("📊 Quick Stats")
        all_preds = db.get_all_predictions()
        if len(all_preds) > 0:
            placed = all_preds[all_preds['prediction'] == 1]
            st.metric("Total Predictions", len(all_preds))
            st.metric("Placed", len(placed))
            st.metric("Avg Confidence", f"{all_preds['confidence'].mean():.1f}%")

elif page == "📊 Analytics":
    st.title("📊 Advanced Analytics & Statistics")
    
    train_df = CacheManager.load_training_data("train.csv")
    stats = CacheManager.compute_statistics(train_df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", stats['total_students'])
    col2.metric("Placement Rate", f"{stats['placement_rate']:.1f}%")
    col3.metric("Avg CGPA", f"{stats['avg_cgpa']:.2f}")
    col4.metric("Avg Aptitude", f"{stats['avg_aptitude']:.1f}")
    
    st.divider()
    
    # Import visualizations
    from visualizations import (
        create_cgpa_distribution, create_skills_scatter, create_internship_boxplot,
        create_correlation_heatmap, create_placement_pie, create_feature_importance,
        create_branch_placement, create_3d_scatter, create_sankey_diagram
    )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Overview", "🔍 Details", "🌐 3D Analysis", "🔄 Flow", "🎯 Features"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_cgpa_distribution(train_df), use_container_width=True)
        with col2:
            st.plotly_chart(create_placement_pie(train_df), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_skills_scatter(train_df), use_container_width=True)
        with col2:
            st.plotly_chart(create_branch_placement(train_df), use_container_width=True)
    
    with tab3:
        st.plotly_chart(create_3d_scatter(train_df), use_container_width=True)
    
    with tab4:
        st.plotly_chart(create_sankey_diagram(train_df), use_container_width=True)
    
    with tab5:
        feature_imp = placement_model.get_feature_importance()
        if feature_imp is not None:
            st.plotly_chart(create_feature_importance(feature_imp.head(10)), use_container_width=True)

elif page == "📈 Batch Upload":
    st.title("📈 Batch Prediction Upload")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview:")
        st.write(df.head())
        
        if st.button("Process Batch"):
            predictions = []
            progress_bar = st.progress(0)
            
            for idx, row in df.iterrows():
                pred, conf = placement_model.predict(row.to_dict())
                predictions.append({**row.to_dict(), 'Prediction': pred, 'Confidence': conf})
                progress_bar.progress((idx + 1) / len(df))
            
            pred_df = pd.DataFrame(predictions)
            st.success("Batch prediction completed!")
            st.write(pred_df)
            
            # Export
            csv = pred_df.to_csv(index=False)
            st.download_button(
                "📥 Download Results CSV",
                csv,
                f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )

elif page == "📋 Leaderboard":
    st.title("📋 Leaderboard & Rankings")
    
    all_preds = db.get_all_predictions()
    
    if len(all_preds) > 0:
        # Sort by CGPA
        leaderboard = all_preds.sort_values('cgpa', ascending=False)[['name', 'cgpa', 'confidence', 'prediction']].head(10)
        leaderboard['Rank'] = range(1, len(leaderboard) + 1)
        leaderboard['Status'] = leaderboard['prediction'].apply(lambda x: '✅ Placed' if x == 1 else '⏳ Pending')
        
        st.write(leaderboard[['Rank', 'name', 'cgpa', 'Status', 'confidence']])
    else:
        st.info("No predictions yet. Start by making predictions!")

elif page == "🎯 Goal Tracker":
    st.title("🎯 Personal Goal Tracker")
    
    student_id = st.text_input("Enter your Student ID/Email")
    
    if student_id:
        goal_type = st.selectbox("Goal Type", ["CGPA", "Coding Skills", "Communication", "Internships", "Projects"])
        target_value = st.number_input("Target Value", 1.0, 100.0, 8.0)
        
        if st.button("Set Goal"):
            db.save_goal(student_id, goal_type, target_value)
            st.success("Goal saved!")
        
        # Display goals
        goals = db.get_goals(student_id)
        if len(goals) > 0:
            st.write(goals)

elif page == "🏆 Achievements":
    st.title("🏆 Achievements & Badges")
    
    st.write("Available Achievements:")
    cols = st.columns(4)
    
    for idx, (key, achievement) in enumerate(Achievement.ACHIEVEMENTS.items()):
        with cols[idx % 4]:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%); 
                            padding: 15px; border-radius: 10px; text-align: center; color: black;'>
                    <h3>{achievement['icon']}</h3>
                    <p><b>{achievement['name']}</b></p>
                    <small>{achievement['description']}</small>
                </div>
            """, unsafe_allow_html=True)

elif page == "📚 Learning Resources":
    st.title("📚 Learning Resources & Interview Prep")
    
    from config import INTERVIEW_QUESTIONS, ARTICLE_TOPICS
    
    tab1, tab2, tab3 = st.tabs(["📖 Articles", "❓ Interview Q&A", "💡 Tips"])
    
    with tab1:
        st.subheader("Recommended Articles")
        for topic in ARTICLE_TOPICS:
            with st.expander(f"📄 {topic}"):
                st.write(f"Content about {topic} will be here...")
    
    with tab2:
        st.subheader("Interview Questions")
        category = st.selectbox("Select Category", ["Technical", "HR", "Aptitude"])
        if category in INTERVIEW_QUESTIONS:
            for idx, question in enumerate(INTERVIEW_QUESTIONS[category], 1):
                with st.expander(f"Q{idx}: {question}"):
                    st.write("Answer and explanation will be here...")
    
    with tab3:
        st.write("""
        - Practice coding daily
        - Read technical blogs
        - Join online communities
        - Build projects
        - Mock interviews
        """)

elif page == "📊 Reports":
    st.title("📊 Reports & Downloads")
    
    all_preds = db.get_all_predictions()
    
    if len(all_preds) > 0:
        st.subheader("Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = all_preds.to_csv(index=False)
            st.download_button(
                "📥 Download All Predictions (CSV)",
                csv,
                f"predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                use_container_width=True
            )
        
        with col2:
            st.write("Excel export available soon!")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings & Preferences")
    
    st.subheader("🎨 Appearance")
    theme = st.radio("Theme", ["Light", "Dark", "Auto"])
    st.session_state.theme = theme.lower()
    
    st.subheader("🌐 Language")
    language = st.selectbox("Language", list(SUPPORTED_LANGUAGES.keys()))
    st.session_state.language = language
    
    st.subheader("📧 Notifications")
    st.checkbox("Email Notifications")
    st.checkbox("SMS Alerts")
    
    st.subheader("🔒 Privacy")
    st.checkbox("Allow data collection for improvements")

elif page == "🔧 Admin Panel":
    st.title("🔧 Admin Panel")
    
    admin_password = st.text_input("Admin Password", type="password")
    
    if admin_password == "admin123":  # Change this in production
        st.success("✅ Admin access granted")
        
        tab1, tab2, tab3 = st.tabs(["👥 Users", "🗑️ Data Cleanup", "📊 Statistics"])
        
        with tab1:
            all_preds = db.get_all_predictions()
            st.write(f"Total Predictions: {len(all_preds)}")
            st.dataframe(all_preds)
        
        with tab2:
            if st.button("Clean Duplicate Records"):
                st.info("Cleaning in progress...")
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Users", len(db.get_all_predictions()))
            col2.metric("Placed", len(db.get_all_predictions()[db.get_all_predictions()['prediction'] == 1]))
            col3.metric("Avg Confidence", db.get_all_predictions()['confidence'].mean())
    else:
        st.error("❌ Incorrect password")
