import streamlit as st
import openai
import os
from config import CHAT_MODEL, EVALUATE_PROMPT, ALL_FILE_NAMES

def get_reference_answer(selected_option):
    # Construct the full path to the file
    if selected_option is None:
        st.write ("No option has been selected!")
    else:
        file_path = os.path.join("qna", selected_option, ALL_FILE_NAMES[3])
           
    # Open and read the file
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)

    return content

def evaluation_result(text_transcribed, selected_question):
    st.header("Analysis")
    with st.spinner("Evaluating your answer..."):    
        ref_answer = get_reference_answer(selected_question)
        chat_messages = [
            {"role": "system", "content": EVALUATE_PROMPT},
            {"role": "user", "content": f'Original Text: "{ref_answer}"'},
            {"role": "user", "content": f'Submitted Text: "{text_transcribed}"'}
        ]
        
        compare_answer = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=chat_messages,
        )
        result = compare_answer.choices[0].message['content']
    return result

