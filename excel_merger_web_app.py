import streamlit as st
import pandas as pd
import openpyxl
import base64

from openpyxl.utils.dataframe import dataframe_to_rows

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
