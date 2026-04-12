"""
Configuration file for Placement Predictor Application
"""

import os
from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).parent

# Database
DATABASE_PATH = BASE_DIR / "placement_predictor.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Data paths
TRAIN_DATA = BASE_DIR / "train.csv"
TEST_DATA = BASE_DIR / "test.csv"

# Email Configuration (Optional - for future use)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "")

# App Settings
APP_TITLE = "🎓 AI-Based Student Placement Advisor"
APP_DESCRIPTION = "Predict placement chances and get personalized improvement suggestions"

# Model Configuration
DEFAULT_MODEL = "Random Forest"
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Feature Names (must match CSV columns)
FEATURE_COLUMNS = [
    'Age', 'Gender', 'Degree', 'Branch', 'CGPA', 'Internships',
    'Projects', 'Coding_Skills', 'Communication_Skills',
    'Aptitude_Test_Score', 'Certifications', 'Backlogs'
]

CATEGORICAL_COLS = ['Gender', 'Degree', 'Branch']
NUMERICAL_COLS = ['CGPA', 'Internships', 'Projects', 'Coding_Skills',
                   'Communication_Skills', 'Aptitude_Test_Score',
                   'Certifications', 'Backlogs', 'Age']

TARGET_COL = 'Placement_Status'

# Thresholds
CGPA_PLACEMENT_THRESHOLD = 7.0
MIN_INTERNSHIPS = 2
MIN_PROJECTS = 2
MIN_CODING_SKILLS = 6
MIN_COMMUNICATION = 6
MIN_CERTIFICATIONS = 2
MAX_BACKLOGS = 0

# Colors
COLOR_PLACED = "#00ff00"
COLOR_NOT_PLACED = "#ff0000"
COLOR_PRIMARY = "#00ffff"
COLOR_SECONDARY = "#0f2027"

# Language Settings
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi"
}

DEFAULT_LANGUAGE = "en"

# Salary Prediction (Approximate Expected values in LPA)
SALARY_RANGES = {
    "Low": (3, 5),      # CTC: 3-5 LPA
    "Medium": (5, 8),   # CTC: 5-8 LPA
    "High": (8, 12),    # CTC: 8-12 LPA
    "Premium": (12, 20) # CTC: 12-20+ LPA
}

# Company Categories
COMPANY_CATEGORIES = {
    "IT Services": ["TCS", "Infosys", "Wipro", "HCL", "Tech Mahindra"],
    "Product": ["Microsoft", "Google", "Amazon", "Apple", "Facebook"],
    "Finance": ["Goldman Sachs", "Morgan Stanley", "Barclays", "ICICI", "HDFC"],
    "Consulting": ["Deloitte", "Accenture", "Capgemini", "EY", "KPMG"],
    "Hardware": ["Intel", "AMD", "Qualcomm", "Broadcom"]
}

# Article Categories
ARTICLE_TOPICS = [
    "Interview Preparation",
    "Resume Writing",
    "Skills Development",
    "Placement Tips",
    "Technical Interview"
]

# Interview Questions Templates
INTERVIEW_QUESTIONS = {
    "Technical": [
        "Explain the difference between Python and Java",
        "What is Object-Oriented Programming?",
        "Explain database normalization",
        "What are design patterns?",
        "Explain API and REST"
    ],
    "HR": [
        "Tell me about yourself",
        "What are your strengths and weaknesses?",
        "Why do you want to join our company?",
        "Where do you see yourself in 5 years?",
        "How do you handle stress?"
    ],
    "Aptitude": [
        "Time and Work problems",
        "Probability questions",
        "Number series",
        "Logical reasoning",
        "Verbal ability"
    ]
}
