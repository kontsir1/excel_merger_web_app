import streamlit as str
import pandas as pd

st.sidebar.markdown("# Select two files")

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
    str.markdown("## First file")
    with str.column("one-half"):
        str.write(df1)
    st.markdown("## Second file")
    with str.column("one-half"):
        str.write(df2)
