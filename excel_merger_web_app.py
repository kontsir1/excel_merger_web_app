import streamlit as st
import pandas as pd
from openpyxl import load_workbook

uploaded_file1 = st.file_uploader("Choose the first file to merge:", type=["xls", "xlsx", "csv"])
uploaded_file2 = st.file_uploader("Choose the second file to merge:", type=["xls", "xlsx", "csv"])
column_name = st.selectbox("Select the column to merge on:", df.columns)
selected_columns = st.multiselect("Select the columns to export:", df.columns)

if st.button("Merge files"):
    df1 = pd.read_excel(uploaded_file1)
    df2 = pd.read_excel(uploaded_file2)
    merged_df = pd.merge(df1, df2, on=column_name)
    merged_df = merged_df[selected_columns]
    if st.button("Download merged file"):
        st.markdown("File is being downloaded...")
        merged_df.to_excel("merged_file.xlsx", index=False)
        st.markdown("File downloaded!")
    st.dataframe(merged_df.head(20))
