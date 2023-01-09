import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

def merge_files(file1, file2):
    # Check if file1 is a CSV file
    if file1.filename.endswith(".csv"):
        df1 = pd.read_csv(file1)
    # Check if file1 is an Excel file
    elif file1.filename.endswith(".xlsx"):
        df1 = pd.read_excel(file1)
    else:
        st.error("Unsupported file type for file1. Please upload a CSV or Excel file.")
        return

    # Check if file2 is a CSV file
    if file2.filename.endswith(".csv"):
        df2 = pd.read_csv(file2)
    # Check if file2 is an Excel file
    elif file2.filename.endswith(".xlsx"):
        df2 = pd.read_excel(file2)
    else:
        st.error("Unsupported file type for file2. Please upload a CSV or Excel file.")
        return

    merged = pd.merge(df1, df2, how='inner')
    
    return merged


def download_file(data, file_format):
    if file_format == "CSV":
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
    elif file_format == "XLSX":
        xlsx = openpyxl.Workbook()
        sheet = xlsx.active
        for r in dataframe_to_rows(data, index=False, header=True):
            sheet.append(r)
        xlsx.save("merged_file.xlsx")
        st.markdown(
            f'<a href="/downloads/merged_file.xlsx" download>Download XLSX File</a>',
            unsafe_allow_html=True,
        )

st.title("File Merger")

file1 = st.sidebar.file_uploader("Upload first file")
file2 = st.sidebar.file_uploader("Upload second file")



if st.sidebar.button("Merge files"):
    merged = merge_files(file1, file2)
    st.dataframe(merged)

if st.sidebar.button("Download merged file"):
    format = st.sidebar.radio("Select format", ["CSV", "XLSX"])
    download_file(merged, format)
