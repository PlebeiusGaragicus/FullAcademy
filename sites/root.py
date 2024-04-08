import streamlit as st

from src.database import get_db
from src.login import login

def page():
    if not login("root"):
        return

    st.header(f":red[ROOT PANEL]")

    db = get_db()

    st.markdown("## Collections")
    st.write(db.list_collection_names())

    # get users collection
    users = db["users"]

    all_users = list(users.find())

    st.markdown("## Users")
    st.write(all_users)

    # for each user, create a delete button
    for user in all_users:
        if st.button(f"Delete {user['name']}"):
            users.delete_one({"name": user["name"]})
