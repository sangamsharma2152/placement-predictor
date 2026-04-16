"""
Machine Learning Models for Placement Prediction
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from config import TRAIN_DATA, CATEGORICAL_COLS, TEST_SIZE, RANDOM_STATE, TARGET_COL

# Optional imports
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False


class PlacementModel:
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.feature_names = None
        self.scaler = None
        self.load_data()
        self.train_models()
    
    def load_data(self):
        """Load and preprocess training data"""
        self.df = pd.read_csv(TRAIN_DATA)
        self.df_original = self.df.copy()
        
        # Drop StudentId and index column if present
        cols_to_drop = [col for col in self.df.columns if col in ['StudentId', 'Unnamed: 0']]
        self.df = self.df.drop(columns=cols_to_drop, errors='ignore')
        
        # Encode categorical variables
        for col in CATEGORICAL_COLS:
            if col in self.df.columns:
                le = LabelEncoder()
                self.df[col] = le.fit_transform(self.df[col].astype(str))
                self.label_encoders[col] = le
        
        # Features and target
        self.X = self.df.drop([TARGET_COL], axis=1, errors='ignore')
        self.y = self.df[TARGET_COL]
        
        # Encode target variable if it's categorical
        if self.y.dtype == 'object':
            le_target = LabelEncoder()
            self.y = le_target.fit_transform(self.y)
            self.label_encoders['_target_'] = le_target
        
        self.feature_names = self.X.columns.tolist()
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
    
    def train_models(self):
        """Train multiple models"""
        model_configs = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1),
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            'Decision Tree': DecisionTreeClassifier(random_state=RANDOM_STATE),
            'SVM': SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE),
            'Gradient Boosting': GradientBoostingClassifier(random_state=RANDOM_STATE)
        }
        
        # Add XGBoost only if available
        if XGBOOST_AVAILABLE:
            model_configs['XGBoost'] = xgb.XGBClassifier(
                random_state=RANDOM_STATE, 
                use_label_encoder=False, 
                eval_metric='logloss'
            )
        
        self.models = {}
        for name, model in model_configs.items():
            try:
                model.fit(self.X_train, self.y_train)
                self.models[name] = model
            except Exception as e:
                print(f"Error training {name}: {e}")
    
    def get_model_accuracy(self, model_name):
        """Get accuracy of a specific model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        y_pred = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        return accuracy
    
    def get_model_metrics(self, model_name):
        """Get detailed metrics for a model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        y_pred = model.predict(self.X_test)
        
        metrics = {
            'Accuracy': accuracy_score(self.y_test, y_pred),
            'Precision': precision_score(self.y_test, y_pred),
            'Recall': recall_score(self.y_test, y_pred),
            'F1-Score': f1_score(self.y_test, y_pred)
        }
        
        try:
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            metrics['ROC-AUC'] = roc_auc_score(self.y_test, y_pred_proba)
        except:
            metrics['ROC-AUC'] = None
        
        return metrics
    
    def predict(self, input_data, model_name='Random Forest'):
        """Make prediction on new data"""
        if model_name not in self.models:
            model_name = 'Random Forest'
        
        # Prepare data
        df_input = pd.DataFrame([input_data])
        
        # Encode categorical variables
        for col in CATEGORICAL_COLS:
            if col in df_input.columns and col in self.label_encoders:
                try:
                    df_input[col] = self.label_encoders[col].transform(df_input[col])
                except:
                    df_input[col] = -1
        
        # Get model
        model = self.models[model_name]
        
        # Predict
        prediction = model.predict(df_input)[0]
        
        # Get confidence
        try:
            confidence = max(model.predict_proba(df_input)[0]) * 100
        except:
            confidence = 50 if prediction == 1 else 50
        
        return prediction, confidence
    
    def get_feature_importance(self, model_name='Random Forest'):
        """Get feature importance for a model"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        try:
            if hasattr(model, 'feature_importances_'):
                importance = model.feature_importances_
            elif hasattr(model, 'coef_'):
                importance = np.abs(model.coef_[0])
            else:
                return None
            
            feature_importance = pd.DataFrame({
                'Feature': self.feature_names,
                'Importance': importance
            }).sort_values('Importance', ascending=False)
            
            return feature_importance
        except:
            return None
    
    def get_all_models_comparison(self):
        """Compare all models"""
        results = {}
        for model_name in self.models.keys():
            results[model_name] = self.get_model_metrics(model_name)
        
        return pd.DataFrame(results).T
    
    def encode_categorical(self, value, column):
        """Encode categorical value"""
        if column in self.label_encoders:
            try:
                return self.label_encoders[column].transform([value])[0]
            except:
                return -1
        return value
    
    def predict_salary(self, prediction, cgpa, coding_skills, internships, certifications):
        """Predict expected salary based on profile"""
        if prediction == 0:
            return "Not Eligible"
        
        score = (cgpa * 0.3) + (coding_skills * 0.25) + (internships * 0.2) + (certifications * 0.25)
        
        if score < 6:
            return "3-5 LPA"
        elif score < 7:
            return "5-8 LPA"
        elif score < 8:
            return "8-12 LPA"
        else:
            return "12-20+ LPA"
    
    def detect_anomalies(self, input_data):
        """Detect anomalous profiles"""
        df_input = pd.DataFrame([input_data])
        
        for col in CATEGORICAL_COLS:
            if col in df_input.columns and col in self.label_encoders:
                try:
                    df_input[col] = self.label_encoders[col].transform(df_input[col])
                except:
                    df_input[col] = -1
        
        # Check for unusual values
        anomalies = []
        
        cgpa = input_data.get('CGPA', 0)
        if cgpa < 3.0 or cgpa > 10.0:
            anomalies.append("Unusual CGPA value")
        
        backlogs = input_data.get('backlogs', 0)
        if backlogs > 5:
            anomalies.append("High number of backlogs")
        
        skills = input_data.get('Skills', 0)
        if skills < 3:
            anomalies.append("Very low skills score")
        
        return anomalies
    
    def get_improvement_suggestions(self, input_data, prediction):
        """Get personalized suggestions"""
        suggestions = []
        
        if prediction == 0:  # Not placed
            cgpa = input_data.get('CGPA', 0)
            if cgpa < 7:
                suggestions.append({
                    'priority': 'High',
                    'suggestion': '📈 Improve CGPA to above 7.0',
                    'impact': 'Critical for placement'
                })
            
            coding = input_data.get('Coding_Skills', 0)
            if coding < 6:
                suggestions.append({
                    'priority': 'High',
                    'suggestion': '💻 Enhance coding skills (Target: 7+)',
                    'impact': 'Key for tech roles'
                })
            
            communication = input_data.get('Communication_Skills', 0)
            if communication < 6:
                suggestions.append({
                    'priority': 'High',
                    'suggestion': '🗣️ Improve communication skills',
                    'impact': 'Essential for HR round'
                })
            
            internships = input_data.get('Internships', 0)
            if internships < 2:
                suggestions.append({
                    'priority': 'Medium',
                    'suggestion': '🏢 Gain at least 2 internships',
                    'impact': 'Demonstrates practical experience'
                })
            
            projects = input_data.get('Projects', 0)
            if projects < 2:
                suggestions.append({
                    'priority': 'Medium',
                    'suggestion': '📂 Build 2+ real-world projects',
                    'impact': 'Portfolio building'
                })
            
            certifications = input_data.get('Certifications', 0)
            if certifications < 1:
                suggestions.append({
                    'priority': 'Low',
                    'suggestion': '📜 Get relevant certifications',
                    'impact': 'Adds credibility'
                })
            
            backlogs = input_data.get('Backlogs', 0)
            if backlogs > 0:
                suggestions.append({
                    'priority': 'Critical',
                    'suggestion': '❌ Clear all backlogs',
                    'impact': 'Most companies require 0 backlogs'
                })
        else:  # Placed
            if not suggestions:
                suggestions.append({
                    'priority': 'Info',
                    'suggestion': '🔥 Excellent profile! Keep improving skills',
                    'impact': 'Continue learning and growing'
                })
        
        return suggestions


# Global model instance
placement_model = PlacementModel()
