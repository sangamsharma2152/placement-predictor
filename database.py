"""
Database operations for Placement Predictor
"""

import sqlite3
import pandas as pd
from datetime import datetime
from config import DATABASE_PATH
import json

class Database:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Predictions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                name TEXT,
                email TEXT,
                branch TEXT,
                cgpa REAL,
                internships INTEGER,
                projects INTEGER,
                coding_skills INTEGER,
                communication_skills INTEGER,
                aptitude_score REAL,
                certifications INTEGER,
                backlogs INTEGER,
                prediction INTEGER,
                confidence REAL,
                predicted_salary TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        
        # Goals Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                goal_type TEXT,
                target_value REAL,
                current_value REAL,
                progress REAL,
                status TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME,
                FOREIGN KEY(student_id) REFERENCES predictions(student_id)
            )
        ''')
        
        # Feedback Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                rating INTEGER,
                comment TEXT,
                prediction_accuracy TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Achievements Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                achievement_name TEXT,
                description TEXT,
                icon TEXT,
                unlocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(student_id) REFERENCES predictions(student_id)
            )
        ''')
        
        # Statistics Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                category TEXT,
                date_recorded DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_prediction(self, data):
        """Save prediction to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO predictions 
                (student_id, name, email, branch, cgpa, internships, projects,
                 coding_skills, communication_skills, aptitude_score, 
                 certifications, backlogs, prediction, confidence, predicted_salary, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('student_id'),
                data.get('name'),
                data.get('email'),
                data.get('branch'),
                data.get('cgpa'),
                data.get('internships'),
                data.get('projects'),
                data.get('coding_skills'),
                data.get('communication_skills'),
                data.get('aptitude_score'),
                data.get('certifications'),
                data.get('backlogs'),
                data.get('prediction'),
                data.get('confidence'),
                data.get('predicted_salary'),
                data.get('notes')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_predictions(self):
        """Retrieve all predictions"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM predictions", conn)
        conn.close()
        return df
    
    def get_prediction(self, student_id):
        """Get specific prediction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_prediction_history(self, student_id):
        """Get prediction history for a student"""
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM predictions WHERE student_id = ? ORDER BY timestamp DESC",
            conn,
            params=(student_id,)
        )
        conn.close()
        return df
    
    def save_goal(self, student_id, goal_type, target_value, current_value=0):
        """Save a goal for student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        progress = (current_value / target_value * 100) if target_value > 0 else 0
        
        cursor.execute('''
            INSERT INTO goals (student_id, goal_type, target_value, current_value, progress, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (student_id, goal_type, target_value, current_value, progress, 'In Progress'))
        conn.commit()
        conn.close()
    
    def get_goals(self, student_id):
        """Get goals for a student"""
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM goals WHERE student_id = ?",
            conn,
            params=(student_id,)
        )
        conn.close()
        return df
    
    def update_goal_progress(self, goal_id, current_value):
        """Update goal progress"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT target_value FROM goals WHERE id = ?", (goal_id,))
        result = cursor.fetchone()
        
        if result:
            target_value = result[0]
            progress = (current_value / target_value * 100) if target_value > 0 else 0
            status = 'Completed' if progress >= 100 else 'In Progress'
            
            cursor.execute('''
                UPDATE goals 
                SET current_value = ?, progress = ?, status = ?, updated_at = ?
                WHERE id = ?
            ''', (current_value, progress, status, datetime.now(), goal_id))
            conn.commit()
        
        conn.close()
    
    def save_feedback(self, student_id, rating, comment, prediction_accuracy):
        """Save feedback"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (student_id, rating, comment, prediction_accuracy)
            VALUES (?, ?, ?, ?)
        ''', (student_id, rating, comment, prediction_accuracy))
        conn.commit()
        conn.close()
    
    def get_feedback(self):
        """Get all feedback"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        return df
    
    def unlock_achievement(self, student_id, achievement_name, description, icon):
        """Unlock an achievement for student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO achievements (student_id, achievement_name, description, icon)
            VALUES (?, ?, ?, ?)
        ''', (student_id, achievement_name, description, icon))
        conn.commit()
        conn.close()
    
    def get_achievements(self, student_id):
        """Get achievements for a student"""
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM achievements WHERE student_id = ?",
            conn,
            params=(student_id,)
        )
        conn.close()
        return df
    
    def get_statistics(self):
        """Get all statistics"""
        conn = self.get_connection()
        df = pd.read_sql_query("SELECT * FROM statistics", conn)
        conn.close()
        return df
    
    def delete_prediction(self, student_id):
        """Delete a prediction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE student_id = ?", (student_id,))
        conn.commit()
        conn.close()
    
    def search_predictions(self, query):
        """Search predictions by name or email"""
        conn = self.get_connection()
        df = pd.read_sql_query(
            "SELECT * FROM predictions WHERE name LIKE ? OR email LIKE ?",
            conn,
            params=(f"%{query}%", f"%{query}%")
        )
        conn.close()
        return df

# Global database instance
db = Database()
