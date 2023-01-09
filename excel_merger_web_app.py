import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

import io
import base64

def merge_files(file1, file2):
    # Check if file1 or file2 is None
    if file1 is None or file2 is None:
        st.error("Please upload both files before merging.")
        return

    # Check if file1 is a CSV file
    if file1.name.endswith(".csv"):
        # Get file1 as a file-like object
        file1_like = io.BytesIO(file1.get_bytestream())
        df1 = pd.read_csv(file1_like)
    # Check if file1 is an Excel file
    elif file1.name.endswith(".xlsx"):
        # Get file1 as a file-like object
        file1_like = io.BytesIO(file1.get_bytestream())
        df1 = pd.read_excel(file1_like)
    else:
        st.error("Unsupported file type for file1. Please upload a CSV or Excel file.")
        return

    # Check if file2 is a CSV file
    if file2.name.endswith(".csv"):
        # Get file2 as a file-like object
        file2_like = io.BytesIO(file2.get_bytestream())
        df2 = pd.read_csv(file2_like)
    # Check if file2 is an Excel file
    elif file2.name.endswith(".xlsx"):
        # Get file2 as a file-like object
        file2_like = io.BytesIO(file2.get_bytestream())
        df2 = pd.read_excel(file2_like)
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
