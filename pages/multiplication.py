import streamlit as st
from src.login import login



def page():
    st.header(":blue[Math practice]", divider="rainbow")
    st.write("math is problem solving")



if login():
    page()
