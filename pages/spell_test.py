import os
import json
import time
import random
import subprocess

import streamlit as st

def choose_word():
    st.session_state.chosen_word_index = random.randint(0, len(st.session_state['words']['list']) - 1)
    # st.session_state.chosen_word = st.session_state['words']['list'][rand_index]

def chosen_word():
    return st.session_state['words']['list'][st.session_state.chosen_word_index]['word']

def change_score(correct: bool):
    if correct:
        st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] += 1
    else:
        st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] -= 1
    
    save_state()

def save_state():
    with open('words.json', 'w') as f:
        json.dump(st.session_state.words, f)









if not 'words' in st.session_state:
    with open('words.json') as f:
        st.session_state.words = json.load(f)
    
    choose_word()
    st.toast("ready")


st.header('Spelling Master', divider="rainbow")

# with st.columns([3, 1])[0]:
    # guess = st.text_input('Type the word you hear:', key='word_input')

with st.form(key='spell_test_form', clear_on_submit=True):
    guess = st.text_input('Type the word you hear:', key='word_input')
    if st.form_submit_button(':green[Submit]'):
# if guess is not None and guess != '':
        if guess.lower() == chosen_word():
            change_score(True)
            choose_word()
            st.balloons()
            # st.success('Correct!')
            time.sleep(1)
            st.rerun()
        else:
            change_score(False)
            st.error('Incorrect! Try again.')

cols = st.columns([4, 1, 1])
with cols[1]:
    if st.button('Say it :orange[again]'):
        st.rerun()

with cols[2]:
    if st.button(":red[Skip]"):
        choose_word()
        st.rerun()

        
example = st.session_state['words']['list'][st.session_state.chosen_word_index]['example']
if example != "":
    subprocess.run(['say', f"{chosen_word()}.\n\n", f"As in, {example}", '-v', 'Samantha'])
else:
    subprocess.run(['say', chosen_word(), '-v', 'Samantha'])

# if os.getenv("DEBUG"):
with st.popover("Debugging"):
    st.write(st.session_state)
