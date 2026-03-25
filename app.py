import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Placement Predictor", layout="wide")

st.title("🎓 Student Placement Predictor Dashboard")

# -----------------------------
# Load Data
# -----------------------------
train = pd.read_csv("train.csv")

# Show dataset
if st.checkbox("Show Dataset"):
    st.dataframe(train.head())

# -----------------------------
# Encode categorical columns
# -----------------------------
le = LabelEncoder()

categorical_cols = ['Gender', 'Degree', 'Branch', 'Placement_Status']

for col in categorical_cols:
    if col in train.columns:
        train[col] = le.fit_transform(train[col])

# -----------------------------
# Features & Model
# -----------------------------
X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# SIDEBAR INPUT (DYNAMIC)
# -----------------------------
st.sidebar.header("📥 Enter Student Details")

input_dict = {}

for col in X.columns:
    if col == "CGPA":
        input_dict[col] = st.sidebar.slider("CGPA", 0.0, 10.0, 7.0)

    elif col in ["Internships", "Projects", "Certifications", "Backlogs"]:
        input_dict[col] = st.sidebar.number_input(col, 0, 10, 1)

    elif col in ["Coding_Skills", "Communication_Skills"]:
        input_dict[col] = st.sidebar.slider(col, 0, 10, 5)

    elif col == "Aptitude_Test_Score":
        input_dict[col] = st.sidebar.slider("Aptitude Score", 0, 100, 50)

    else:
        # For any unexpected column
        input_dict[col] = st.sidebar.number_input(col, 0, 100, 0)

# -----------------------------
# Prediction (FIXED)
# -----------------------------
if st.sidebar.button("Predict Placement"):

    input_df = pd.DataFrame([input_dict])

    # Ensure correct column order
    input_df = input_df[X.columns]

    prediction = model.predict(input_df)

    if prediction[0] == 1:
        st.success("🎉 Student will be PLACED")
    else:
        st.error("❌ Student will NOT be placed")

# -----------------------------
# 📊 CGPA DISTRIBUTION
# -----------------------------
st.subheader("📊 CGPA Distribution Analysis")

fig1 = px.histogram(train, x="CGPA", color="Placement_Status", nbins=20)
st.plotly_chart(fig1, use_container_width=True)

st.info("👉 Higher CGPA increases placement chances.")

# -----------------------------
# 📊 SKILLS ANALYSIS
# -----------------------------
st.subheader("📊 Skills Impact")

fig2 = px.scatter(train,
                  x="Coding_Skills",
                  y="Communication_Skills",
                  size="CGPA",
                  color="Placement_Status")

st.plotly_chart(fig2, use_container_width=True)

st.info("👉 Balanced skills = better placement.")

# -----------------------------
# 📊 INTERNSHIP ANALYSIS
# -----------------------------
st.subheader("📊 Internship Impact")

fig3 = px.box(train,
              x="Placement_Status",
              y="Internships",
              color="Placement_Status")

st.plotly_chart(fig3, use_container_width=True)

st.info("👉 More internships improve placement chances.")

# -----------------------------
# 📊 HEATMAP
# -----------------------------
st.subheader("📊 Correlation Heatmap")

corr = train.corr()

fig4 = px.imshow(corr, text_auto=True)
st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# 📊 PIE CHART
# -----------------------------
st.subheader("📊 Placement Distribution")

counts = train['Placement_Status'].value_counts()

fig5 = px.pie(
    names=["Not Placed", "Placed"],
    values=counts.values,
    hole=0.4
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# 📊 FEATURE IMPORTANCE
# -----------------------------
st.subheader("📊 Feature Importance")

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

fig6 = px.bar(imp_df, x="Feature", y="Importance")
st.plotly_chart(fig6, use_container_width=True)

# -----------------------------
# 🎬 ANIMATION
# -----------------------------
st.subheader("🎬 Animated Placement Trend")

fig7 = px.scatter(train,
                  x="CGPA",
                  y="Aptitude_Test_Score",
                  color="Placement_Status",
                  size="Coding_Skills",
                  animation_frame="Age")

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------
# 🧠 CONCLUSION
# -----------------------------
st.subheader("🧠 Final Insights")

st.markdown("""
- CGPA strongly affects placement  
- Skills are critical  
- Internships improve chances  
- Backlogs reduce placement  

👉 Balanced profile leads to success 🚀
""")
