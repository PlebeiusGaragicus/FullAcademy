import streamlit as st

from src.database import get_db
from src.login import login


def create_user_if_needed():
    if st.session_state.username is None:
        return

    db = get_db()

    # get users collection
    users = db["users"]

    # find user by name
    user = users.find_one({"name": st.session_state.username})
    # if not found, create one
    if not user:
        st.balloons()
        st.toast("Welcome to Full Academy!", icon="🎉")
        user = {"name": st.session_state.username}
        users.insert_one(user)


def show_collections():
    db = get_db()
    st.markdown("## Collections")
    st.write(db.list_collection_names())


def show_users():
    db = get_db()
    users = db["users"]
    all_users = list(users.find())

    st.markdown("## Users")
    st.write(all_users)

    # for each user, create a delete button
    for user in all_users:
        if st.button(f"Delete {user['name']}"):
            users.delete_one({"name": user["name"]})



def page():
    if not login():
        return

    st.header(f":rainbow[Welcome, {st.session_state.username}!] 👋🏻")

    create_user_if_needed()

    show_collections()
    show_users()
