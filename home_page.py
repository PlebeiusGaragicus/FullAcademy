import streamlit as st

from enum import Enum


from sites.landing_page import page as landing_page
from sites.spelling_practice import page as spell_practice_page
from sites.spelling_progress import page as spelling_progress_page

from sites.practice import page as practice_page

from sites.study_collections import page as study_collections_page
from sites.collection_edit import page as collection_edit_page

# from sites.spelling_settings import page as spelling_settings_page
from sites.root import page as root_page

import sites


class Pages(Enum):
    HOME = (sites.HOME, landing_page, True)

    # SPELLING_PRACTICE = ("🧠 :orange[Spelling practice]", spell_practice_page)
    # SPELLING_TEST = (":green[Spelling test]", spelling_test_page)
    # SPELLING_SETTINGS = ("👨🏻‍🏫 :blue[Spelling settings]", spelling_settings_page)

    PRACTICE = ("🧠 :rainbow[Practice]", practice_page, False)

    STUDY_COLLECTIONS = ("📚 :green[Study Collections]", study_collections_page, True)
    COLLECTION_EDIT = ("📝 :blue[Edit a Collection]", collection_edit_page, True)

    SPELLING_PROGRESS = ("📈 :violet[Spelling progress]", spelling_progress_page, True)

    ROOT_PANEL = ("🔒 :red[Root panel]", root_page, True)



if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state.current_page = Pages.HOME.value[0]


    def on_click(page):
        st.session_state.current_page = page

    with st.sidebar:
        for p in Pages:
            if p.value[2]:
                button_text = p.value[0]
                if st.session_state.current_page == p.value[0]:
                    button_text = f"⭐️ **{button_text}** ⭐️"
                st.button(button_text, on_click=on_click, args=(p.value[0],), use_container_width=True)


    for p in Pages:
        if st.session_state.current_page == p.value[0]:
            p.value[1]()
            break

    with st.sidebar:
        with st.popover("🔧"):
            st.write(st.session_state)
