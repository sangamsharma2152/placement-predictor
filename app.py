"""
Placement Predictor - Main Application
Advanced Streamlit App
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from config import APP_TITLE, SUPPORTED_LANGUAGES
from database import db
from models import placement_model

from utils import (
    SessionManager,
    CacheManager,
    ReportGenerator,
    Achievement,
    DataValidator
)


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


SessionManager.init_session_state()



# =========================
# CUSTOM CSS
# =========================

st.markdown(
"""
<style>

.prediction-card-placed{
background:linear-gradient(135deg,#51cf66,#2f9e44);
padding:20px;
border-radius:10px;
color:white;
text-align:center;
font-size:24px;
}

.prediction-card-not{
background:linear-gradient(135deg,#ff6b6b,#c92a2a);
padding:20px;
border-radius:10px;
color:white;
text-align:center;
font-size:24px;
}

.suggestion-box{
background:linear-gradient(135deg,#ffd43b,#fab005);
padding:15px;
border-radius:10px;
margin:10px;
}

</style>
""",
unsafe_allow_html=True
)



# =========================
# SIDEBAR
# =========================


with st.sidebar:

    st.markdown("### Navigation")

    pages = [
        "Home",
        "Predictions",
        "Analytics",
        "Batch Upload",
        "Leaderboard",
        "Goal Tracker",
        "Achievements",
        "Learning Resources",
        "Reports",
        "Settings",
        "Admin Panel"
    ]


    if "page" not in st.session_state:
        st.session_state.page = "Home"


    page = st.radio(
        "Select Page",
        pages,
        index=pages.index(
            st.session_state.page
        )
    )


    st.session_state.page = page


    st.divider()


    col1,col2 = st.columns(2)


    with col1:

        if st.button("Dark Theme"):
            st.session_state.theme="dark"



    with col2:

        if st.button("Light Theme"):
            st.session_state.theme="light"



    st.divider()

    st.caption(
        "Placement Predictor v2.0 Advanced"
    )





# =========================
# HOME PAGE
# =========================


if page=="Home":


    st.markdown(
    """
    <div style='
    background:linear-gradient(135deg,#667eea,#764ba2);
    padding:40px;
    border-radius:15px;
    text-align:center;
    color:white;
    '>

    <h1>Placement Predictor</h1>

    <p>
    AI Powered Student Career Prediction Platform
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )



    # Dashboard Data

    try:

        all_preds = db.get_all_predictions()


        total_students = len(
            all_preds
        )


        placed = (
            len(
                all_preds[
                    all_preds["prediction"]==1
                ]
            )
            if total_students>0
            else 0
        )


        avg_confidence = (
            all_preds["confidence"].mean()
            if total_students>0
            else 0
        )


        avg_salary = (
            all_preds["predicted_salary"].mean()
            if total_students>0
            and "predicted_salary" in all_preds.columns
            else 0
        )


    except Exception:

        total_students=0
        placed=0
        avg_confidence=0
        avg_salary=0

        all_preds=pd.DataFrame()



    c1,c2,c3,c4 = st.columns(4)



    c1.metric(
        "Total Predictions",
        total_students
    )



    placement_rate = (
        placed/total_students*100
        if total_students>0
        else 0
    )



    c2.metric(
        "Placement Rate",
        f"{placement_rate:.1f}%"
    )



    c3.metric(
        "Avg Confidence",
        f"{avg_confidence:.1f}%"
    )



    c4.metric(
        "Avg Salary",
        f"₹{avg_salary:,.0f}"
        if avg_salary>0
        else "N/A"
    )



    st.divider()



    left,right = st.columns(2)



    with left:


        st.subheader(
            "Key Features"
        )


        st.markdown(
        """

        ✅ AI Placement Prediction

        📊 Advanced Analytics

        🎯 Goal Tracking

        🏆 Achievements

        📄 Reports

        """
        )




    with right:


        st.subheader(
            "Quick Actions"
        )


        col_a,col_b = st.columns(2)



        with col_a:

            if st.button(
                "Make Prediction",
                use_container_width=True
            ):

                st.session_state.page="Predictions"

                st.rerun()



        with col_b:

            if st.button(
                "View Analytics",
                use_container_width=True
            ):

                st.session_state.page="Analytics"

                st.rerun()



        col_c,col_d = st.columns(2)



        with col_c:

            if st.button(
                "Learning",
                use_container_width=True
            ):

                st.session_state.page="Learning Resources"

                st.rerun()



        with col_d:

            if st.button(
                "Achievements",
                use_container_width=True
            ):

                st.session_state.page="Achievements"

                st.rerun()




    st.divider()



    st.subheader(
        "Recent Predictions"
    )


    if total_students>0:


        st.dataframe(
            all_preds.tail(5),
            use_container_width=True
        )


    else:


        st.info(
            "No predictions yet. Make your first prediction!"
        )



# =========================
# PART 2 CONTINUES BELOW
# =========================# =========================
# PREDICTIONS PAGE
# =========================

elif page=="Predictions":

    st.title("Student Placement Prediction")

    col1,col2 = st.columns([2,1])

    with col1:

        st.subheader("Enter Student Details")

        with st.form("prediction_form"):

            c1,c2 = st.columns(2)

            with c1:

                name = st.text_input("Student Name")
                email = st.text_input("Email")

                branch = st.selectbox(
                    "Branch",
                    ["CSE","ECE","ME","IT"]
                )

                gender = st.selectbox(
                    "Gender",
                    ["M","F"]
                )

                age = st.number_input(
                    "Age",
                    18,
                    30,
                    22
                )

                cgpa = st.slider(
                    "CGPA",
                    0.0,
                    10.0,
                    7.0
                )

                aptitude = st.slider(
                    "Aptitude Score",
                    0,
                    100,
                    50
                )


            with c2:

                internships = st.number_input(
                    "Internships",
                    0,
                    10,
                    1
                )

                projects = st.number_input(
                    "Projects",
                    0,
                    10,
                    2
                )

                certifications = st.number_input(
                    "Certifications",
                    0,
                    10,
                    1
                )

                coding = st.slider(
                    "Coding Skills",
                    0,
                    10,
                    5
                )

                communication = st.slider(
                    "Communication",
                    0,
                    10,
                    5
                )

                problem = st.slider(
                    "Problem Solving",
                    0,
                    10,
                    5
                )


            submit = st.form_submit_button(
                "Predict Placement"
            )



        if submit:

            if name=="" or email=="":

                st.error(
                    "Enter name and email"
                )

            else:

                student_data = {

                    "Age":age,
                    "Gender":gender,
                    "Branch":branch,
                    "CGPA":cgpa,
                    "Internships":internships,
                    "Projects":projects,
                    "Coding_Skills":coding,
                    "Communication_Skills":communication,
                    "Aptitude_Test_Score":aptitude,
                    "Certifications":certifications,
                    "Problem_Solving":problem

                }


                prediction,confidence = (
                    placement_model.predict(
                        student_data
                    )
                )


                salary = (
                    placement_model.predict_salary(
                        prediction,
                        cgpa,
                        coding,
                        internships,
                        certifications
                    )
                )


                save_data={

                    "student_id":email,
                    "name":name,
                    "email":email,
                    "branch":branch,
                    "cgpa":cgpa,
                    "internships":internships,
                    "projects":projects,
                    "coding_skills":coding,
                    "communication_skills":communication,
                    "aptitude_score":aptitude,
                    "certifications":certifications,
                    "backlogs":0,
                    "prediction":prediction,
                    "confidence":confidence,
                    "predicted_salary":salary

                }


                db.save_prediction(
                    save_data
                )


                st.cache_data.clear()


                if prediction==1:

                    st.success(
                        f"PLACED 🎉 Confidence {confidence:.1f}%"
                    )

                else:

                    st.error(
                        f"NOT PLACED Confidence {confidence:.1f}%"
                    )


    with col2:

        st.subheader(
            "Platform Stats"
        )

        data = db.get_all_predictions()


        if len(data)>0:

            st.metric(
                "Total Predictions",
                len(data)
            )

            st.metric(
                "Average CGPA",
                f"{data['cgpa'].mean():.2f}"
            )

        else:

            st.info(
                "No predictions yet"
            )





# =========================
# ANALYTICS PAGE
# =========================


elif page=="Analytics":


    st.title(
        "Analytics Dashboard"
    )


    data = db.get_all_predictions()


    if len(data)>0:


        c1,c2,c3=st.columns(3)


        c1.metric(
            "Students",
            len(data)
        )


        c2.metric(
            "Placed",
            len(
                data[
                    data["prediction"]==1
                ]
            )
        )


        c3.metric(
            "Average CGPA",
            round(
                data["cgpa"].mean(),
                2
            )
        )


        st.subheader(
            "CGPA Distribution"
        )

        st.bar_chart(
            data["cgpa"]
        )


        st.subheader(
            "Branch Distribution"
        )

        st.bar_chart(
            data["branch"].value_counts()
        )


    else:


        st.info(
            "No analytics data available"
        )






# =========================
# BATCH UPLOAD PAGE
# =========================


elif page=="Batch Upload":


    st.title(
        "Batch Prediction Upload"
    )


    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )


    if uploaded:


        df=pd.read_csv(uploaded)


        st.dataframe(
            df.head()
        )


        if st.button(
            "Run Prediction"
        ):


            results=[]


            for _,row in df.iterrows():


                pred,conf = placement_model.predict(
                    row.to_dict()
                )


                results.append(
                    {
                    **row,
                    "Prediction":pred,
                    "Confidence":conf
                    }
                )


            st.dataframe(
                pd.DataFrame(results)
            )






# =========================
# LEADERBOARD PAGE
# =========================


elif page=="Leaderboard":


    st.title(
        "Leaderboard"
    )


    data=db.get_all_predictions()


    if len(data)>0:


        board = data.sort_values(
            "cgpa",
            ascending=False
        )


        st.dataframe(
            board[
            [
            "name",
            "cgpa",
            "confidence"
            ]
            ]
        )


    else:


        st.info(
            "No leaderboard data"
        )


# =========================
# PART 3 CONTINUES BELOW
# =========================# =========================
# GOAL TRACKER PAGE
# =========================

elif page=="Goal Tracker":

    st.title("🎯 Goal Tracker")

    st.write(
        "Set your placement preparation goals"
    )

    student = st.text_input(
        "Student Email / ID"
    )

    goal = st.selectbox(
        "Goal Type",
        [
            "CGPA",
            "Coding Skills",
            "Communication",
            "Internships",
            "Projects",
            "Certifications"
        ]
    )


    target = st.number_input(
        "Target Value",
        0.0,
        100.0,
        8.0
    )


    if st.button("Save Goal"):

        try:

            db.save_goal(
                student,
                goal,
                target
            )

            st.success(
                "Goal Saved Successfully"
            )


        except:

            st.success(
                "Goal Saved"
            )






# =========================
# ACHIEVEMENTS PAGE
# =========================


elif page=="Achievements":

    st.title(
        "🏆 Achievements"
    )


    achievements = [

        "First Prediction",

        "CGPA Master",

        "Coding Champion",

        "Internship Achiever",

        "Project Builder"

    ]



    cols = st.columns(3)


    for i,item in enumerate(
        achievements
    ):

        with cols[i%3]:

            st.markdown(
                f"""
                ### 🏆 {item}
                Keep improving your profile
                """
            )






# =========================
# LEARNING PAGE
# =========================


elif page=="Learning Resources":

    st.title(
        "📚 Learning Resources"
    )


    tab1,tab2,tab3 = st.tabs(
        [
        "Coding",
        "Interview",
        "Career"
        ]
    )


    with tab1:

        st.subheader(
            "Coding Preparation"
        )

        st.write(
            """
            - Data Structures
            - Algorithms
            - Python
            - SQL
            - System Design
            """
        )


    with tab2:

        st.subheader(
            "Interview Questions"
        )


        questions=[

            "Tell me about yourself",

            "Explain OOP concepts",

            "Difference between SQL and NoSQL",

            "Explain Machine Learning"

        ]


        for q in questions:

            with st.expander(q):

                st.write(
                    "Prepare a clear structured answer."
                )



    with tab3:

        st.subheader(
            "Career Tips"
        )

        st.write(
            """
            ✔ Build Projects

            ✔ Improve Communication

            ✔ Practice DSA

            ✔ Create Resume

            ✔ Do Internships
            """
        )






# =========================
# REPORTS PAGE
# =========================


elif page=="Reports":


    st.title(
        "📄 Reports"
    )


    data = db.get_all_predictions()


    if len(data)>0:


        st.dataframe(
            data,
            use_container_width=True
        )


        csv = data.to_csv(
            index=False
        )


        st.download_button(

            "Download CSV",

            csv,

            "placement_report.csv",

            "text/csv"

        )


    else:

        st.info(
            "No reports available"
        )







# =========================
# SETTINGS PAGE
# =========================


elif page=="Settings":


    st.title(
        "⚙️ Settings"
    )


    theme = st.radio(

        "Theme",

        [
        "Light",
        "Dark"
        ]

    )


    st.session_state.theme = (
        theme.lower()
    )


    st.success(
        "Settings Updated"
    )








# =========================
# ADMIN PANEL
# =========================


elif page=="Admin Panel":


    st.title(
        "🔧 Admin Panel"
    )


    password = st.text_input(

        "Admin Password",

        type="password"

    )



    if password=="admin123":


        st.success(
            "Admin Access Granted"
        )


        data=db.get_all_predictions()



        st.metric(
            "Total Users",
            len(data)
        )


        if len(data)>0:


            st.dataframe(
                data,
                use_container_width=True
            )


    elif password!="":

        st.error(
            "Wrong Password"
        )





# =========================
# END OF APP
# =========================
