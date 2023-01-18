import streamlit as st
import pandas as pd
import base64
import openpyxl
from io import BytesIO


st.set_page_config(page_title="Merge CSV and Excel Files", page_icon=":guardsman:", layout="wide")

st.title("Merge CSV and Excel Files")
st.write("This app allows you to upload two CSV or Excel files and merge them on a common column.")
st.write("You can also select which columns of the merged dataframe should be exported.")
st.write("The resulting dataframe is exported to a CSV and an XLSX file and allow the user to download these files.")

def read_csv(file):
    df = pd.DataFrame()
    chunksize = 50  # set the chunksize to 50 rows
    try:
        for chunk in pd.read_csv(file, chunksize=chunksize):
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
    selected_columns = st.multiselect("Select columns to export", df1.columns.tolist())
    if set(selected_columns[0]).intersection(set(selected_columns[1])) != set(selected_columns[0]):
        st.warning("Error: Could not merge dataframes. Make sure the selected columns are the same in both dataframes.")
    else:
        try:
            df_merged = pd.merge(df1, df2, left_on=common_column1, right_on=common_column2, how='inner')
        except ValueError:
            st.warning("Error: Could not merge dataframes. Make sure the selected common columns exist and have the same data type in both dataframes.")
    return df_merged

def export_csv(df, selected_columns):
    """Export selected columns of dataframe as CSV"""
    if df is not None:
        if len(selected_columns) > 1:
            if set(selected_columns[0]).intersection(set(selected_columns[1])) != set(selected_columns[0]):
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
            if set(selected_columns[0]).intersection(set(selected_columns[1])) != set(selected_columns[0]):
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
    file_one = st.sidebar.file_uploader("Upload first file (csv, xlsx)", type=["csv", "xlsx"])    
    file_two = st.sidebar.file_uploader("Upload second file (csv, xlsx)", type=["csv", "xlsx"])

    if file_one and file_two:
        df1, df2, file_one_name, file_two_name = read_files(file_one,file_two)
        if df1 is not None and df2 is not None:
            common_column1 = st.selectbox("Select common column in first file", df1.columns.tolist())
            common_column2 = st.selectbox("Select common column in second file", df2.columns.tolist())
            selected_columns = st.multiselect("Select columns to export", df1.columns.tolist())
            df_merged = merge_dataframes(df1, df2, common_column1, common_column2, selected_columns)
            if df_merged is not None:
                st.write("Preview of the merged dataframe:")
                st.dataframe(df_merged)

                selected_columns = st.multiselect("Select columns to export", df_merged.columns.tolist())
                if set(selected_columns[0]).intersection(set(selected_columns[1])) != set(selected_columns[0]):
                    st.warning("Error: Could not export dataframes. Make sure the selected columns are the same in both dataframes.")
                else:
                    export_csv(df_merged, selected_columns)
                    export_xlsx(df_merged, selected_columns)


if __name__ == "__main__":
    main()
