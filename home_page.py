import streamlit as st

from enum import Enum

from sites.home_page import page as home_page
from sites.spell_practice import page as spell_practice_page
from sites.spelling_progress import page as spelling_progress_page
from sites.spelling_TEST import page as spelling_test_page



class Pages(Enum):
    HOME = ("Home", home_page)

    ### BTC
    SPELLING_PRACTICE = (":orange[Spelling practice]", spell_practice_page)
    SPELLING_TEST = (":green[Spelling test]", spelling_test_page)
    HISTORICAL_PRICE = (":blue[Historical Bitcoin Price]", btc_historical_price_page)
    MINING_CALCS = (":red[Bitcoin Mining Calcs]", btc_mining_calcs_page)




if __name__ == "__main__":
    if "current_page" not in st.session_state:
        st.session_state.current_page = Pages.HOME.value


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
