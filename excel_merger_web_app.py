import streamlit as st
import pandas as pd

df = pd.read_csv("dir/file.csv")

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


csv = convert_df(df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)
