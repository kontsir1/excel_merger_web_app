import streamlit as st
import pandas as pd
import base64
import openpyxl
from io import BytesIO

def merge_dataframes(df1, df2, common_column1, common_column2):
    # Merge the two dataframes on the specified common columns
    df_merged = pd.merge(df1, df2, left_on=common_column1, right_on=common_column2)
    
    # Drop one of the common columns
    df_merged.drop(common_column1, axis=1, inplace=True)
    
    return df_merged

def delete_rows(df, start_row, end_row):
    return df.drop(range(start_row, end_row+1))

# Set page layout to wide
st.set_page_config(layout="wide")

# Use the file uploader to select the first file
file_one = st.sidebar.file_uploader("Upload first file")

# Use the file uploader to select the second file
file_two = st.sidebar.file_uploader("Upload second file")

# Check if both files are uploaded
if file_one and file_two:
    # Read both files as pandas dataframes
    df1 = pd.read_csv(file_one, on_bad_lines='skip')
    df2 = pd.read_csv(file_two, on_bad_lines='skip')

    # Ask the user whether they want to delete rows from the first dataframe
    delete_rows_df1 = st.checkbox("Delete rows from first dataframe")
    if delete_rows_df1:
        # Get the index range of the rows to delete from the first dataframe
        start_row_df1 = st.number_input("Start row", max_value=df1.shape[0])
        end_row_df1 = st.number_input("End row", max_value=df1.shape[0])
        # Delete the specified range of rows from the first dataframe
        df1 = delete_rows(df1, start_row_df1, end_row_df1)

    # Ask the user whether they want to delete rows from the second dataframe
    delete_rows_df2 = st.checkbox("Delete rows from second dataframe")
    if delete_rows_df2:
        # Get the index range of the rows to delete from the second dataframe
        start_row_df2 = st.number_input("Start row", max_value=df2.shape[0])
        end_row_df2 = st.number_input("End row", max_value=df2.shape[0])
        # Delete the specified range of rows from the second dataframe
        df2 = delete_rows(df2, start_row_df2, end_row_df2)

    # Display the two dataframes side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## First file: " + file_one.name)
        file_size = file_one.getbuffer().nbytes / 1024 / 1024
        st.markdown(f"## First file: {file_one.name} | Size: {file_size:.2f}MB")
        st.write(df1)
    with col2:
        st.markdown(f"## Second file: {file_two.name}")
        file_size = file_two.getbuffer().nbytes / 1024 / 1024
        st.markdown(f"## Second file: {file_two.name} | Size: {file_size:.2f}MB")
        st.write(df2)
    
    # Get the common column names from the user
    common_column1 = st.sidebar.selectbox("Select common column for first file", df1.columns)
    common_column2 = st.sidebar.selectbox("Select common column for second file", df2.columns)
    
    # Merge the dataframes on the selected common columns
    df_merged = merge_dataframes(df1, df2, common_column1, common_column2)
    
    # Display the merged dataframe
    st.markdown("## Merged dataframe")
    st.write(df_merged)
    
    # Add a multi-select box to the sidebar to choose columns to export
    selected_columns = st.sidebar.multiselect("Select columns to export", df_merged.columns)

if st.sidebar.button("Download CSV"):
    st.markdown("Clicked download button")
    csv = df_merged[selected_columns].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.sidebar.button("Download Excel"):
    st.markdown("Clicked download button")
    excel_file = BytesIO()
    df_merged[selected_columns].to_excel(excel_file, index=False)
    excel_file.seek(0)
    b64 = base64.b64encode(excel_file.read()).decode()
    href = f'<a href="data:file/xlsx;base64,{b64}" download="merged_data.xlsx">Download Excel File</a>'
    st.markdown(href, unsafe_allow_html=True)
