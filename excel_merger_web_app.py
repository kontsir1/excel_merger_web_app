import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

def merge_files(files):
    merged = None
    for file in files:
        # Check if file is a CSV file
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        # Check if file is an Excel file
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type. Please upload a CSV or Excel file.")
            return

        if merged is None:
            merged = df
        else:
            merged = pd.merge(merged, df, how='inner')
    
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

files = st.sidebar.file_uploader("Upload files to merge", type=["csv", "xlsx"], multiple=True)

if st.sidebar.button("Merge files"):
    merged = merge_files(files)
    st.dataframe(merged)

if st.sidebar.button("Download merged file"):
    format = st.sidebar.radio("Select format", ["CSV", "XLSX"])
    download_file(merged, format)
