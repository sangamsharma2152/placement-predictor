"""
Page: Insights & Learning Resources
"""

import streamlit as st
from config import INTERVIEW_QUESTIONS, ARTICLE_TOPICS

st.title("🧠 Insights & Conclusions")

# Key Insights
st.subheader("🔍 Key Insights from Data")

insights_data = [
    ("CGPA Impact", "CGPA strongly impacts placement chances. Students with CGPA > 7.0 have 60% higher placement rates."),
    ("Skills Matter", "Coding + Communication skills are critical. Combined score > 12 increases placement by 40%."),
    ("Internships Advantage", "Students with 2+ internships have 70% placement rate vs 30% for those without."),
    ("Backlogs Impact", "Any backlog reduces placement chances by 50%. Most companies require 0 backlogs."),
    ("Projects Experience", "Real-world projects showcase practical skills. 2+ projects increase confidence by 25%."),
    ("Certifications Value", "Relevant certifications add credibility. 2+ certs boost placement chances by 15%."),
]

for title, insight in insights_data:
    with st.expander(f"💡 {title}", expanded=False):
        st.write(insight)

st.divider()

# Interview Preparation
st.subheader("❓ Interview Preparation")

tab1, tab2, tab3 = st.tabs(["Technical", "HR", "Aptitude"])

with tab1:
    st.write("### Technical Interview Questions")
    for idx, q in enumerate(INTERVIEW_QUESTIONS.get("Technical", []), 1):
        with st.expander(f"Q{idx}: {q}"):
            st.write("💡 **Sample Answer:** [Answer will be filled based on topic]")
            st.write("**Key Points to Cover:**")
            st.write("- Concept explanation")
            st.write("- Real-world application")
            st.write("- Implementation details")

with tab2:
    st.write("### HR Interview Questions")
    for idx, q in enumerate(INTERVIEW_QUESTIONS.get("HR", []), 1):
        with st.expander(f"Q{idx}: {q}"):
            st.write("💡 **Sample Answer:** [Answer will be filled]")
            st.write("**Tips:**")
            st.write("- Be honest and authentic")
            st.write("- Provide specific examples")
            st.write("- Connect to company values")

with tab3:
    st.write("### Aptitude Interview Topics")
    for idx, q in enumerate(INTERVIEW_QUESTIONS.get("Aptitude", []), 1):
        with st.expander(f"Q{idx}: {q}"):
            st.write("💡 **Approach:** [Methodology explained]")
            st.write("**Practice Resources:**")
            st.write("- Online platforms (HackerEarth, IndiaBix)")
            st.write("- Previous year papers")

st.divider()

# Study Resources
st.subheader("📚 Recommended Study Resources")

resources = {
    "Technical Skills": {
        "Coding": ["LeetCode", "HackerRank", "CodeSignal"],
        "System Design": ["Grokking System Design", "YouTube Channels"],
        "Data Structures": ["GeeksforGeeks", "InterviewBit"]
    },
    "Soft Skills": {
        "Communication": ["Toastmasters", "Public speaking courses"],
        "Interview Prep": ["Mock interview platforms", "LinkedIn Learning"],
        "Resume": ["Resume builders", "Career coaching"]
    },
    "Company Info": {
        "Research": ["Glassdoor", "Company websites", "LinkedIn"],
        "Culture": ["YouTube videos", "Employee blogs"],
        "Salary": ["Levels.fyi", "Blind Community"]
    }
}

for category, subcats in resources.items():
    with st.expander(f"📖 {category}"):
        for subcat, items in subcats.items():
            st.write(f"**{subcat}:**")
            for item in items:
                st.write(f"- {item}")

st.divider()

# Success Stories
st.subheader("🌟 Success Stories")

success_stories = [
    {
        "name": "Amit Kumar",
        "branch": "CSE",
        "cgpa": 8.5,
        "company": "Google",
        "salary": "18 LPA",
        "key": "Focus on competitive coding"
    },
    {
        "name": "Priya Singh",
        "branch": "IT",
        "cgpa": 7.8,
        "company": "Microsoft",
        "salary": "16 LPA",
        "key": "Strong communication skills"
    },
    {
        "name": "Rahul Sharma",
        "branch": "ECE",
        "cgpa": 7.2,
        "company": "Infosys",
        "salary": "8.5 LPA",
        "key": "Multiple internships"
    }
]

for story in success_stories:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Student", story['name'])
    with col2:
        st.metric("Company", story['company'])
    with col3:
        st.metric("Package", story['salary'])
    st.write(f"**Key to Success:** {story['key']}")
    st.divider()

st.divider()

# Final Recommendations
st.subheader("🎯 Final Recommendations")

st.info("""
### To Maximize Your Placement Chances:

**Academic Excellence**
- Maintain CGPA above 7.0
- Clear all backlogs before final year
- Focus on relevant subjects

**Skill Development**
- Learn in-demand programming languages
- Build 3+ significant projects
- Get 2+ industry certifications

**Experience Building**
- Complete 2+ internships
- Contribute to open source
- Participate in hackathons

**Professional Growth**
- Develop strong communication skills
- Build a compelling resume
- Network with professionals
- Practice mock interviews

**Mental Preparation**
- Build confidence through practice
- Study company-specific patterns
- Develop problem-solving mindset
- Stay organized and motivated

✅ **Success Formula:** Academic Excellence + Technical Skills + Practical Experience + Soft Skills + Persistence
""")

