"""
Notifications and Email functionality
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
import os


class EmailNotification:
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.sender_email = SENDER_EMAIL
        self.sender_password = SENDER_PASSWORD
    
    def send_prediction_email(self, recipient_email, student_name, prediction, confidence):
        """Send prediction result email"""
        if not self.sender_email or not self.sender_password:
            print("Email configuration not set. Skipping email notification.")
            return False
        
        try:
            subject = "🎓 Your Placement Prediction Result"
            
            body = f"""
            Dear {student_name},
            
            Your placement prediction has been completed!
            
            Prediction Result: {'✅ PLACED' if prediction == 1 else '❌ NOT PLACED'}
            Confidence Score: {confidence:.2f}%
            
            Log in to the Placement Predictor app to view detailed analysis and personalized suggestions.
            
            Best Regards,
            Placement Predictor Team
            """
            
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_achievement_email(self, recipient_email, student_name, achievement_name):
        """Send achievement unlock email"""
        if not self.sender_email or not self.sender_password:
            return False
        
        try:
            subject = f"🏆 Achievement Unlocked: {achievement_name}"
            
            body = f"""
            Dear {student_name},
            
            Congratulations! You have unlocked a new achievement:
            
            🏆 {achievement_name}
            
            Keep up the great work and continue improving your profile!
            
            Best Regards,
            Placement Predictor Team
            """
            
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_goal_reminder(self, recipient_email, student_name, goal_type, target):
        """Send goal reminder email"""
        if not self.sender_email or not self.sender_password:
            return False
        
        try:
            subject = f"📌 Goal Reminder: {goal_type}"
            
            body = f"""
            Dear {student_name},
            
            This is a reminder about your goal:
            
            Goal: {goal_type}
            Target: {target}
            
            Keep working towards your target to improve placement chances!
            
            Best Regards,
            Placement Predictor Team
            """
            
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


# Alert Templates
ALERT_TEMPLATES = {
    'low_cgpa': {
        'title': '⚠️ Low CGPA Alert',
        'message': 'Your CGPA is below the recommended threshold. Consider improving it.',
        'color': 'red'
    },
    'high_backlogs': {
        'title': '⚠️ High Backlogs Alert',
        'message': 'Clear your backlogs to improve placement chances.',
        'color': 'red'
    },
    'good_profile': {
        'title': '✅ Good Profile',
        'message': 'Your profile is looking good! Keep improving.',
        'color': 'green'
    },
    'placement_eligible': {
        'title': '🎉 Placement Eligible',
        'message': 'You are eligible for placements!',
        'color': 'green'
    },
    'improvement_needed': {
        'title': '💡 Improvement Needed',
        'message': 'Focus on the suggested areas to improve placement chances.',
        'color': 'orange'
    }
}
