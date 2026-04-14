"""
Batch Prediction Page
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from models import placement_model
from database import db

st.title("📈 Batch Predictions")

st.write("Upload a CSV file with multiple student records for batch predictions.")

uploaded_file = st.file_uploader("Choose CSV file", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.write("### Preview of uploaded data")
    st.dataframe(df.head(10))
    
    if st.button("🚀 Process Batch Predictions"):
        predictions = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, row in df.iterrows():
            try:
                row_dict = row.to_dict()
                pred, conf = placement_model.predict(row_dict)
                
                row_dict['Prediction'] = pred
                row_dict['Confidence'] = conf
                row_dict['Result'] = "Placed" if pred == 1 else "Not Placed"
                
                predictions.append(row_dict)
            except Exception as e:
                st.warning(f"Error processing row {idx + 1}: {e}")
            
            progress = (idx + 1) / len(df)
            progress_bar.progress(progress)
            status_text.text(f"Processing: {idx + 1}/{len(df)}")
        
        results_df = pd.DataFrame(predictions)
        
        st.success("✅ Batch processing completed!")
        
        st.subheader("Results Summary")
        col1, col2, col3 = st.columns(3)
        placed = len(results_df[results_df['Prediction'] == 1])
        col1.metric("Total Records", len(results_df))
        col2.metric("Placed", placed)
        col3.metric("Placement Rate", f"{placed/len(results_df)*100:.1f}%")
        
        st.subheader("Detailed Results")
        st.dataframe(results_df)
        
        # Export
        csv = results_df.to_csv(index=False)
        st.download_button(
            "📥 Download Results CSV",
            csv,
            f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv"
        )
