import streamlit as st
from streamlit_mic_recorder import mic_recorder
import openai
import io
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

state=st.session_state

if 'text_received' not in state:
    state.text_received=[]

if not '_last_audio_id' in state:
    state._last_audio_id=0    

def WhisperSTT(start_prompt="Start recording",stop_prompt="Stop recording",just_once=False,use_container_width=False,key=None):
    audio = mic_recorder(start_prompt=start_prompt,stop_prompt=stop_prompt,just_once=just_once,use_container_width=use_container_width,key=key)
    if audio is None:
        return None
    else:
        audio_BIO = io.BytesIO(audio['bytes'])
        success=False
        err=0
        text=None
        while not success and err<3: #Retry up to 3 times in case of OpenAI server error.
            try:
                #audio_file= open("./streamlit_audio_10_12_20235_19_27 PM.wav", "rb")
                audio_BIO.name = "audio.mp3"
                transcript = openai.Audio.transcribe("whisper-1", audio_BIO, language="en") 
            except Exception as e:
                print(str(e)) # log the exception in the terminal
                err+=1
            else:
                success=True
                text=transcript['text']
        return text
    
c1,c2=st.columns(2)
with c1:
    st.write("Convert speech to text:")
with c2:
    text=WhisperSTT(use_container_width=True,just_once=True,key='STT')

if text:       
    state.text_received.append(text)

for text in state.text_received:
    st.write(text)

st.write("Record your voice, and play the recorded audio:")
audio=mic_recorder(start_prompt="⏺️",stop_prompt="⏹️",key='recorder')

if audio:       
    st.audio(audio['bytes'])