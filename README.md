# Placement Predictor 🎓

An AI-powered Streamlit application that predicts student placement chances and provides personalized improvement suggestions.

## Features

- **📊 Data Dashboard**: Visualize student data with interactive charts
- **🤖 Placement Prediction**: Predict placement chances based on student profile
- **📈 Model Comparison**: Compare different ML models (Logistic Regression, Decision Tree, Random Forest)
- **🧠 Insights & Recommendations**: Get personalized suggestions for improvement
- **🎨 Beautiful UI**: Modern interface with animated backgrounds

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sangamsharma2152/placement-predictor.git
cd placement-predictor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
placement_predictor/
├── app.py                          # Main application
├── requirements.txt                # Python dependencies
├── train.csv                       # Training dataset
├── test.csv                        # Test dataset
├── .devcontainer/
│   └── devcontainer.json          # Dev container configuration
└── pages/
    ├── 1_Dashboard.py             # Data visualization dashboard
    ├── 2_Prediction.py            # Individual prediction page
    ├── 3_Model_Comparison.py      # ML model comparison
    └── _Insights.py               # Insights and conclusions
```

## Dataset

The project uses a student placement dataset with the following features:

- **Student_ID**: Unique identifier
- **Age**: Student age
- **Gender**: Student gender
- **Degree**: Educational degree (B.Tech, etc.)
- **Branch**: Engineering branch (CSE, ECE, ME, IT)
- **CGPA**: Cumulative GPA
- **Internships**: Number of internships completed
- **Projects**: Number of projects completed
- **Coding_Skills**: Coding skill rating (0-10)
- **Communication_Skills**: Communication skill rating (0-10)
- **Aptitude_Test_Score**: Aptitude test score (0-100)
- **Certifications**: Number of certifications
- **Backlogs**: Number of backlogs
- **Placement_Status**: Placed (1) or Not Placed (0)

## Pages

### 1. Dashboard (1_Dashboard.py)
- View dataset statistics
- CGPA vs Aptitude score scatter plot
- Correlation heatmap
- CGPA distribution histogram

### 2. Prediction (2_Prediction.py)
- Input student details using interactive sliders
- Get instant placement prediction
- Machine learning powered by Random Forest

### 3. Model Comparison (3_Model_Comparison.py)
- Compare three different ML models
- Evaluate accuracy of each model
- Visual comparison charts

### 4. Insights (_Insights.py)
- Key insights about placement factors
- Conclusion on what affects placement success

## Key Insights

- **CGPA strongly impacts placement** - Maintain above 7.0 for better chances
- **Coding + Communication skills are critical** - Balance both technical and soft skills
- **Internships improve success rate** - Gain practical experience
- **Backlogs reduce placement chances** - Keep academics clean

## Technologies Used

- **Streamlit**: Web framework for data apps
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning models
- **Plotly**: Interactive visualizations
- **Python**: Programming language

## Models

The project uses the following ML models for prediction:

1. **Random Forest Classifier** - Main prediction model (highest accuracy)
2. **Logistic Regression** - Linear classification
3. **Decision Tree** - Tree-based classification

## Future Enhancements

- Add more features and data preprocessing
- Implement deep learning models
- Add exported reports feature
- Include more visualizations
- Add historical data tracking

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Author

Sangam Sharma - [GitHub Profile](https://github.com/sangamsharma2152)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This is a demo project for educational purposes. Placement prediction depends on many more factors beyond what's captured in this model.
