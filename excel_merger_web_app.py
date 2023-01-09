import streamlit as st
import pandas as pd

def merge_dataframes(df1, df2):
    # Merge the two dataframes
    df_merged = pd.merge(df1, df2, how='inner')
    
    return df_merged


st.sidebar.markdown("# Select two files")

# Use the file uploader to select the first file
file_one = st.sidebar.file_uploader("Upload first file")

# Use the file uploader to select the second file
file_two = st.sidebar.file_uploader("Upload second file")

# Check if both files are uploaded
if file_one and file_two:
    # Read both files as pandas dataframes
    df1 = pd.read_csv(file_one)
    df2 = pd.read_csv(file_two)

    # Display the two dataframes side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## First file")
        st.write(df1)
    with col2:
        st.markdown("## Second file")
        st.write(df2)
    ###### ABOVE THIS DO NOT DELETE #######
    # Merge the dataframes
    df_merged = merge_dataframes(df1, df2)
    
    # Display the merged dataframe
    st.markdown("## Merged dataframe")
    st.write(df_merged)
