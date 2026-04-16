"""
Achievements Page
"""

import streamlit as st
from utils import Achievement
from database import db

st.title("🏆 Achievements & Badges")

st.write("Earn achievements by reaching milestones in your placement journey!")

st.subheader("🥇 Available Achievements")

# Create grid
cols = st.columns(4)

for idx, (key, achievement) in enumerate(Achievement.ACHIEVEMENTS.items()):
    with cols[idx % 4]:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #ffd43b 0%, #fab005 100%); 
                        padding: 20px; border-radius: 10px; text-align: center; 
                        color: black; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h2>{achievement['icon']}</h2>
                <h4>{achievement['name']}</h4>
                <p style='font-size: 12px;'>{achievement['description']}</p>
            </div>
        """, unsafe_allow_html=True)

st.divider()

st.subheader("🎖️ Your Achievements")

student_id = st.text_input("Enter your Email/ID to view your achievements")

if student_id:
    achievements = db.get_achievements(student_id)
    
    if len(achievements) > 0:
        st.success(f"You have unlocked {len(achievements)} achievements! 🎉")
        
        unlocked_cols = st.columns(3)
        for idx, ach in achievements.iterrows():
            with unlocked_cols[idx % 3]:
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #51cf66 0%, #2f9e44 100%); 
                                padding: 15px; border-radius: 8px; text-align: center; color: white;'>
                        <h3>{ach['icon'] if 'icon' in ach else '⭐'}</h3>
                        <p><b>{ach['achievement_name']}</b></p>
                        <small>{ach['description']}</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No achievements unlocked yet. Keep working towards your goals!")

st.divider()

st.subheader("💡 How to Unlock Achievements")

st.write("""
**First Prediction** 🎯
- Make your first placement prediction

**High Scorer** ⭐
- Achieve CGPA above 8.5

**Coding Master** 💻
- Reach Coding Skills score of 8 or higher

**Placement Ready** 🚀
- All metrics above recommended thresholds

**Skill Builder** 🏗️
- Complete 3 or more certifications

**Intern Pro** 🏢
- Complete 3 or more internships

**Great Communicator** 🗣️
- Communication skills above 8

**Perfect Profile** 🌟
- All scores at maximum levels
""")
