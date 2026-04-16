"""
Reports & Downloads Page
"""

import streamlit as st
import pandas as pd
from database import db
from datetime import datetime

st.title("📊 Reports & Data Downloads")

st.write("Generate reports and export your prediction data.")

tab1, tab2, tab3 = st.tabs(["📥 Export Data", "📈 Statistics Report", "🎓 Student Report"])

with tab1:
    st.subheader("Download Prediction Data")
    
    all_predictions = db.get_all_predictions()
    
    if len(all_predictions) > 0:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            branch_filter = st.multiselect("Filter by Branch", all_predictions['branch'].unique())
        
        with col2:
            status_filter = st.multiselect("Filter by Status", [0, 1], format_func=lambda x: "Placed" if x == 1 else "Not Placed")
        
        # Apply filters
        filtered_data = all_predictions
        if branch_filter:
            filtered_data = filtered_data[filtered_data['branch'].isin(branch_filter)]
        if status_filter:
            filtered_data = filtered_data[filtered_data['prediction'].isin(status_filter)]
        
        st.write(f"Total records: {len(filtered_data)}")
        st.dataframe(filtered_data)
        
        # Download options
        col_csv, col_excel = st.columns(2)
        
        with col_csv:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                f"predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col_excel:
            st.info("Excel export coming soon!")
    else:
        st.info("No data available yet!")

with tab2:
    st.subheader("📈 Statistics Report")
    
    all_predictions = db.get_all_predictions()
    
    if len(all_predictions) > 0:
        stats = {
            'Total Predictions': len(all_predictions),
            'Placed': len(all_predictions[all_predictions['prediction'] == 1]),
            'Not Placed': len(all_predictions[all_predictions['prediction'] == 0]),
            'Avg CGPA': all_predictions['cgpa'].mean(),
            'Avg Aptitude Score': all_predictions['aptitude_score'].mean(),
            'Avg Confidence': all_predictions['confidence'].mean()
        }
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Predictions", stats['Total Predictions'])
        col2.metric("Placed", stats['Placed'])
        col3.metric("Placement Rate", f"{(stats['Placed']/stats['Total Predictions']*100):.1f}%")
        
        st.divider()
        
        # Statistics by branch
        st.subheader("Statistics by Branch")
        branch_stats = all_predictions.groupby('branch').agg({
            'prediction': ['count', 'sum'],
            'cgpa': 'mean'
        }).round(2)
        
        st.dataframe(branch_stats)
    else:
        st.info("No data available yet!")

with tab3:
    st.subheader("🎓 Individual Student Report")
    
    search_email = st.text_input("Enter student email to generate report")
    
    if search_email:
        student_data = db.get_prediction(search_email)
        
        if student_data:
            st.subheader(f"Report for {student_data['name']}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Branch", student_data['branch'])
            col2.metric("CGPA", f"{student_data['cgpa']:.2f}")
            col3.metric("Status", "✅ Placed" if student_data['prediction'] == 1 else "⏳ Pending")
            
            st.divider()
            
            # Details
            col_details_a, col_details_b = st.columns(2)
            
            with col_details_a:
                st.write("**Profile Summary**")
                st.write(f"- Internships: {student_data['internships']}")
                st.write(f"- Projects: {student_data['projects']}")
                st.write(f"- Coding Skills: {student_data['coding_skills']}/10")
                st.write(f"- Communication: {student_data['communication_skills']}/10")
            
            with col_details_b:
                st.write("**Prediction Details**")
                st.write(f"- Aptitude Score: {student_data['aptitude_score']:.0f}")
                st.write(f"- Certifications: {student_data['certifications']}")
                st.write(f"- Backlogs: {student_data['backlogs']}")
                st.write(f"- Predicted Salary: {student_data['predicted_salary']}")
            
            st.divider()
            
            # Export individual report
            if st.button("📄 Generate PDF Report"):
                st.info("PDF generation coming soon!")
        else:
            st.warning("Student not found!")
