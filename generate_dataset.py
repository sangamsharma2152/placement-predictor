"""
Generate 45,000 synthetic student records for training
"""
import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
num_records = 45000

# Generate data
data = {
    'Student_ID': range(1, num_records + 1),
    'Age': np.random.randint(20, 26, num_records),
    'Gender': np.random.choice(['M', 'F'], num_records, p=[0.55, 0.45]),
    'Degree': np.random.choice(['B.Tech', 'B.Sc', 'M.Tech'], num_records, p=[0.70, 0.20, 0.10]),
    'Branch': np.random.choice(['CSE', 'ECE', 'ME', 'EE', 'Civil', 'IT'], num_records, p=[0.30, 0.20, 0.15, 0.15, 0.12, 0.08]),
    'CGPA': np.random.normal(7.5, 1.2, num_records).clip(3.0, 10.0),
    'Internships': np.random.randint(0, 6, num_records),
    'Projects': np.random.randint(0, 8, num_records),
    'Coding_Skills': np.random.randint(2, 11, num_records),
    'Communication_Skills': np.random.randint(2, 11, num_records),
    'Aptitude_Test_Score': np.random.randint(30, 100, num_records),
    'Certifications': np.random.randint(0, 6, num_records),
    'Backlogs': np.random.randint(0, 4, num_records),
}

# Placement Status - higher scores = more likely to be placed
df_temp = pd.DataFrame(data)
placement_likelihood = (
    (df_temp['CGPA'] / 10) * 0.25 +
    (df_temp['Internships'] / 5) * 0.15 +
    (df_temp['Projects'] / 7) * 0.15 +
    (df_temp['Coding_Skills'] / 10) * 0.20 +
    (df_temp['Communication_Skills'] / 10) * 0.15 +
    (df_temp['Aptitude_Test_Score'] / 100) * 0.10
) - (df_temp['Backlogs'] * 0.05)

placement_likelihood = placement_likelihood.clip(0, 1)
data['Placement_Status'] = (np.random.random(num_records) < placement_likelihood).astype(int)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('train.csv', index=False)
print(f"✅ Generated {num_records:,} student records")
print(f"✅ Saved to: train.csv")
print(f"\nDataset Statistics:")
print(f"  - Total Students: {len(df):,}")
print(f"  - Placed: {df['Placement_Status'].sum():,} ({df['Placement_Status'].mean()*100:.1f}%)")
print(f"  - Not Placed: {(1-df['Placement_Status']).sum():,} ({(1-df['Placement_Status'].mean())*100:.1f}%)")
print(f"  - Average CGPA: {df['CGPA'].mean():.2f}")
print(f"  - Average Aptitude Score: {df['Aptitude_Test_Score'].mean():.1f}")
print(f"\nFirst 5 rows:")
print(df.head())
