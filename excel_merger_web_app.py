import streamlit as st
import pandas as pd

# Allow the user to upload multiple CSV or XLSX files
uploaded_files = st.sidebar.file_uploader("Select files to merge", type=["csv", "xlsx"], multiple=True)

# Create a submit button that the user can click to trigger the merge
if st.sidebar.button("Submit"):
    # Initialize an empty list to store the dataframes
    dataframes = []

    # Iterate over the uploaded files
    for file in uploaded_files:
        # Read the file into a dataframe
        df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)

        # Add the dataframe to the list
        dataframes.append(df)

    # Merge the dataframes on the selected column
    merge_column = st.sidebar.selectbox("Select the merge column", dataframes[0].columns)
    merged_data = pd.concat(dataframes, on=merge_column)

    # Display the merged data in the main panel of the UI
    st.write(merged_data)

# Create a download button that the user can click to download the merged data
if st.sidebar.button("Download"):
    # Determine the file format based on the file extension
    file_format = "csv" if st.sidebar.radio("Format", ["CSV", "XLSX"]) == "CSV" else "xlsx"

    # Create a temporary file to store the merged data
    with st.spinner("Saving file..."):
        temp_file = merged_data.to_csv() if file_format == "csv" else merged_data.to_excel()

    # Add the download link to the sidebar
    st.sidebar.markdown(f'<a href="temp_file" download>Download {file_format.upper()}</a>', unsafe_allow_html=True)
