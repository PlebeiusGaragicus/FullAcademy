import streamlit as st

from src.common import login_needed

if login_needed():
    st.button("Settings")
# else:
    # st.write("You need to log in first.")
