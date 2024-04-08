import os
import json
import time
import random
import subprocess

import streamlit as st

from src.login import login

def choose_word():
    st.session_state.chosen_word_index = random.randint(0, len(st.session_state['words']['list']) - 1)
    st.session_state.failed_attempts = 0
    st.session_state.given_up = False
    st.session_state.speak_word = True

def chosen_word():
    return st.session_state['words']['list'][st.session_state.chosen_word_index]['word']




###############################################
def page():
    if not login():
        return

    st.header('Spelling TEST', divider="rainbow")


    ### INIT
    if not 'test' in st.session_state:
        st.session_state.test = True

        with open(f'./words/{st.session_state.username}_words.json') as f:
            st.session_state.words = json.load(f)

        choose_word()
        st.session_state.correct_words = 0
        st.session_state.incorrect_words = 0
        st.toast("Ready to learn!")





    ### GUESS SUBMISSION FORM
    with st.form(key='spell_test_form', clear_on_submit=True):
        guess = st.text_input('Type the word you hear:', key='word_input')
        if st.form_submit_button(':green[Submit]'):
            if guess.lower() == chosen_word():
                choose_word()
                st.session_state.correct_words += 1
                st.balloons()
                time.sleep(1)
                st.rerun()

                # STUDENT GOT IT WRONG
            else:
                st.session_state.speak_word = True
                st.session_state.incorrect_words += 1
                st.error('WRONG')
                time.sleep(1)
                choose_word()
                st.rerun()


    if st.session_state.incorrect_words > 2:
        st.error("You need more practice.")
        st.warning("Refresh the page to try again.")
        st.stop()


    if st.session_state.correct_words >= 10:
        st.success("You passed the test!")
        st.info("This is your pass to :rainbow[SCREEN TIME!]")
        st.stop()

    st.write(f"Correct: {st.session_state.correct_words}")

    # st.write(st.session_state.chosen_word_index)
    # st.write(chosen_word())

    if st.button('Say it :orange[again]'):
        st.rerun()

    example = st.session_state['words']['list'][st.session_state.chosen_word_index]['example']
    if example != "":
        subprocess.run(['say', f"Spell: `{chosen_word()}`.\n\n", f"As in: '{example}'", '-v', 'Alex'])
    else:
        subprocess.run(['say', f"Spell: `{chosen_word()}`", '-v', 'Alex'])


