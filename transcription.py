import os
import datetime
import openai
import streamlit as st

from audio_recorder_streamlit import audio_recorder

# import API key from .env file
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY", "")


def transcribe(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="en")
    return transcript

def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"recordings/audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name


def transcribe_audio(file_path):
    """
    Transcribe the audio file at the specified path.

    :param file_path: The path of the audio file to transcribe
    :return: The transcribed text
    """
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)

    return transcript["text"]


def run_transcription_app():
    """
    Main function to run the Transcription app.
    """
    st.markdown("---")
    st.header("Record your answer")
    st.markdown('<small>Click the mic to start/stop the recording. Then click Analyze.</small>', unsafe_allow_html=True)    
   
    # Record Audio tab
    audio_bytes = audio_recorder(energy_threshold=(-1.0, 1.0),  pause_threshold=120.0)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        save_audio_file(audio_bytes, "mp3")
        st.session_state.analyze_button_disable = False            


def do_transcribe():
    # Find the newest audio file
    subdirectory_path = os.path.join(".", "recordings")

    audio_file_path = max(
        [os.path.join(subdirectory_path, f) for f in os.listdir(subdirectory_path) if f.startswith("audio")],
        key=os.path.getctime,
    )

    # Transcribe the audio file
    transcript_text = transcribe_audio(audio_file_path)

    # Display the transcript
    st.header("Transcript")
    st.write(transcript_text)
    
    # Save the transcript to a text file    
    a_file = os.path.splitext(os.path.basename(audio_file_path))[0]
    with open("transcripts/ts_" + a_file + ".txt", "w") as f:
        f.write(transcript_text)
        
    return transcript_text
    # Provide a download button for the transcript
    #st.download_button("Download Transcript", transcript_text)
   
