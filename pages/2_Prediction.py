"""
Page 2: Advanced Predictions
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from models import placement_model
from database import db
from utils import ReportGenerator, Achievement, DataValidator, SessionManager
from config import INTERVIEW_QUESTIONS

st.title("🤖 Advanced Placement Prediction Engine")

SessionManager.init_session_state()

# Create two columns
prediction_col, results_col = st.columns([1.5, 1])

with prediction_col:
    st.subheader("📝 Enter Student Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("Full Name")
        cgpa = st.slider("CGPA (0-10)", 0.0, 10.0, 7.0, 0.1)
        major_projects = st.number_input("Major Projects", 0, 5, 1)
    
    with col2:
        email = st.text_input("Email")
        internship = st.selectbox("Internship", ["Yes", "No"])
        workshops = st.number_input("Workshops/Certificates", 0, 10, 1)
    
    with col3:
        skills = st.slider("Skills (0-10)", 0, 10, 5)
        mini_projects = st.number_input("Mini Projects", 0, 5, 1)
        communication = st.slider("Communication Rating (0-5)", 0, 5, 3, 0.5)
    
    st.divider()
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        percentage_10th = st.number_input("10th Percentage", 30, 100, 75)
    
    with col5:
        percentage_12th = st.number_input("12th Percentage", 30, 100, 75)
    
    with col6:
        backlogs = st.number_input("Backlogs", 0, 10, 0)
    
    st.divider()
    
    hackathon = st.selectbox("Hackathon Participation", ["Yes", "No"])
    
    # Model selection
    st.subheader("🤖 Model Selection")
    model_name = st.selectbox("Select Model", 
        ["Random Forest", "Logistic Regression", "Decision Tree", "SVM", "Gradient Boosting", "XGBoost"])
    
    student_data = {
        'name': name,
        'email': email,
        'CGPA': cgpa,
        'Skills': skills,
        'Communication Skill Rating': communication,
        'Major Projects': major_projects,
        'Mini Projects': mini_projects,
        'Workshops/Certificatios': workshops,
        '12th Percentage': percentage_12th,
        '10th Percentage': percentage_10th,
        'backlogs': backlogs,
        'Internship': internship,
        'Hackathon': hackathon
    }
    
    col_pred_a, col_pred_b = st.columns(2)
    
    with col_pred_a:
        predict_btn = st.button("🚀 Make Prediction", use_container_width=True)
    
    with col_pred_b:
        what_if_btn = st.checkbox("❓ What-If Analysis")

with results_col:
    if predict_btn:
        # Validate
        errors = DataValidator.validate_student_data(student_data)
        
        if errors:
            st.error("Validation Errors:")
            for error in errors:
                st.write(f"❌ {error}")
        else:
            # Make prediction
            with st.spinner("Analyzing profile..."):
                prediction, confidence = placement_model.predict(student_data, model_name)
                salary = placement_model.predict_salary(prediction, cgpa, coding_skills, internships, certifications)
                
                if prediction == 1:
                    st.success(f"✅ PLACEMENT PREDICTED\n\nConfidence: {confidence:.1f}%")
                else:
                    st.error(f"❌ NOT LIKELY TO BE PLACED\n\nConfidence: {100-confidence:.1f}%")
                
                st.info(f"💰 Expected Salary: {salary}")

st.divider()

# Detailed Analysis Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Suggestions", "🎯 Anomalies", "📊 Comparison", "❓ What-If", "📄 Report"])

with tab1:
    st.subheader("💡 Personalized Suggestions")
    if predict_btn:
        suggestions = placement_model.get_improvement_suggestions(student_data, prediction if predict_btn else 0)
        for sug in suggestions:
            with st.container():
                col_priority, col_text = st.columns([1, 4])
                with col_priority:
                    st.metric("Priority", sug['priority'])
                with col_text:
                    st.write(f"**{sug['suggestion']}**")
                    st.caption(f"Impact: {sug['impact']}")

with tab2:
    st.subheader("🔍 Anomaly Detection")
    if predict_btn:
        anomalies = placement_model.detect_anomalies(student_data)
        if anomalies:
            for anomaly in anomalies:
                st.warning(f"⚠️ {anomaly}")
        else:
            st.success("✅ No anomalies detected")

with tab3:
    st.subheader("📊 Model Comparison")
    if predict_btn:
        comparison = placement_model.get_all_models_comparison()
        st.dataframe(comparison)
        
        # Best model
        best_model = comparison['Accuracy'].idxmax()
        st.success(f"Best Model: {best_model} ({comparison.loc[best_model, 'Accuracy']:.2%} accuracy)")

with tab4:
    st.subheader("❓ What-If Analysis")
    st.write("Simulate different scenarios:")
    
    col_scenario_a, col_scenario_b = st.columns(2)
    
    with col_scenario_a:
        scenario_cgpa = st.slider("Scenario CGPA", 0.0, 10.0, cgpa, 0.1)
        scenario_coding = st.slider("Scenario Coding", 0, 10, coding_skills)
    
    with col_scenario_b:
        scenario_intern = st.number_input("Scenario Internships", 0, 10, internships)
        scenario_backlogs = st.number_input("Scenario Backlogs", 0, 10, backlogs)
    
    if st.button("Simulate"):
        scenario_data = student_data.copy()
        scenario_data.update({
            'CGPA': scenario_cgpa,
            'Coding_Skills': scenario_coding,
            'Internships': scenario_intern,
            'Backlogs': scenario_backlogs
        })
        
        scenario_pred, scenario_conf = placement_model.predict(scenario_data, model_name)
        st.info(f"Scenario Result: {'✅ PLACED' if scenario_pred == 1 else '❌ NOT PLACED'} ({scenario_conf:.1f}% confidence)")

with tab5:
    st.subheader("📄 Generate Report")
    if st.button("📥 Generate PDF Report"):
        if predict_btn:
            report_gen = ReportGenerator()
            suggestions = placement_model.get_improvement_suggestions(student_data, prediction if predict_btn else 0)
            pdf_buffer = report_gen.generate_prediction_report(student_data, prediction if predict_btn else 0, confidence if predict_btn else 0, suggestions)
            
            st.download_button(
                "Download PDF Report",
                pdf_buffer,
                f"report_{name}_{datetime.now().strftime('%Y%m%d')}.pdf",
                "application/pdf",
                use_container_width=True
            )
        else:
            st.info("Make a prediction first!")

