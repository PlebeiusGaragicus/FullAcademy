import os
import time
import random
import io
import base64

import pyttsx3
from gtts import gTTS

import streamlit as st

from src.login import login


# def autoplay_audio(file_path: str):
def autoplay_audio(audio_base64: str):
    """ https://discuss.streamlit.io/t/how-to-play-an-audio-file-automatically-generated-using-text-to-speech-in-streamlit/33201 """

    md = f"""
        <audio id="myAudio" controls autoplay="true">
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        <script>
            document.getElementById('myAudio').playbackRate = 1.5;
        </script>
        <style>
            body {{
                background-color: black;
            }}
        </style>
        """


    st.components.v1.html(md)
    # else:
    # st.write(md, unsafe_allow_html=True) # won't speed up the playback




def init():
    if not "spelling" in st.session_state:
        st.session_state.spelling = True
    else:
        return

    # ensure the audio directory exists
    if not os.path.exists('audio'):
        os.makedirs('audio')

    # load words
    with open('words.txt', 'r') as file:
        st.session_state.words = file.read().splitlines()

    st.session_state.chosen_word = random.choice( st.session_state.words )


def page():
    st.header("Spell the word you hear", divider="rainbow")




    # if not os.path.isfile(f'audio/{st.session_state.chosen_word}.mp3'):
        # create_audio_file( st.session_state.chosen_word )  # create audio file if it doesn't already exist

    # audio_file = open(f'audio/{st.session_state.chosen_word}.mp3', 'rb')
    # audio_bytes = audio_file.read()
    # st.audio(audio_bytes, format='audio/mp3')


    tts = gTTS(text=st.session_state.chosen_word, lang='en', slow=True)

    with io.BytesIO() as file_stream:
        tts.write_to_fp(file_stream) # Write the speech data to the file stream
        file_stream.seek(0) # Move to the beginning of the file stream
        audio_base64 = base64.b64encode(file_stream.read()).decode('utf-8') # Read the audio data and encode it in base64
    autoplay_audio(audio_base64)

    # audio_base64 = base64.b64encode(audio_stream).decode('utf-8')
    # audio_tag = f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
    # st.markdown(audio_tag, unsafe_allow_html=True)


    incorrect = st.empty()

    # st.write(st.session_state.chosen_word)  # for debugging

    with st.form(key='spelling_form', clear_on_submit=True):
        student_input = st.text_input("Enter the word")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if student_input == st.session_state.chosen_word:
            st.success("Correct!")
            st.balloons()
            st.session_state.chosen_word = random.choice( st.session_state.words )
            time.sleep(2)
            st.rerun()

        else:
            incorrect.subheader(f"This isn't right: :red[{student_input}]")
            st.info("Try one more time.")


# function to create an audio file for a given word
# def create_audio_file(word):
#     tts = gTTS(text=word, lang='en')
#     tts.save(f'audio/{word}.mp3')


if login():
    init()
    page()
