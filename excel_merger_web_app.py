import streamlit as st
import pandas as pd

st.sidebar.markdown("# Select files")

# Use the file uploader to select multiple files
files = st.sidebar.file_uploader("Upload files", type=["csv", "xlsx"], accept_multiple_files=True)

# Check if any files are uploaded
if files:
    # Read the files as pandas dataframes
    dfs = [pd.read_csv(f) if f.endswith(".csv") else pd.read_excel(f) for f in files]

    # Display the dataframes side by side
    for i, df in enumerate(dfs):
        st.markdown(f"## File {i+1}")
        st.write(df)
