import streamlit as st
import openai
import os
from config import *
from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env.local")
# user_job_title = os.getenv("USER_JOB_TITLE", "")
# if user_job_title == "":
#     user_job_title = st.secrets["USER_JOB_TITLE"]

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

def evaluation_result(actual_answer, selected_option, reference_answer="", user_dict={}):
    st.header("Analysis")
    with st.spinner("Evaluating your answer..."):        
        question = get_qna_content(selected_option, ALL_FILE_NAMES[0])
        if (reference_answer == ""):
            reference_answer = get_qna_content(selected_option, ALL_FILE_NAMES[3])
        
        if(user_dict != {}):
            evaluate_answer_prepped = EVALUATE_USER_PROMPT.format(
                JOB_TITLE=user_dict["title"], COMPANY=user_dict["company"], QUESTION_HERE=question, ACTUAL_ANSWER=actual_answer, NUM_EXPERIENCE=user_dict["years"]
            )
        else:
            evaluate_answer_prepped = EVALUATE_USER_PROMPT.format(
                JOB_TITLE=DEFAULT_JOB_TITLE, COMPANY=DEFAULT_COMPANY, QUESTION_HERE=question, ACTUAL_ANSWER=actual_answer, NUM_EXPERIENCE=DEFAULT_EXPERIENCE
            )    
        
        if len(reference_answer) > 10:
            evaluate_answer_prepped += REFERENCE_ANSWER_PROMPT.format(REFERENCE_ANSWER_HERE=reference_answer)
        
        #print("EVALUATE_SYSTEM_PROMPT=", EVALUATE_SYSTEM_PROMPT)
        #print("evaluate_answer_prepped=", evaluate_answer_prepped)
        chat_messages = [{"role": "system", "content": EVALUATE_SYSTEM_PROMPT},
                         {"role": "user", "content": evaluate_answer_prepped}]
        #print("chat_messages", chat_messages)
        
        compare_answer = openai.ChatCompletion.create(
            model=CHAT_MODEL,
            messages=chat_messages,
        )
        result = compare_answer.choices[0].message['content']
    return result

