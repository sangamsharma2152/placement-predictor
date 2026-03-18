import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Data Dashboard")

train = pd.read_csv("train.csv")

st.dataframe(train.head())

# Scatter
fig = px.scatter(train, x="CGPA", y="Aptitude_Test_Score",
                 color="Placement_Status",
                 animation_frame="Age")

st.plotly_chart(fig, use_container_width=True)

# Heatmap
corr = train.corr()
fig2 = px.imshow(corr, text_auto=True)
st.plotly_chart(fig2)

# Distribution
fig3 = px.histogram(train, x="CGPA", color="Placement_Status")
st.plotly_chart(fig3)
