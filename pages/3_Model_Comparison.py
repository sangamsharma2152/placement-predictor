import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

st.title("📈 Model Comparison")

train = pd.read_csv("train.csv")

le = LabelEncoder()
for col in ['Gender','Degree','Branch','Placement_Status']:
    train[col] = le.fit_transform(train[col])

X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    results[name] = acc

df = pd.DataFrame(list(results.items()), columns=["Model","Accuracy"])

fig = px.bar(df, x="Model", y="Accuracy", title="Model Accuracy Comparison")

st.plotly_chart(fig)
