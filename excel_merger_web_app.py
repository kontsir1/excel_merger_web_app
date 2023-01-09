import io

file1 = st.file_uploader('Select the first file')
file2 = st.file_uploader('Select the second file')

if file1 is not None and file2 is not None:
    file1.seek(0)
    df1 = pd.read_csv(io.StringIO(file1.read()))
    file2.seek(0)
    df2 = pd.read_csv(io.StringIO(file2.read()))
    st.dataframe(df1)
    st.dataframe(df2)

    
if st.button('Merge files'):
    merged_df = pd.merge(df1, df2)
    st.dataframe(merged_df)
