# Import necessary libraries
import streamlit as st
import pandas as pd

# Merge excel files
def merge_excel_files(file_list, merge_column):
    # Read in each file
    df_list = []
    for file in file_list:
        df = pd.read_excel(file)
        df_list.append(df)
    
    # Merge files on specified column
    merged_df = pd.concat(df_list, ignore_index=True, sort=False)
    
    # Return merged dataframe
    return merged_df

# Main function
def main():
    # Allow user to upload files
    uploaded_files = st.file_uploader("Upload excel files to merge", type=["xls", "xlsx", "csv"])
    
    if uploaded_files is not None:
        # Get list of columns to include in merged file
        all_columns = pd.read_excel(uploaded_files[0]).columns
        selected_columns = st.multiselect("Select columns to include in merged file", all_columns)
        
        # Merge files
        merged_df = merge_excel_files(uploaded_files, selected_columns)
        
        # Display merged data
        st.dataframe(merged_df)
        
        # Allow user to download merged file
        file_format = st.selectbox("Select file format for download", ["xls", "xlsx", "csv"])
        if file_format == "xls":
            st.write("Downloading xls file...")
            merged_df.to_excel("merged_file.xls")
            st.download("merged_file.xls")
        elif file_format == "xlsx":
            st.write("Downloading xlsx file...")
            merged_df.to_excel("merged_file.xlsx")
            st.download("merged_file.xlsx")
        elif file_format == "csv":
            st.write("Downloading csv file...")
            merged_df.to_csv("merged_file.csv")
            st.download("merged_file.csv")

# Run main function
if __name__ == '__main__':
    main()
