import streamlit as st
import random
import os
from transcription import run_transcription_app, do_transcribe
from create_question_folders import create_folders_for_questions
from config import QUESTIONS_DATA
from evaluate_answer import evaluation_result

# Parse the question data separated by | and then sort it alphabetically based on the second field (summary)    
question_data = [(item.split('|')[0].strip(), item.split('|')[-1].strip()) for item in QUESTIONS_DATA]
question_data.sort(key=lambda pair: pair[1])
    
def init_session_state():
    """Initialize the session state variables."""
    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = None

    if 'random_button_pressed' not in st.session_state:
        st.session_state.random_button_pressed = False

    if 'analyze_button_disable' not in st.session_state:
        st.session_state.analyze_button_disable = True        

def display_sidebar(options):
    """Render the sidebar elements."""
    with st.sidebar:
        st.title("All Questions")
        expanded = st.checkbox("Interview Questions", True)
        if expanded:
            selected_option = st.radio("Select a question", options, index=0)
            idx = options.index(selected_option)
            st.session_state.selected_question = question_data[idx][0]

def display_main_content(questions):
    """Render the main page of the application."""

    if st.button("Pick a Random Question"):
        selected_question = random.choice(questions)
        # Don't select the same question twice
        while selected_question == st.session_state.selected_question:
            selected_question = random.choice(questions)
        st.session_state.selected_question = selected_question
        st.session_state.random_button_pressed = True
    else:
        st.session_state.random_button_pressed = False

    if st.session_state.selected_question:
        st.header(st.session_state.selected_question)
        run_transcription_app()        
        if st.button('Analyze', key='analyze', disabled=st.session_state.get("analyze_button_disable", True)):
            transcription = do_transcribe()
            selected_option = [pair[1] for pair in question_data if pair[0] == st.session_state.selected_question][0]
            eval_result = evaluation_result(transcription, selected_option)
            st.write(eval_result)
            st.session_state.analyze_button_disable = True            

# Main application logic
def main():
    # Read the questions data and create qna folders for first time
    create_folders_for_questions()

    st.title("Welcome to Interview-GPT")
    init_session_state()    
    
    _, extracted_words = zip(*question_data)
    display_sidebar(extracted_words)

    display_main_content([pair[0] for pair in question_data])

if __name__ == '__main__':
    main()
