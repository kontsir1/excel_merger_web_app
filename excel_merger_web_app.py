import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows


st.title("File Merger")

if file is not None:

    df= pd.read_csv(file)

    st.write(df)



#adding a file uploader to accept multiple CSV files

uploaded_files = st.file_uploader("Please choose a CSV file", accept_multiple_files=True)

for file in uploaded_files:

    bytes_data = file.read()

    st.write("File uploaded:", file.name)

    st.write(bytes_data)
