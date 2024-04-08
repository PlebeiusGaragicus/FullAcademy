import os
import json
import time
import random
import subprocess

import streamlit as st

from src.login import login
from src.database import get_db
from src.schema import UserAttempt





def choose_word():
    st.session_state.failed_attempts = 0
    st.session_state.given_up = False
    st.session_state.speak_word = True

    db = get_db()

    # query for problems with this problem set id
    problems = list(db["problem"].find({"problem_set_id": str(st.session_state.practice_set["_id"])}))

    with st.expander("words"):
        st.write(problems)

    random_word = random.choice(problems)
    st.session_state.chosen_word_id = str(random_word['_id'])
    st.session_state.chosen_word = random_word['word']


def chosen_word():
    return st.session_state.chosen_word



def select_a_set():
    with st.container(border=True):
        db = get_db()

        # user_id = db["users"].find_one({"name": st.session_state.username})["_id"]
        # user_id_str = str(user_id)
        # st.sidebar.write(f"User ID: '{user_id_str}'")

        problemsets = list(db["problemset"].find({"user_id": st.session_state.user_id_str}))

        # find problem sets of type "spelling"
        spelling_sets = [problemset['title'] for problemset in problemsets if problemset['type'] == "spelling"]

        selected_set = practice_set = st.selectbox("Spelling sets", spelling_sets, index=None)

        if selected_set:
            # find the selected set
            st.session_state.practice_set = db["problemset"].find_one({"title": selected_set})
            st.rerun()

    st.stop()



def show_attempts():
    db = get_db()
    attempts = list(db["attempts"].find({"user_id": st.session_state.user_id_str, "problem_id": st.session_state.chosen_word_id}))
    st.write(attempts)

    accuracy = sum([attempt['was_correct'] for attempt in attempts]) / len(attempts) if len(attempts) > 0 else 0
    color = "green" if accuracy > 0.8 else "red"
    st.write(f"Accuracy: :{color}[{accuracy * 100:.0f}%]")


def change_score(correct):
    db = get_db()
    attempt = UserAttempt(user_id=st.session_state.user_id_str,
                            problem_id=st.session_state.chosen_word_id,
                            was_correct=correct)

    db['attempts'].insert_one(attempt.model_dump())



###############################################
def page():
    if not login():
        return

    st.header('🧠 :rainbow[Spelling practice]', divider="rainbow")


    # NOTE: shouldn't need this anymore because this page is hidden and only accessible from the "Study this" button
    # if not "practice_set" in st.session_state:
    #     select_a_set()

    st.write(st.session_state.practice_set)

    if not st.session_state.chosen_word:
        choose_word()
        st.toast("Ready to learn!")

    st.markdown(f"# word: {st.session_state.chosen_word}")

    show_attempts()

    ### GUESS SUBMISSION FORM
    with st.form(key='spell_test_form', clear_on_submit=True):
        guess = st.text_input('Type the word you hear:', key='word_input')
        if st.form_submit_button(':green[Submit]'):
            if guess.lower() == chosen_word():
                if st.session_state.given_up:
                    st.warning("Good practice!")
                else:
                    if st.session_state.failed_attempts < 2:
                        change_score(True)
                        st.toast("Correct!")
                choose_word()
                st.balloons()
                # st.success('Correct!')
                time.sleep(1)
                st.rerun()

                # STUDENT GOT IT WRONG
            else:
                # create a UserAttempt in the 'attempts' collection
                # db = get_db()
                # attempt = UserAttempt(user_id=st.session_state.user_id_str,
                #                       problem_id=st.session_state.chosen_word_id,
                #                       was_correct=False)

                # db['attempts'].insert_one(attempt.model_dump())

                st.session_state.speak_word = True
                change_score(False)
                if st.session_state.failed_attempts == 0:
                    st.error('Incorrect! Try again.')
                    st.rerun()
                # elif st.session_state.failed_attempts == 1:
                    # st.error('Try one more time!')
                else:
                    st.markdown(f"# Sorry, the word was `{chosen_word()}`")
                    # choose_word()
                    # st.rerun()

                st.session_state.failed_attempts += 1








    # if st.session_state.failed_attempts < 2:
    #     ### BUTTONS
    #     cols = st.columns([3, 1, 1, 1])
    #     with cols[0]:
    #         if st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts'] > 0:
    #             st.write(f"{st.session_state['words']['list'][st.session_state.chosen_word_index]['score'] / st.session_state['words']['list'][st.session_state.chosen_word_index]['attempts'] * 100:.2f}%")
    #         # else:
    #             # st.write("Never tried this word")

    #     with cols[1]:
    #         if st.button(":blue[Show]"):
    #             st.session_state.given_up = True
    #             # st.markdown(f":blue[{chosen_word()}]")

    #     with cols[2]:
    #         placeholder_sayitagain = st.empty()

    #     with cols[3]:
    #         placeholder_skip = st.empty()
            


    #     if st.session_state.given_up:
    #         st.markdown(f"# :blue[{chosen_word()}]")


    #     ### SPEAK THE WORD
    #     if st.session_state.speak_word:
    #         example = st.session_state['words']['list'][st.session_state.chosen_word_index]['example']
    #         if example != "":
    #             subprocess.run(['say', f"Spell: `{chosen_word()}`.\n\n", f"As in: '{example}'", '-v', 'Alex'])
    #         else:
    #             subprocess.run(['say', f"Spell: `{chosen_word()}`", '-v', 'Alex'])

    #         st.session_state.speak_word = False

    #     if not st.session_state.given_up:
    #         if placeholder_sayitagain.button('Say it :orange[again]'):
    #             st.session_state.speak_word = True
    #             st.rerun()
        
    #     if placeholder_skip.button(":red[Skip]"):
    #         choose_word()
    #         st.rerun()
