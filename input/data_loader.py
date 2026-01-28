# input/data_loader.py

import pandas as pd
import streamlit as st

def load_tabular_file(uploaded_file):
    """
    Load CSV or Excel file into a pandas DataFrame
    """
    if uploaded_file is None:
        return None,None
    
    file_name = uploaded_file.name.lower()
    
    try:
        if file_name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_name}")
            return None
        
        return df,file_name.split('.')[0]
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None,file_name
