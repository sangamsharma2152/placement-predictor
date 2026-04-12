"""
Goal Tracker Page
"""

import streamlit as st
import pandas as pd
from database import db

st.title("🎯 Personal Goal Tracker")

st.write("Set and track your placement improvement goals.")

st.subheader("📌 Set New Goal")

col1, col2, col3 = st.columns(3)

with col1:
    student_id = st.text_input("Your Email/ID")

with col2:
    goal_type = st.selectbox("Goal Type", 
        ["CGPA", "Coding Skills", "Communication", "Internships", "Projects", "Certifications", "Aptitude Score"])

with col3:
    target_value = st.number_input("Target Value", 0.0, 100.0, 8.0)

if st.button("🎯 Set Goal"):
    db.save_goal(student_id, goal_type, target_value)
    st.success(f"Goal set: {goal_type} → {target_value}")

st.divider()

st.subheader("📈 Your Goals")

if student_id:
    goals = db.get_goals(student_id)
    
    if len(goals) > 0:
        for idx, goal in goals.iterrows():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**{goal['goal_type']}**")
            
            with col2:
                progress = goal['progress']
                st.progress(progress / 100 if progress else 0)
            
            with col3:
                st.write(f"{progress:.0f}%")
            
            # Update progress
            new_value = st.slider(
                f"Update {goal['goal_type']}",
                0.0, float(goal['target_value']),
                float(goal['current_value']),
                key=f"slider_{goal['id']}"
            )
            
            if st.button(f"Update {goal['id']}", key=f"btn_{goal['id']}"):
                db.update_goal_progress(goal['id'], new_value)
                st.success("Goal updated!")
            
            st.divider()
    else:
        st.info("No goals set yet! Create one above.")
