import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

st.title("🤖 Placement Prediction")

train = pd.read_csv("train.csv")

le = LabelEncoder()
for col in ['Gender','Degree','Branch','Placement_Status']:
    train[col] = le.fit_transform(train[col])

X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

model = RandomForestClassifier()
model.fit(X, y)

# Inputs
cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
internships = st.number_input("Internships", 0, 10, 1)
projects = st.number_input("Projects", 0, 10, 2)
coding = st.slider("Coding Skills", 0, 10, 5)
communication = st.slider("Communication Skills", 0, 10, 5)
aptitude = st.slider("Aptitude Score", 0, 100, 50)
certifications = st.number_input("Certifications", 0, 10, 1)
backlogs = st.number_input("Backlogs", 0, 10, 0)

if st.button("Predict"):
    data = np.array([[cgpa, internships, projects, coding,
                      communication, aptitude,
                      certifications, backlogs]])

    pred = model.predict(data)

    if pred[0] == 1:
        st.success("🎉 Placed")
    else:
        st.error("❌ Not Placed")
