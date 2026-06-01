
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config import TRAIN_DATA, CATEGORICAL_COLS, TARGET_COL, TEST_SIZE, RANDOM_STATE

class PlacementModel:
    def __init__(self):
        self.models={}
        self.label_encoders={}
        self.load_data()
        self.train_models()

    def load_data(self):
        self.df=pd.read_csv(TRAIN_DATA)
        self.df=self.df.drop(columns=["StudentId","Unnamed: 0"],errors="ignore")
        y=self.df[TARGET_COL].astype(str).str.lower().str.replace(" ","")
        self.y=y.map({"placed":1,"notplaced":0,"yes":1,"no":0,"1":1,"0":0}).astype(int)
        self.X=self.df.drop(columns=[TARGET_COL])
        for col in CATEGORICAL_COLS:
            if col in self.X.columns:
                le=LabelEncoder()
                self.X[col]=le.fit_transform(self.X[col].astype(str))
                self.label_encoders[col]=le
        self.X=self.X.fillna(0)
        self.feature_names=list(self.X.columns)
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(
            self.X,self.y,test_size=TEST_SIZE,random_state=RANDOM_STATE
        )

    def train_models(self):
        configs={
            "Random Forest":RandomForestClassifier(n_estimators=100,random_state=42),
            "Logistic Regression":LogisticRegression(max_iter=1000),
            "Decision Tree":DecisionTreeClassifier(),
            "SVM":SVC(probability=True),
            "Gradient Boosting":GradientBoostingClassifier()
        }
        for n,m in configs.items():
            try:
                m.fit(self.X_train,self.y_train)
                self.models[n]=m
            except Exception as e:
                print(e)

    def predict(self,input_data,model_name="Random Forest"):
        df=pd.DataFrame([input_data])
        for col in self.label_encoders:
            if col in df:
                try:
                    df[col]=self.label_encoders[col].transform(df[col].astype(str))
                except:
                    df[col]=0
        for col in self.feature_names:
            if col not in df:
                df[col]=0
        df=df[self.feature_names]
        model=self.models[model_name]
        pred=int(model.predict(df)[0])
        try:
            conf=max(model.predict_proba(df)[0])*100
        except:
            conf=50
        return pred,conf

    def predict_salary(self,prediction,cgpa,coding_skills,internships,certifications):
        if prediction==0:
            return 0
        return (cgpa*70000)+(coding_skills*50000)+(internships*80000)+(certifications*40000)

    def get_feature_importance(self,model_name="Random Forest"):
        model=self.models.get(model_name)
        if hasattr(model,"feature_importances_"):
            return pd.DataFrame({"Feature":self.feature_names,"Importance":model.feature_importances_})
        return None

    def get_model_metrics(self,name):
        m=self.models[name]
        p=m.predict(self.X_test)
        return {
        "Accuracy":accuracy_score(self.y_test,p),
        "Precision":precision_score(self.y_test,p,zero_division=0),
        "Recall":recall_score(self.y_test,p,zero_division=0),
        "F1":f1_score(self.y_test,p,zero_division=0)
        }

    def get_all_models_comparison(self):
        return pd.DataFrame({x:self.get_model_metrics(x) for x in self.models}).T

    def get_improvement_suggestions(self,*args,**kwargs):
        return []

placement_model=PlacementModel()
