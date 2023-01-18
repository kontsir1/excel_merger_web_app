import streamlit as st
import pandas as pd
import base64
import openpyxl
import re
from io import BytesIO


st.set_page_config(page_title="Merge CSV and Excel Files", page_icon=":guardsman:", layout="wide")

st.title("Merge CSV and Excel Files")
st.write("This app allows you to upload two CSV or Excel files and merge them on a common column.")
st.write("You can also select which columns of the merged dataframe should be exported.")
st.write("The resulting dataframe is exported to a CSV and an XLSX file and allow the user to download these files.")

file_one = st.sidebar.file_uploader("Upload first file (csv, xlsx)", type=["csv", "xlsx"])    
file_two = st.sidebar.file_uploader("Upload second file (csv, xlsx)", type=["csv", "xlsx"])

def read_csv(file):
    df = pd.DataFrame()
    chunksize = 50  # set the chunksize to 50 rows
    try:
        with open(file, 'r') as f:
            data = f.read()
        header_match = re.search(r'^(Segments.*)', data, re.MULTILINE)
        header = header_match.group(1)
        data = re.sub(r'^[#].*\n(?!'+header+')', '', data)
        data = re.sub(r'\n[#].*', '', data)
        data = re.sub(r'\n.*(D_Variants).*\n', '\n', data)

        for chunk in pd.read_csv(BytesIO(data.encode()), chunksize=chunksize):
            df = pd.concat([df, chunk])
    except:
        st.warning("An error occurred while processing the file. Make sure it is a valid CSV file.")
        df = None
    return df


def read_excel(file):
    try:
        df = pd.read_excel(file)
    except:
        st.warning("An error occurred while processing the file. Make sure it is a valid Excel file.")
        df = None
    return df

@st.cache
def read_files(file_one,file_two):
    """Read the first and second files as pandas dataframes"""
    if file_one and file_two:
        file_one_ext = file_one.name.split('.')[-1]
        file_two_ext = file_two.name.split('.')[-1]
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        if file_one_ext == 'csv':
            df1 = read_csv(file_one)
        else:
            df1 = read_excel(file_one)
        if file_two_ext == 'csv':
            df2 = read_csv(file_two)
        else:
            df2 = read_excel(file_two)
        return df1, df2, file_one.name, file_two.name
    else:
        return None, None, None, None

def merge_dataframes(df1, df2, common_column1, common_column2):
    df_merged = None
    try:
        df_merged = pd.merge(df1, df2, left_on=common_column1, right_on=common_column2, how='inner')
    except ValueError:
        st.warning("Error: Could not merge dataframes. Make sure the selected common columns exist and have the same data type in both dataframes.")
    return df_merged

def export_csv(df, selected_columns):
    """Export selected columns of dataframe as CSV"""
    if df is not None:
        if len(selected_columns) > 1:
            # check if the selected columns are the same
            if set(selected_columns[0]) != set(selected_columns[1]):
                st.warning("Error: Could not export dataframes. Make sure the selected columns are the same in both dataframes.")
            else:
                # Export as CSV
                csv = df[selected_columns].to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                csv_href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV</a>'
                st.sidebar.markdown(csv_href, unsafe_allow_html=True)

def export_xlsx(df, selected_columns):
    """Export selected columns of dataframe as XLSX"""
    if df is not None:
        if len(selected_columns) > 1:
            # check if the selected columns are the same
            if set(selected_columns[0]) != set(selected_columns[1]):
                st.warning("Error: Could not export dataframes. Make sure the selected columns are the same in both dataframes.")
            else:
                # Export as XLSX
                xlsx_file = BytesIO()
                df[selected_columns].to_excel(xlsx_file, index=False)
                xlsx_file.seek(0)
                xlsx_data = xlsx_file.read()
                xlsx_b64 = base64.b64encode(xlsx_data).decode()
                xlsx_href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{xlsx_b64}" download="merged_data.xlsx">Download XLSX</a>'
                st.sidebar.markdown(xlsx_href, unsafe_allow_html=True)
                     

def main():

    df1, df2, first_file_name, second_file_name = read_files(file_one,file_two)

    if df1 is not None:
        # Display the dataframes
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{first_file_name}")
            st.write(df1)
        with col2:
            st.subheader(f"{second_file_name}")
            st.write(df2)

        # Merge dataframes and select common columns
        common_column1 = st.sidebar.selectbox("Select common column for first file", df1.columns)
        common_column2 = st.sidebar.selectbox("Select common column for second file", df2.columns)

        # Select columns to export
        df_merged = merge_dataframes(df1, df2, common_column1, common_column2)
        if df_merged is not None:
            selected_columns = st.sidebar.multiselect("Select columns to export", df_merged.columns)
        
        # Display merged dataframe
        st.subheader("Merged dataframe")
        st.write(df_merged)

        # Export dataframe as CSV or XLSX
        if df_merged is not None:
            export_csv(df_merged, selected_columns)
            export_xlsx(df_merged, selected_columns)


if __name__ == "__main__":
    main()
