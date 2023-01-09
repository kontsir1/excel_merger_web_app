import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

def merge_files(files, column, selected_columns):
    # Initialize an empty list to store the dataframes
    dataframes = []
    
    # Iterate through the list of files
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
        
        # Append the dataframe to the list
        dataframes.append(df)
    
    # Merge the dataframes using pd.concat
    merged = pd.concat(dataframes, axis=0, ignore_index=True)
    
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
        href = f'<a href="data:file/csv;base64,{b64}" download "merged_file.csv">Download CSV File</a>'
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

# Allow the user to select multiple files
file1 = st.sidebar.file_uploader("Upload first file")
file2 = st.sidebar.file_uploader("Upload second file")
file3 = st.sidebar.file_uploader("Upload third file")
# ... and so on

# Store the files in a list
files = [file1, file2, file3]

# Remove any None elements from the list
files = [f for f in files if f is not None]

# Get list of column names from the first file
column_options = list(pd.read_csv(files[0]).columns)

# Allow user to select column
column = st.sidebar.selectbox("Select column to merge on", column_options)

select_columns = st.sidebar.checkbox("Select specific columns to include in merged file")

if select_
    merged = merge_files(files, column, selected_columns)
    st.dataframe(merged)

if st.sidebar.button("Download merged file"):
    format = st.sidebar.radio("Select format", ["CSV", "XLSX"])
    download_file(merged, format)


