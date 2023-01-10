def read_files():
    """Read the first and second files as pandas dataframes"""
    file_one = st.file_uploader("Upload first file")
    file_two = st.file_uploader("Upload second file")
    if file_one and file_two:
        df1 = pd.read_csv(file_one)
        df2 = pd.read_csv(file_two)
        return df1, df2, file_one.name, file_two.name
    else:
        return None, None, None, None

def merge_dataframes(df1, df2, common_column1, common_column2):
    """Merge the two dataframes on the specified common columns"""
    df_merged = pd.merge(df1, df2, left_on=common_column1, right_on=common_column2)
    df_merged.drop(common_column1, axis=1, inplace=True)
    return df_merged

def delete_rows(df, start_row, end_row):
    """Delete specified rows from dataframe"""
    return df.drop(range(start_row, end_row+1))

def export_dataframe(df, selected_column):  
    """Export selected columns of dataframe as CSV"""
    csv = df[selected_columns].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
                     
def main():
    df1, df2, first_file_name, second_file_name = read_files()

    if df1 is not None:
        # Delete rows from first dataframe
        if st.checkbox("Delete rows from first dataframe"):
            start_row = st.number_input("Start row", max_value=df1.shape[0])
            end_row = st.number_input("End row", max_value=df1.shape[0])
            df1 = delete_rows(df1, start_row, end_row)

        # Delete rows from second dataframe
        if st.checkbox("Delete rows from second dataframe"):
            start_row = st.number_input("Start row", max_value=df2.shape[0])
            end_row = st.number_input("End row", max_value=df2.shape[0])
            df2 = delete_rows(df2, start_row, end_row)

        # Display the dataframes
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"## First file: {first_file_name}")
            st.write(df1)
        with col2:
            st.markdown(f"## Second file: {second_file_name}")
            st.write(df2)

        # Merge dataframes and select common columns
        common_column1 = st.selectbox("Select common column for first file", df1.columns)
        common_column2 = st.selectbox("Select common column for second file", df2.columns)
        df_merged = merge_dataframes(df1, df2, common_column1, common_column2)

        # Display merged dataframe
        st.markdown("## Merged dataframe")
        st.write(df_merged)

        # Select columns to export
        selected_columns = st.multiselect("Select columns to export", df_merged.columns)

        # Export dataframe as CSV
        if st.button("Download CSV"):
            export_dataframe(df_merged, selected_columns)

if __name__ == "__main__":
    main()
