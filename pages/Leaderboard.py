"""
Leaderboard Page
"""

import streamlit as st
import pandas as pd
from database import db

st.title("📋 Leaderboard & Rankings")

# Tabs for different rankings
tab1, tab2, tab3 = st.tabs(["🏆 Top CGPA", "⭐ Highest Confidence", "✅ Placed Students"])

with tab1:
    st.subheader("Top 10 Students by CGPA")
    all_preds = db.get_all_predictions()
    
    if len(all_preds) > 0:
        leaderboard = all_preds.sort_values('cgpa', ascending=False)[['name', 'cgpa', 'branch', 'prediction']].head(10)
        leaderboard['Rank'] = range(1, len(leaderboard) + 1)
        leaderboard['Status'] = leaderboard['prediction'].apply(lambda x: '✅ Placed' if x == 1 else '⏳ Pending')
        leaderboard = leaderboard[['Rank', 'name', 'branch', 'cgpa', 'Status']]
        
        # Display with colors
        st.dataframe(leaderboard, use_container_width=True)
        
        for idx, row in leaderboard.iterrows():
            medal = "🥇" if row['Rank'] == 1 else "🥈" if row['Rank'] == 2 else "🥉" if row['Rank'] == 3 else f"{row['Rank']}."
            st.write(f"{medal} **{row['name']}** - CGPA: {row['cgpa']:.2f} ({row['branch']}) {row['Status']}")
    else:
        st.info("No predictions yet!")

with tab2:
    st.subheader("Top 10 Predictions by Confidence")
    all_preds = db.get_all_predictions()
    
    if len(all_preds) > 0:
        confidence_board = all_preds.sort_values('confidence', ascending=False)[['name', 'confidence', 'prediction', 'cgpa']].head(10)
        confidence_board['Rank'] = range(1, len(confidence_board) + 1)
        confidence_board['Result'] = confidence_board['prediction'].apply(lambda x: '✅ Placed' if x == 1 else '❌ Not Placed')
        confidence_board = confidence_board[['Rank', 'name', 'cgpa', 'confidence', 'Result']]
        
        st.dataframe(confidence_board, use_container_width=True)

with tab3:
    st.subheader("Successfully Placed Students")
    all_preds = db.get_all_predictions()
    
    if len(all_preds) > 0:
        placed = all_preds[all_preds['prediction'] == 1].sort_values('confidence', ascending=False)
        
        if len(placed) > 0:
            st.metric("Total Placed", len(placed))
            st.dataframe(placed[['name', 'branch', 'cgpa', 'predicted_salary']], use_container_width=True)
        else:
            st.info("No placed students yet!")
