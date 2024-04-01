import os
import json
import time
import random
import subprocess

import streamlit as st

def choose_word():
    st.session_state.chosen_word_index = random.randint(0, len(st.session_state['words']['list']) - 1)
    st.session_state.failed_attempts = 0

def chosen_word():
    return st.session_state['words']['list'][st.session_state.chosen_word_index]['word']

def change_score(correct: bool):
    if correct:
        st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] += 1
    # else:
        # st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] -= 1

    st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts'] += 1
    save_state()

def save_state():
    with open('words.json', 'w') as f:
        json.dump(st.session_state.words, f)






###############################################
st.set_page_config(
    page_title="Spelling Master",
    initial_sidebar_state="collapsed",
    # layout="wide"
)
st.header('Spelling Master', divider="rainbow")


### INIT
if not 'words' in st.session_state:
    with open('words.json') as f:
        st.session_state.words = json.load(f)
    
    choose_word()
    st.toast("Ready to learn!")





### GUESS SUBMISSION FORM
with st.form(key='spell_test_form', clear_on_submit=True):
    guess = st.text_input('Type the word you hear:', key='word_input')
    if st.form_submit_button(':green[Submit]'):
        if guess.lower() == chosen_word():
            change_score(True)
            choose_word()
            st.balloons()
            # st.success('Correct!')
            time.sleep(1)
            st.rerun()

            # STUDENT GOT IT WRONG
        else:
            change_score(False)
            if st.session_state.failed_attempts == 0:
                st.error('Incorrect! Try again.')
            elif st.session_state.failed_attempts == 1:
                st.error('Try one more time!')
            else:
                st.markdown(f"# Sorry, the word was `{chosen_word()}`")
                # choose_word()
                # st.rerun()

            st.session_state.failed_attempts += 1


# st.write(f"Score: {st.session_state['words']['list'][st.session_state.chosen_word_index]['score']}")
# st.write(f"attempts: {st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts']}")

if st.session_state.failed_attempts <= 2:
    ### BUTTONS
    cols = st.columns([4, 1, 1])
    with cols[0]:
        if st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts'] > 0:
            st.write(f"Percentage: {st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] / st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts'] * 100:.2f}%")
        else:
            st.write("Never tried this word")

    with cols[1]:
        if st.button('Say it :orange[again]'):
            st.rerun()

    with cols[2]:
        if st.button(":red[Skip]"):
            choose_word()
            st.rerun()

    st.write(chosen_word())


    ### SPEAK THE WORD
    example = st.session_state['words']['list'][st.session_state.chosen_word_index]['example']
    if example != "":
        subprocess.run(['say', f"{chosen_word()}.\n\n", f"As in, {example}", '-v', 'Samantha'])
    else:
        subprocess.run(['say', chosen_word(), '-v', 'Samantha'])



with st.sidebar.popover("Debugging"):
    st.write(st.session_state)