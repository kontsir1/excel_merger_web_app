import streamlit as st
import pandas as pd
import base64

def merge_dataframes(df1, df2, common_column1, common_column2):
    # Merge the two dataframes on the specified common columns
    try:
        df_merged = pd.merge(df1, df2, left_on=common_column1, right_on=common_column2, how='inner')
    except ValueError:
        st.error("Error: Could not merge dataframes. Make sure the selected common columns exist and have the same data type in both dataframes.")
        return
    
    # Drop one of the common columns
    df_merged.drop(common_column1, axis=1, inplace=True)
    
    return df_merged

# Use the file uploader to select the first file
file_one = st.sidebar.file_uploader("Upload first file")

# Use the file uploader to select the second file
file_two = st.sidebar.file_uploader("Upload second file")

# Check if both files are uploaded
if file_one and file_two:
    # Read both files as pandas dataframes
    df1 = pd.read_csv(file_one)
    df2 = pd.read_csv(file_two)
    # Check if either dataframe is empty
    if df1.empty or df2.empty:
        st.error("Error: One or both of the selected files are empty.")
        return
    
    # Display the two dataframes side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## First file")
        st.write(df1)
    with col2:
        st.markdown("## Second file")
        st.write(df2)
    
    # Get the common column names from the user
    common_column1 = st.sidebar.selectbox("Select common column for first file", df1.columns)
    common_column2 = st.sidebar.selectbox("Select common column for second file", df2.columns)
    
    # Check if either common column is not present in both dataframes
    if common_column1 not in df1.columns or common_column2 not in df2.columns:
        st.error("Error: One or both of the selected common columns are not present in both dataframes.")
        return
    
    # Merge the dataframes on the selected common columns
    df_merged = merge_dataframes(df1, df2, common_column1, common_column2)
    
    # Check if the merged dataframe is empty
    if df_merged.empty:
        st.error("Error: No common rows found between the two dataframes.")
        return
    
    # Display the merged dataframe
    st.markdown("## Merged dataframe")
    st.write(df_merged)
    
    # Add a download button to the sidebar
    st.sidebar.markdown("## Download merged dataframe")
    if st.sidebar.button("Download CSV"):
        st.markdown("Clicked download button")
        csv = df_merged.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
