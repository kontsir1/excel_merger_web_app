import streamlit as st
import pandas as pd
import base64
import openpyxl
from io import BytesIO


# Set theme colors
primary_color = "#2D72C5"
secondary_color = "#F3A623"
text_color = "#1B1B1B"
background_color = "#F7F7F7"

# Apply theme colors to the Streamlit theme
st.set_theme(
    theme_type="custom",
    primary_color=primary_color,
    secondary_color=secondary_color,
    text_color=text_color,
    background_color=background_color,
    primary_palette="Blues",
    secondary_palette="Oranges",
)



st.set_page_config(page_title="Merge CSV and Excel Files", page_icon=":guardsman:", layout="wide")

st.title("Merge CSV and Excel Files")
st.write("This app allows you to upload two CSV or Excel files and merge them on a common column.")
st.write("You can also select which columns of the merged dataframe should be exported.")
st.write("The resulting dataframe is exported to a CSV and an XLSX file and allow the user to download these files.")


def read_files():
    """Read the first and second files as pandas dataframes"""
    file_one = st.sidebar.file_uploader("Upload first file (csv, xlsx)", type=["csv", "xlsx"])    
    file_two = st.sidebar.file_uploader("Upload second file (csv, xlsx)", type=["csv", "xlsx"])
    if file_one and file_two:
        file_one_ext = file_one.name.split('.')[-1]
        file_two_ext = file_two.name.split('.')[-1]
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        if file_one_ext in ['csv', 'xlsx']:
            if file_one_ext == 'csv':
                chunksize = 500  # set the chunksize to 500 rows
                try:
                    for chunk in pd.read_csv(file_one, chunksize=chunksize):
                        df1 = pd.concat([df1, chunk])
                except:
                    st.warning("An error occurred while processing the first file. Make sure it is a valid CSV file.")
                    df1 = None
            else:
                try:
                    df1 = pd.read_excel(file_one)
                except:
                    st.warning("An error occurred while processing the first file. Make sure it is a valid Excel file.")
                    df1 = None
        
        if file_two_ext in ['csv', 'xlsx']:
            if file_two_ext == 'csv':
                chunksize = 500  # set the chunksize to 500 rows
                try:
                    for chunk in pd.read_csv(file_two, chunksize=chunksize):
                        df2 = pd.concat([df2, chunk])
                except:
                    st.warning("An error occurred while processing the second file. Make sure it is a valid CSV file.")
                    df2 = None
            else:
                try:
                    df2 = pd.read_excel(file_two)
                except:
                    st.warning("An error occurred while processing the second file. Make sure it is a valid Excel file.")
                    df2 = None
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

def export_dataframe(df, selected_columns):  
    if df is not None:
        """Export selected columns of dataframe as CSV and XLSX"""
        # Export as CSV
        csv = df[selected_columns].to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        csv_href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV</a>'
        st.sidebar.markdown(csv_href, unsafe_allow_html=True)

        # Export as XLSX
        xlsx_file = BytesIO()
        df[selected_columns].to_excel(xlsx_file, index=False)
        xlsx_file.seek(0)
        xlsx_b64 = base64.b64encode(xlsx_file.read()).decode()
        xlsx_href = f'<a href="data:file/xlsx;base64,{xlsx_b64}" download="merged_data.xlsx">Download XLSX</a>'
        st.sidebar.markdown(xlsx_href, unsafe_allow_html=True)
                     

def main():

    df1, df2, first_file_name, second_file_name = read_files()

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
        df_merged = merge_dataframes(df1, df2, common_column1, common_column2)

        # Display merged dataframe
        st.subheader("Merged dataframe")
        st.write(df_merged)

        # Select columns to export
        selected_columns = st.sidebar.multiselect("Select columns to export", df_merged.columns)

        # Export dataframe as CSV
        if st.sidebar.button("Download CSV"):
                if df_merged is not None:
                    export_dataframe(df_merged, selected_columns)
        if st.sidebar.button("Download Excel"):
            if df_merged is not None:
                    export_dataframe(df_merged, selected_columns)

if __name__ == "__main__":
    main()
