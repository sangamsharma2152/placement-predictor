import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import streamlit.components.v1 as components

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Placement Predictor", layout="wide")

# -----------------------------
# 🔥 FULL SCREEN VANTA BACKGROUND
# -----------------------------
components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body, html {
    margin: 0;
    padding: 0;
    overflow: hidden;
}

#vanta-bg {
    position: fixed;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    top: 0;
    left: 0;
}
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>
</head>

<body>
<div id="vanta-bg"></div>

<script>
VANTA.NET({
  el: "#vanta-bg",
  mouseControls: true,
  touchControls: true,
  gyroControls: false,
  color: 0x00ffff,
  backgroundColor: 0x0f2027
});
</script>

</body>
</html>
""", height=0)

# -----------------------------
# MAKE STREAMLIT TRANSPARENT
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.block-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🎓 AI-Based Student Placement Advisor")

# -----------------------------
# LOAD DATA
# -----------------------------
train = pd.read_csv("train.csv")

if st.checkbox("Show Dataset"):
    st.dataframe(train.head())

# -----------------------------
# ENCODING
# -----------------------------
le = LabelEncoder()
categorical_cols = ['Gender', 'Degree', 'Branch', 'Placement_Status']

for col in categorical_cols:
    if col in train.columns:
        train[col] = le.fit_transform(train[col])

# -----------------------------
# MODEL
# -----------------------------
X = train.drop(['Student_ID','Placement_Status'], axis=1)
y = train['Placement_Status']

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# INPUT SECTION
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
        input_dict[col] = st.sidebar.number_input(col, 0, 100, 0)

# -----------------------------
# PREDICTION + SUGGESTIONS
# -----------------------------
if st.sidebar.button("Predict Placement"):

    input_df = pd.DataFrame([input_dict])
    input_df = input_df[X.columns]

    prediction = model.predict(input_df)

    if prediction[0] == 1:
        st.success("🎉 Student will be PLACED")
    else:
        st.error("❌ Student will NOT be placed")

    # Suggestions
    st.subheader("🧠 Personalized Improvement Suggestions")

    suggestions = []

    if input_dict.get("CGPA", 0) < 7:
        suggestions.append("📈 Improve CGPA (target above 7)")

    if input_dict.get("Coding_Skills", 0) < 6:
        suggestions.append("💻 Improve coding skills")

    if input_dict.get("Communication_Skills", 0) < 6:
        suggestions.append("🗣 Improve communication skills")

    if input_dict.get("Internships", 0) < 2:
        suggestions.append("🏢 Gain internship experience")

    if input_dict.get("Projects", 0) < 2:
        suggestions.append("📂 Build more projects")

    if input_dict.get("Certifications", 0) < 2:
        suggestions.append("📜 Add certifications")

    if input_dict.get("Backlogs", 0) > 0:
        suggestions.append("❌ Clear backlogs")

    if suggestions:
        for s in suggestions:
            st.warning(s)
    else:
        st.success("🔥 Excellent profile!")

    # Final Advice
    st.subheader("🎯 Final Evaluation")

    if prediction[0] == 1:
        st.info("You are on the right track. Keep improving!")
    else:
        st.info("Focus on improvements to increase placement chances.")

# -----------------------------
# VISUALIZATION
# -----------------------------

st.subheader("📊 CGPA Distribution")
fig1 = px.histogram(train, x="CGPA", color="Placement_Status")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Skills Analysis")
fig2 = px.scatter(train,
                  x="Coding_Skills",
                  y="Communication_Skills",
                  size="CGPA",
                  color="Placement_Status")
st.plotly_chart(fig2)

st.subheader("📊 Internship Impact")
fig3 = px.box(train,
              x="Placement_Status",
              y="Internships",
              color="Placement_Status")
st.plotly_chart(fig3)

st.subheader("📊 Correlation Heatmap")
fig4 = px.imshow(train.corr(), text_auto=True)
st.plotly_chart(fig4)

st.subheader("📊 Placement Distribution")
counts = train['Placement_Status'].value_counts()
fig5 = px.pie(names=["Not Placed", "Placed"],
              values=counts.values,
              hole=0.4)
st.plotly_chart(fig5)

st.subheader("📊 Feature Importance")
importance = model.feature_importances_
imp_df = pd.DataFrame({"Feature": X.columns, "Importance": importance})
fig6 = px.bar(imp_df, x="Feature", y="Importance")
st.plotly_chart(fig6)

st.subheader("🎬 Animated Trend")
fig7 = px.scatter(train,
                  x="CGPA",
                  y="Aptitude_Test_Score",
                  color="Placement_Status",
                  size="Coding_Skills",
                  animation_frame="Age")
st.plotly_chart(fig7)

# -----------------------------
# CONCLUSION
# -----------------------------
st.subheader("🧠 Conclusion")

st.markdown("""
- CGPA, skills, and internships are key factors  
- Backlogs reduce placement chances  
- Balanced profile leads to success  

👉 This system predicts AND guides improvement
""")
