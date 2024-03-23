import os
import yaml

import streamlit as st
import streamlit_authenticator as stauth

def setup_interface():
    # st.set_page_config(
    #     page_title="DEBUG!" if os.getenv("DEBUG", False) else "Pleb Chat",
    #     page_icon=os.path.join(ASSETS_PATH, "favicon.ico"),
    #     layout="centered",
    #     initial_sidebar_state="auto",
    # )
    pass


# def login_needed():
#     return False




def login_needed():
    """
    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    """

    try:
        with open("./auth.yaml") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        st.error("This instance of PlebChat has not been configured.  Missing `auth.yaml` file.")
        # TODO - just create an empty file and then re-run?  Put default root password in there and have user change it?
        st.stop()

    st.session_state.authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        # config["preauthorized"],
    )

    # if st.session_state["authentication_status"] is None:
        # if 'appstate' in st.session_state:
        #     del st.session_state['appstate']
        #     st.error("Application state has been cleared!")

    if st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
        return False

    # https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/
    # https://github.com/mkhorasani/Streamlit-Authenticator?ref=blog.streamlit.io
    st.session_state.authenticator.login(location="main", max_concurrent_users=1, fields={
        "Form name": "FullAcademy",
        "Username": "Username",
        "Password": "Password",
        "Login": "Enter, Teacher!",
    })


    if st.session_state["authentication_status"] is True:
        st.session_state.authenticator.logout(button_name=":red[👋🏻 Logout]")
        st.header("Teacher Settings", divider="rainbow")

        return True
