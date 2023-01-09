import streamlit as st

st.title('Merge Excel Files')

st.write('Select the column to use as the key for merging:')
key_column = st.selectbox('Column:', ['A', 'B', 'C'])

st.write('Select the columns to export:')
columns_to_export = st.multiselect('Columns:', ['A', 'B', 'C'])

st.write('Select the input files:')
files = st.file_uploader('Files:', type=['xls', 'xlsx', 'csv'])

if files:
    # Merge the files using pandas
    df = pd.concat(map(pd.read_excel, files), ignore_index=True, sort=False)

    # Select the columns to export
    df = df[columns_to_export]

    # Display the first 20 rows
    st.dataframe(df.head(20))

    # Add a download button
    st.write('Click the button below to download the merged file:')
    file_format = st.selectbox('Format:', ['xls', 'xlsx', 'csv'])
    if st.button('Download'):
        if file_format == 'xls':
            with open('merged.xls', 'wb') as f:
                f.write(df.to_excel())
            st.success('File downloaded')
        elif file_format == 'xlsx':
            with open('merged.xlsx', 'wb') as f:
                f.write(df.to_excel())
            st.success('File downloaded')
        elif file_format == 'csv':
            with open('merged.csv', 'w') as f:
                f.write(df.to_csv())
            st.success('File downloaded')
