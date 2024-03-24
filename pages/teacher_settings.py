import streamlit as st
from src.login import login



if login("root"):
    st.header("Teacher Settings", divider="rainbow")
    if st.button("Settings"):
        st.write("does nothing")
