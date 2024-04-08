import os
import json
import time
import random
import subprocess

import streamlit as st

from src.login import login


###############################################
def page():
    if not login():
        return

    st.header('📈 :rainbow[Spelling progress]', divider="rainbow")

    st.write("This is the spelling practice page.")
