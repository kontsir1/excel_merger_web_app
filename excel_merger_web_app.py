import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

def merge_files(file1, file2):
    print(f'file1: {file1}')
    print(f'file1.filename: {file1.filename}')
    # Check if file1 or file2 is None
    if file1 is None or file2 is None:
        st.error("Please upload both files before merging.")
        return


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
