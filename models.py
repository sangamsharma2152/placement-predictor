"""
Machine Learning Models for Placement Prediction
Error Free Version
"""

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


from config import (
    TRAIN_DATA,
    CATEGORICAL_COLS,
    TEST_SIZE,
    RANDOM_STATE,
    TARGET_COL
)



# ==============================
# OPTIONAL XGBOOST
# ==============================

try:

    import xgboost as xgb
    XGBOOST_AVAILABLE = True

except:

    XGBOOST_AVAILABLE = False




class PlacementModel:


    def __init__(self):

        self.models = {}

        self.label_encoders = {}

        self.feature_names = []

        self.load_data()

        self.train_models()



    # ==========================
    # LOAD DATA
    # ==========================


    def load_data(self):


        self.df = pd.read_csv(TRAIN_DATA)


        self.df.columns = (
            self.df.columns
            .str.strip()
        )


        self.df = self.df.drop(
            columns=[
                "StudentId",
                "Unnamed: 0"
            ],
            errors="ignore"
        )



        # --------------------
        # FIX TARGET COLUMN
        # --------------------


        self.df[TARGET_COL] = (
            self.df[TARGET_COL]
            .astype(str)
            .str.strip()
            .str.lower()
        )


        self.df[TARGET_COL] = (
            self.df[TARGET_COL]
            .replace(
                {
                    "placed":1,
                    "not placed":0,
                    "yes":1,
                    "no":0,
                    "true":1,
                    "false":0
                }
            )
        )


        self.df[TARGET_COL] = pd.to_numeric(
            self.df[TARGET_COL],
            errors="coerce"
        )


        self.df = self.df.dropna(
            subset=[TARGET_COL]
        )


        self.df[TARGET_COL] = (
            self.df[TARGET_COL]
            .astype(int)
        )



        # --------------------
        # FEATURES
        # --------------------


        self.X = self.df.drop(
            TARGET_COL,
            axis=1
        )


        self.y = self.df[TARGET_COL]



        # categorical encoding

        for col in CATEGORICAL_COLS:


            if col in self.X.columns:


                encoder = LabelEncoder()


                self.X[col] = (
                    encoder
                    .fit_transform(
                        self.X[col]
                        .astype(str)
                    )
                )


                self.label_encoders[col] = encoder




        # fill missing

        self.X = self.X.fillna(0)



        self.feature_names = (
            self.X.columns
            .tolist()
        )



        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(

            self.X,

            self.y,

            test_size=TEST_SIZE,

            random_state=RANDOM_STATE,

            stratify=self.y

        )





    # ==========================
    # TRAIN MODELS
    # ==========================


    def train_models(self):


        model_list = {


            "Random Forest":

                RandomForestClassifier(
                    n_estimators=200,
                    random_state=RANDOM_STATE
                ),


            "Logistic Regression":

                LogisticRegression(
                    max_iter=2000
                ),


            "Decision Tree":

                DecisionTreeClassifier(
                    random_state=RANDOM_STATE
                ),


            "SVM":

                SVC(
                    probability=True
                ),


            "Gradient Boosting":

                GradientBoostingClassifier()

        }



        if XGBOOST_AVAILABLE:


            model_list["XGBoost"] = (

                xgb.XGBClassifier(

                    eval_metric="logloss"

                )

            )




        for name,model in model_list.items():


            try:


                model.fit(
                    self.X_train,
                    self.y_train
                )


                self.models[name]=model


                print(
                    name,
                    "trained"
                )


            except Exception as e:


                print(
                    name,
                    e
                )





    # ==========================
    # PREDICTION
    # ==========================


    def predict(
        self,
        input_data,
        model_name="Random Forest"
    ):


        df = pd.DataFrame(
            [input_data]
        )



        for col in CATEGORICAL_COLS:


            if col in df.columns:


                try:

                    df[col] = (
                        self.label_encoders[col]
                        .transform(
                            df[col].astype(str)
                        )
                    )


                except:


                    df[col]=0




        for col in self.feature_names:


            if col not in df.columns:

                df[col]=0




        df = df[
            self.feature_names
        ]



        model = self.models[
            model_name
        ]



        prediction = (
            model.predict(df)[0]
        )



        try:

            confidence = (
                max(
                    model.predict_proba(df)[0]
                )
                *100
            )

        except:

            confidence=50



        return (
            int(prediction),
            confidence
        )






    # ==========================
    # MODEL METRICS
    # ==========================


    def get_model_metrics(
        self,
        model_name
    ):


        if model_name not in self.models:

            return None



        model=self.models[model_name]


        pred=model.predict(
            self.X_test
        )


        result={


            "Accuracy":

            accuracy_score(
                self.y_test,
                pred
            ),


            "Precision":

            precision_score(
                self.y_test,
                pred,
                zero_division=0
            ),


            "Recall":

            recall_score(
                self.y_test,
                pred,
                zero_division=0
            ),


            "F1-Score":

            f1_score(
                self.y_test,
                pred,
                zero_division=0
            )

        }


        try:

            result["ROC-AUC"] = (

                roc_auc_score(

                    self.y_test,

                    model.predict_proba(
                        self.X_test
                    )[:,1]

                )

            )


        except:

            result["ROC-AUC"]=0



        return result





    def get_all_models_comparison(self):


        return pd.DataFrame(

            {

            name:self.get_model_metrics(name)

            for name in self.models

            }

        ).T





    def get_feature_importance(
        self,
        model_name="Random Forest"
    ):


        model=self.models.get(
            model_name
        )


        if not model:

            return None



        if hasattr(
            model,
            "feature_importances_"
        ):


            return pd.DataFrame(

                {

                "Feature":
                self.feature_names,


                "Importance":
                model.feature_importances_

                }

            ).sort_values(

                "Importance",

                ascending=False

            )



        return None




    def predict_salary(
        self,
        prediction,
        cgpa,
        coding_skills,
        internships,
        certifications
    ):


        if prediction==0:

            return 0



        score = (

            cgpa*0.3 +

            coding_skills*0.3 +

            internships +

            certifications

        )



        return score*100000




    def get_improvement_suggestions(
        self,
        input_data,
        prediction
    ):


        if prediction==1:


            return [
                {
                "priority":"Info",
                "suggestion":"Great profile keep improving",
                "impact":"Positive"
                }
            ]



        return [

            {

            "priority":"High",

            "suggestion":"Improve CGPA, coding skills and projects",

            "impact":"High"

            }

        ]




# ==========================
# GLOBAL OBJECT
# ==========================


placement_model = PlacementModel()
