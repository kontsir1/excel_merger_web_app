# pip install openpyxl
import pandas as pd
import streamlit as st
import zipfile
import base64
import os

# Web App Title
st.markdown('''
# **Excel File Merger**

This is the **Excel File Merger App** created in Python using the Streamlit library.

**Credit:** App built in `Python` + `Streamlit` by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) (aka [Data Professor](http://youtube.com/dataprofessor))

---
''')

# Excel file merge function
def excel_file_merge(zip_file_name, column):
    df = pd.DataFrame()
    archive = zipfile.ZipFile(zip_file_name, 'r')
    with zipfile.ZipFile(zip_file_name, "r") as f:
        for file in f.namelist():
          xlfile = archive.open(file)
          if file.endswith('.xlsx'):
            # Add a note indicating the file name that this dataframe originates from
            df_xl = pd.read_excel(xlfile, engine='openpyxl')
            df_xl['Note'] = file
            # Appends content of each Excel file iteratively
            df = df.append(df_xl, ignore_index=True)
    # Merge the data based on the specified column
    merged_df = pd.merge(df, df_xl, on=column)
    return merged_df

# Upload CSV data
with st.sidebar.header('1. Upload your ZIP file'):
    uploaded_file = st.sidebar.file_uploader("Excel-containing ZIP file", type=["zip"])
    st.sidebar.markdown("""
[Example ZIP input file](https://github.com/dataprofessor/excel-file-merge-app/raw/main/nba_data.zip)
""")

# Main panel
if st.sidebar.button('Submit'):
    #@st.cache
    df = excel_file_merge(uploaded_file)
    
    # Select column for merge
    with st.sidebar.header('2. Select the column for merge'):
        column = st.sidebar.selectbox("Column", df.columns)
    
    df = excel_file_merge(uploaded_file, column)
    st.header('**Merged data**')
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)
    st.markdown(xldownload(df), unsafe_allow_html=True)
else:
    st.info('Awaiting for ZIP file to be uploaded.')
