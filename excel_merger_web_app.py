import streamlit as str
import pandas as pd

str.sidebar.markdown("# Select two files")

# Use the file uploader to select the first file
file_one = str.sidebar.file_uploader("Upload first file")

# Use the file uploader to select the second file
file_two = str.sidebar.file_uploader("Upload second file")

# Check if both files are uploaded
if file_one and file_two:
    # Read both files as pandas dataframes
    df1 = pd.read_csv(file_one)
    df2 = pd.read_csv(file_two)

    # Display the two dataframes side by side
    col1, col2 = str.columns(2)
    str.markdown("## First file")
    with col1:
        str.write(df1)
    str.markdown("## Second file")
    with col2:
        str.write(df2)
