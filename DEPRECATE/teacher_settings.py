import streamlit as st

from src.login import login_required

# if not login_required():
    # st.stop()



st.header("Teacher Settings", divider="rainbow")
if st.button("Settings"):
    st.write("does nothing")

# if login("root"):
#     st.header("Teacher Settings", divider="rainbow")
#     if st.button("Settings"):
#         st.write("does nothing")
