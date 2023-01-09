import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

def merge_files(file1, file2, column, selected_columns):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    merged = pd.merge(df1, df2, on=column)
    if selected_columns:
        merged = merged[selected_columns]
    return merged

def select_columns(dataframe):
    all_columns = list(dataframe.columns)
    selected_columns = st.multiselect("Select columns to include in merged file", all_columns)
    return selected_columns

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

file1 = st.file_uploader("Upload first file")
file2 = st.file_uploader("Upload second file")
columns = st.multiselect("Select column to merge on", merged.columns)

if st.button("Merge files"):
    merged = merge_files(file1, file2, columns)
    st.dataframe(merged)
    select_columns = st.checkbox("Select specific columns to include in merged file")
    if select_columns:
        selected_columns = select_columns(merged)
    else:
        selected_columns = None

if st.button("Download merged file"):
    format = st.radio("Select format", ["CSV", "XLSX"])
    download_file(merged, format)

