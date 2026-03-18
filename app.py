import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

import plotly.express as px

fig = px.scatter(train, x="CGPA", y="Aptitude_Test_Score",
                 color="Placement_Status")

st.plotly_chart(fig)

st.set_page_config(page_title="Placement Predictor", layout="wide")

st.title("🎓 Student Placement Predictor")

# -----------------------------
# Load Data
# -----------------------------
train = pd.read_csv("train.csv")

if st.checkbox("Show Dataset"):
    st.dataframe(train.head())

# -----------------------------
# Encoding
# -----------------------------
le = LabelEncoder()

for col in ['Gender','Degree','Branch','Placement_Status']:
    train[col] = le.fit_transform(train[col])

X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# USER INPUT SECTION
# -----------------------------
st.sidebar.header("Enter Student Details")

cgpa = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0)
internships = st.sidebar.number_input("Internships", 0, 10, 1)
projects = st.sidebar.number_input("Projects", 0, 10, 2)
coding = st.sidebar.slider("Coding Skills", 0, 10, 5)
communication = st.sidebar.slider("Communication Skills", 0, 10, 5)
aptitude = st.sidebar.slider("Aptitude Score", 0, 100, 50)
certifications = st.sidebar.number_input("Certifications", 0, 10, 1)
backlogs = st.sidebar.number_input("Backlogs", 0, 10, 0)

# -----------------------------
# Prediction
# -----------------------------
if st.sidebar.button("Predict Placement"):

    input_data = np.array([[cgpa, internships, projects, coding,
                            communication, aptitude,
                            certifications, backlogs]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("🎉 Student will be PLACED")
    else:
        st.error("❌ Student will NOT be placed")

# -----------------------------
# 📊 INTERACTIVE GRAPH (Plotly)
# -----------------------------
st.subheader("📊 CGPA vs Placement")

fig = px.scatter(train,
                 x="CGPA",
                 y="Aptitude_Test_Score",
                 color="Placement_Status",
                 size="Coding_Skills",
                 title="Placement Analysis",
                 animation_frame="Age")   # 🔥 animation

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 📊 Feature Importance
# -----------------------------
st.subheader("📊 Feature Importance")

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

fig2 = px.bar(imp_df, x="Feature", y="Importance", title="Feature Importance")

st.plotly_chart(fig2, use_container_width=True)
