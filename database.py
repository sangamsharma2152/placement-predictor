"""
Database Manager
"""

import sqlite3
import pandas as pd
from datetime import datetime


class Database:


    def __init__(self):

        self.db_name = "placement.db"

        self.create_table()



    def connect(self):

        return sqlite3.connect(
            self.db_name,
            check_same_thread=False
        )



    def create_table(self):

        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
        """

        CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id TEXT,

        name TEXT,

        email TEXT,

        branch TEXT,

        cgpa REAL,

        internships INTEGER,

        projects INTEGER,

        coding_skills INTEGER,

        communication_skills INTEGER,

        aptitude_score INTEGER,

        certifications INTEGER,

        backlogs INTEGER,

        prediction INTEGER,

        confidence REAL,

        predicted_salary REAL,

        created_at TEXT

        )

        """

        )


        conn.commit()

        conn.close()




    def save_prediction(
        self,
        data
    ):


        conn = self.connect()

        cursor = conn.cursor()


        cursor.execute(
        """

        INSERT INTO predictions(

        student_id,
        name,
        email,
        branch,
        cgpa,
        internships,
        projects,
        coding_skills,
        communication_skills,
        aptitude_score,
        certifications,
        backlogs,
        prediction,
        confidence,
        predicted_salary,
        created_at

        )

        VALUES(
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )

        """,

        (

        data.get("student_id"),

        data.get("name"),

        data.get("email"),

        data.get("branch"),

        data.get("cgpa"),

        data.get("internships"),

        data.get("projects"),

        data.get("coding_skills"),

        data.get("communication_skills"),

        data.get("aptitude_score"),

        data.get("certifications"),

        data.get("backlogs"),

        int(data.get("prediction")),

        float(data.get("confidence")),

        float(data.get("predicted_salary",0)),

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        )

        )


        conn.commit()

        conn.close()




    def get_all_predictions(self):


        conn=self.connect()


        try:

            df=pd.read_sql(

            "SELECT * FROM predictions",

            conn

            )


        except:


            df=pd.DataFrame()



        conn.close()


        return df




    def save_goal(
        self,
        *args,
        **kwargs
    ):

        pass



    def get_goals(
        self,
        *args,
        **kwargs
    ):

        return pd.DataFrame()



db = Database()
