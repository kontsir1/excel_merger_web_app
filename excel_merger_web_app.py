import io

def merge_files(file1, file2):
    # Check if file1 or file2 is None
    if file1 is None or file2 is None:
        st.error("Please upload both files before merging.")
        return

    # Check if file1 is a CSV file
    if file1.name.endswith(".csv"):
        # Get file1 as a file-like object
        file1_like = io.BytesIO(file1.get_bytestream())
        df1 = pd.read_csv(file1_like)
    # Check if file1 is an Excel file
    elif file1.name.endswith(".xlsx"):
        # Get file1 as a file-like object
        file1_like = io.BytesIO(file1.get_bytestream())
        df1 = pd.read_excel(file1_like)
    else:
        st.error("Unsupported file type for file1. Please upload a CSV or Excel file.")
        return

    # Check if file2 is a CSV file
    if file2.name.endswith(".csv"):
        # Get file2 as a file-like object
        file2_like = io.BytesIO(file2.get_bytestream())
        df2 = pd.read_csv(file2_like)
    # Check if file2 is an Excel file
    elif file2.name.endswith(".xlsx"):
        # Get file2 as a file-like object
        file2_like = io.BytesIO(file2.get_bytestream())
        df2 = pd.read_excel(file2_like)
    else:
        st.error("Unsupported file type for file2. Please upload a CSV or Excel file.")
        return

    merged = pd.merge(df1, df2, how='inner')
    return merged
