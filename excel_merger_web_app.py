import streamlit as st
import pandas as pd

def merge_excel_files(excel_files, merge_column):
    # create an empty dataframe to store the final merged file
    merged_df = pd.DataFrame()

    # loop through each excel file and add it to the merged dataframe
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            merged_df = pd.merge(merged_df, df, on=merge_column, how="outer")
        except Exception as e:
            st.write("Error: Invalid file selected")
            st.write(e)

    return merged_df

# add a file uploader for the user to select the excel files they want to merge
excel_files = st.file_uploader("Select excel files to merge", type=["xlsx", "csv"])

# display the header of each imported file
if excel_files:
    for file in excel_files:
        try:
            df = pd.read_excel(file)
            st.write(df.head())
        except Exception as e:
            st.write("Error: Invalid file selected")
            st.write(e)

# add a dropdown menu for the user to select the column on which to merge the excel files
if excel_files:
    merge_column = st.selectbox("Select column to merge on", df.columns)
else:
    st.write("Error: No files selected")

# add a validation check to ensure that the user selects at least two excel files to merge
if excel_files and len(excel_files) < 2:
    st.write("Error: Please select at least two excel files to merge")
else:
    # add a validation check to ensure that the selected merge column is present in all of the excel files
    valid_merge_column = True
    for file in excel_files:
        df = pd.read_excel(file)
        if merge_column not in df.columns:
            valid_merge_column = False
            st.write("Error: Selected merge column is not present in all of the excel files")

        # add a check to ensure that the selected merge column has the same data type in all of the files
        if df[merge_column].dtype != merged_df[merge_column].dtype:
            valid_merge_column = False
            st.write("Error: Selected merge column has different data types in the different files")

    # call the merge_excel_files function and pass in the excel files and the selected merge column as arguments
    if valid_merge_column:
        # create a progress bar to show the progress of the file merge process
        progress_bar = st.progress(0)
        max_steps = len(excel_files)
        step = 0

        try:
            merged_df = merge_excel_files(excel_files, merge_column)

            # update the progress bar
            step += 1
            progress_bar.progress(step/max_steps)
        except Exception as e:
            st.write("Error: Invalid merge column selected")
            st.write(e)

        # display the finalised file
        st.dataframe(merged_df)

        # add a multi-select box for the user to select the columns they want to include in the merged file
        selected_columns = st.multiselect("Select columns to include in merged file", merged_df.columns)

        # create a new dataframe with only the selected columns
        filtered_df = merged_df[selected_columns]

# add a download button for the user to download the merged file in either xlsx or csv format
if st.button("Download file"):
    file_format = st.selectbox("Select file format", ["xlsx", "csv"])
    if file_format == "xlsx":
        # convert the dataframe to an excel file
        merged_excel = pd.ExcelWriter("merged_file.xlsx", engine="xlsxwriter")
        filtered_df.to_excel(merged_excel, index=False)
        merged_excel.save()

        # download the excel file
        st.download("merged_file.xlsx")
    elif file_format == "csv":
        # convert the dataframe to a csv file
        filtered_df.to_csv("merged_file.csv", index=False)

        # download the csv file
        st.download("merged_file.csv")

