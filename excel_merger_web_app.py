import streamlit as st
import pandas as pd

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
    # Find common columns between the two dataframes
    common_columns = list(set(df1.columns) & set(df2.columns))

    # If there are common columns, merge on those columns
    if common_columns:
        merged_df = pd.merge(df1, df2, on=common_columns)
    else:
        # If there are no common columns, display all the columns and ask the user on which column to perform the merge
        all_columns = list(set(df1.columns) | set(df2.columns))
        st.write("No common columns between the two dataframes.")
        st.write("The available columns are:", all_columns)
        merge_column = st.selectbox("Select the column on which to perform the merge:", all_columns)
        merged_df = pd.merge(df1, df2, on=merge_column)

    # Display the merged dataframe
    st.write(merged_df)
