import streamlit as st

from enum import Enum

from sites.landing_page import page as landing_page
from sites.spelling_practice import page as spell_practice_page
from sites.spelling_progress import page as spelling_progress_page

from sites.study_collections import page as study_collections_page
from sites.collection_edit import page as collection_edit_page

# from sites.spelling_settings import page as spelling_settings_page
from sites.root import page as root_page



class Pages(Enum):
    HOME = ("Home", landing_page)


    SPELLING_PRACTICE = (":orange[Spelling practice]", spell_practice_page)
    SPELLING_PROGRESS = (":purple[Spelling progress]", spelling_progress_page)
    # SPELLING_TEST = (":green[Spelling test]", spelling_test_page)
    # SPELLING_SETTINGS = ("👨🏻‍🏫 :blue[Spelling settings]", spelling_settings_page)

    STUDY_COLLECTIONS = ("📚 :purple[Collections]", study_collections_page)
    COLLECTION_EDIT = ("📝 :blue[Collection edit]", collection_edit_page)

    ROOT_PANEL = ("🔒 :red[Root panel]", root_page)




if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state.current_page = Pages.HOME.value[0]


    def on_click(page):
        st.session_state.current_page = page

    with st.sidebar:
        for p in Pages:
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
