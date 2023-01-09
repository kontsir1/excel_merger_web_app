import streamlit as st
import pandas as pd

def merge_dataframes(df1, df2, common_column):
    # Merge the two dataframes on the specified common column
    df_merged = pd.merge(df1, df2, on=common_column, how='outer')
    
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
     # Get the common column name from the user
    common_column = st.sidebar.selectbox("Select common column", df1.columns)
    
    # Merge the dataframes on the selected common column
    df_merged = merge_dataframes(df1, df2, common_column)
    
    # Display the merged dataframe
    st.markdown("## Merged dataframe")
    st.write(df_merged)
