import streamlit as st
import pandas as pd

# Allow users to upload two files
file1 = st.file_uploader('Select the first file')
file2 = st.file_uploader('Select the second file')

# If both files are uploaded, display them and create a button to merge them
if file1 is not None and file2 is not None:
    # Read the files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Display the DataFrames
    st.dataframe(df1)
    st.dataframe(df2)

    # Create a button to merge the DataFrames
    if st.button('Merge files'):
        merged_df = pd.merge(df1, df2)
        st.dataframe(merged_df)

        # Create a button to download the merged DataFrame
        st.download_button('Download merged file', 'merged.csv', merged_df.to_csv())
