import json

import streamlit as st

from src.login import login



def add_word(word, example):
    """checks session state for new word, adds it to the list of words, and saves the updated list to the file"""

    if word.strip() == "":
        st.toast("Word cannot be empty.")
        return

    # check st.session_state['words'] for the new word
    for w in st.session_state['words']['list']:
        if w['word'] == word:
            st.warning("Word already exists.")
            return
    # if word in st.session_state['words']['list']:
        # st.warning("Word already exists.")
        # return

    # add the new word to the list of words
    st.session_state['words']['list'].append(
        {
            "word": word,
            "example": example,
            "score": 0,
            "attempts": 0,
        }
    )


    # save the updated list of words to the file
    with open(f'./words/{st.session_state.user_select}_words.json', 'w') as file:
        json.dump(st.session_state['words'], file)
    
    st.toast("Word added")


def load_words():
    """loads the list of words from the file and saves it to the session state"""
    with open(f'./words/{st.session_state.user_select}_words.json', 'r') as file:
        data = json.load(file)
        st.session_state['words'] = data

    st.toast("Words loaded")






def page():
    if not login("root"):
        return
        # st.stop()
    
    student = st.selectbox("Select user", ["charlie", "presley"], key="user_select", index=None)

    if student:

        if not "words" in st.session_state:
            load_words()


        with st.form(key='add_word_form', clear_on_submit=True):
            new_word = st.text_input("Enter a new word")
            example = st.text_input("Enter an example sentence")
            if st.form_submit_button('Submit'):
                add_word(new_word, example)


        st.header("Words", divider="rainbow")

        for w in st.session_state['words']['list']:
            # st.write(f"Word: {w['word']}")
            # st.write(f"Example: {w['example']}")

            cols = st.columns((1, 4))
            with cols[0]:
                st.write(w['word'])

            with cols[1]:
                if st.button("Delete", key=f"{w['word']}_delete"):
                    st.session_state['words']['list'].remove(w)
                    with open(f'./words/{st.session_state.user_select}_words.json', 'w') as file:
                        json.dump(st.session_state['words'], file)
                    # st.toast("Word deleted")
                    st.rerun()


        word_list = st.text_area("Bulk add", height=200)

        if st.button("Bulk add"):
            for word in word_list.split("\n"):
                add_word(word, "")
            st.rerun()


        # st.divider()
        # st.text_area("Words", json.dumps(st.session_state['words'], indent=4), height=500)


        if st.button("Reset stats", key="reset_stats"):
            if st.button(":red[are you sure!?!?!]"):
                for w in st.session_state['words']['list']:
                    w['score'] = 0
                    w['attempts'] = 0

                with open('words.json', 'w') as file:
                    json.dump(st.session_state['words'], file)
                st.toast("Stats reset!!")
                st.rerun()
