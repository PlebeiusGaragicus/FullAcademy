import os
import json
import time
import random
import subprocess

import streamlit as st

from src.login import login
from src.database import get_db
from src.schema import UserAttempt
from src.speech import TTS



def 



def choose_word():
    st.session_state.failed_attempts = 0
    st.session_state.given_up = False

    # query for problems with this problem set id
    db = get_db()
    problems = list(db["problem"].find({"problem_set_id": str(st.session_state.practice_set["_id"])}))
    # random_word = random.choice(problems)

    # find a word that hasn't been attempted yet
    attempted_words = [attempt['problem_id'] for attempt in db["attempts"].find({"user_id": st.session_state.user_id_str})]
    unattempted_words = [problem for problem in problems if problem['_id'] not in attempted_words]
    if unattempted_words:
        random_word = random.choice(unattempted_words)
    else:


        if random.random() < 0.7: # 70% chance
            # do the "hard" ones
            # if accuracy is less than 40, show the word
            problems_to_show = []
            for problem in problems:
                attempts = list(db["attempts"].find({"problem_id": problem['_id']}))
                accuracy = sum([attempt['was_correct'] for attempt in attempts]) / len(attempts) if len(attempts) > 0 else 0
                if accuracy < 0.4:
                    problems_to_show.append(problem)
            

        elif random.random() < 0.3:  # 10% chance
            # do the "easy" ones
            # if accuracy is less than 80 and above 40, show the word
            problems_to_show = []
            for problem in problems:
                attempts = list(db["attempts"].find({"problem_id": problem['_id']}))
                accuracy = sum([attempt['was_correct'] for attempt in attempts]) / len(attempts) if len(attempts) > 0 else 0
                if accuracy >= 0.8:
                    problems_to_show.append(problem)

        else: # 20% chance
            # do the "medium" ones
            # if accuracy 80% or better, show this word
            problems_to_show = []
            for problem in problems:
                attempts = list(db["attempts"].find({"problem_id": problem['_id']}))
                accuracy = sum([attempt['was_correct'] for attempt in attempts]) / len(attempts) if len(attempts) > 0 else 0
                if 0.4 <= accuracy < 0.8:
                    problems_to_show.append(problem)

        random_word = random.choice(problems_to_show)



    st.session_state.chosen_word_id = str(random_word['_id'])
    st.session_state.chosen_word = random_word['word']
    if random_word['example_usage']:
        st.session_state.speak_this = f"Spell: '{random_word['word']}'.\n\n As in: {random_word['example_usage']}"
    else:
        st.session_state.speak_this = f"Spell: '{random_word['word']}'."


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

        selected_set = st.selectbox("Spelling sets", spelling_sets, index=None)

        if selected_set:
            # find the selected set
            st.session_state.practice_set = db["problemset"].find_one({"title": selected_set})
            st.rerun()

    st.stop()



def show_attempts():
    db = get_db()
    attempts = list(db["attempts"].find({"user_id": st.session_state.user_id_str, "problem_id": st.session_state.chosen_word_id}))
    # st.write(attempts)

    accuracy = sum([attempt['was_correct'] for attempt in attempts]) / len(attempts) if len(attempts) > 0 else 0
    color = "green" if accuracy > 0.8 else "red"
    st.write(f"Accuracy: :{color}[{accuracy * 100:.0f}%]")


def change_score(correct):
    if st.session_state.given_up:
        return

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

    # st.write(st.session_state.practice_set)

    if not st.session_state.chosen_word:
        choose_word()
        st.toast("Ready to learn!")

    # st.markdown(f"# word: {st.session_state.chosen_word}")

    # TTS(st.session_state.speak_this, slow=False)
    # subprocess.run(['say', f"Spell: `{chosen_word()}`.\n\n", f"As in: '{example}'", '-v', 'Alex'])
    tts_placeholder = st.empty()

    show_attempts()

    # st.write(st.session_state.failed_attempts)

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
                st.session_state.failed_attempts += 1

                change_score(False)
                if st.session_state.failed_attempts == 0:
                    st.error('Incorrect! Try again.')
                    st.rerun()
                elif st.session_state.failed_attempts == 1:
                    st.error('Try one more time!')
                else:
                    st.markdown(f"# Sorry, the word was `{chosen_word()}`")
                    # choose_word()
                    # st.rerun()

    cols = st.columns([3, 1, 1, 1])
    give_up = st.empty()
    with cols[-1]:
        if st.button("😿 :grey[give up]"):    
            give_up.markdown(f"# :blue[{chosen_word()}]")
            st.session_state.given_up = True


    if st.session_state.failed_attempts < 2 and not st.session_state.given_up:
        with tts_placeholder:
            TTS(st.session_state.speak_this, slow=False)







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
