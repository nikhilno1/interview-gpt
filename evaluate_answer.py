import streamlit as st
import openai
import os
from config import CHAT_MODEL, EVALUATE_SYSTEM_PROMPT, EVALUATE_USER_PROMPT, REFERENCE_ANSWER_PROMPT, ALL_FILE_NAMES, QNA_FOLDER
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
user_job_title = os.getenv("USER_JOB_TITLE", "")
if user_job_title == "":
    user_job_title = st.secrets["USER_JOB_TITLE"]

def get_qna_content(selected_option, file_name):
    # Construct the full path to the file
    if selected_option is None:
        st.write ("No option has been selected!")
    else:
        file_path = os.path.join(QNA_FOLDER, selected_option, file_name)
           
    # Open and read the file
    with open(file_path, 'r') as file:
        content = file.read()
        #print(content)

    return content

def evaluation_result(actual_answer, selected_option):
    st.header("Analysis")
    with st.spinner("Evaluating your answer..."):    
        question = get_qna_content(selected_option, ALL_FILE_NAMES[0])
        reference_answer = get_qna_content(selected_option, ALL_FILE_NAMES[3])

        evaluate_answer_prepped = EVALUATE_USER_PROMPT.format(
            JOB_TITLE=user_job_title, QUESTION_HERE=question, ACTUAL_ANSWER=actual_answer
        )
        if len(reference_answer) > 10:
            evaluate_answer_prepped += REFERENCE_ANSWER_PROMPT.format(REFERENCE_ANSWER_HERE=reference_answer)
             
        chat_messages = [{"role": "system", "content": EVALUATE_SYSTEM_PROMPT},
                         {"role": "user", "content": evaluate_answer_prepped}]
        #print("chat_messages", chat_messages)
        
        compare_answer = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=chat_messages,
        )
        result = compare_answer.choices[0].message['content']
    return result

