import streamlit as st
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
#import extra_streamlit_components as stx
import random, os, json
from transcription import run_transcription_app, do_transcribe
from create_question_folders import create_folders_for_questions
from config import *
from evaluate_answer import evaluation_result
from generate_answers import generate_chatgpt_answer, qna_dict

st.set_page_config(
    page_title="Interview GPT",
    page_icon="📝",
)

# @st.cache_resource(experimental_allow_widgets=True)
# def get_manager():
#     return stx.CookieManager()

# cookie_manager = get_manager()
# cookies = cookie_manager.get_all()

#st.write(st.experimental_user)
def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

def create_folder(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

# Parse the question data separated by | and then sort it alphabetically based on the second field (summary)    
question_data = [(item.split('|')[0].strip(), item.split('|')[-1].strip()) for item in QUESTIONS_DATA]
question_data.sort(key=lambda pair: pair[1])

unique_user_id = get_remote_ip()
st.write(f'Your IP: {unique_user_id}')

#if "ajs_anonymous_id" in cookies:
#    unique_user_id = cookies["ajs_anonymous_id"] + "-" + get_remote_ip()     

recordings_folder = "recordings/" + unique_user_id
transcripts_folder = "transcripts/" + unique_user_id

def create_folders_for_user_data():
    global recordings_folder, transcripts_folder
    #create_folder(qna_dict_folder)    
    create_folder(recordings_folder)    
    create_folder(transcripts_folder)

#qna_dict_file_path = qna_dict_folder + '/qna_dict.pkl'
#print(qna_dict_file_path)

def read_qna_data(single_folder=""):    
    global qna_dict
    question = rough_answer = chatgpt_answer = ""
    for root, dirs, files in os.walk(QNA_FOLDER):
        if dirs == []:
            continue        
        if single_folder != "":
            # Keep only the passed folder name and remove all other elements
            dirs = [element for element in dirs if element == single_folder]
            #print("dirs updated to ", dirs)

        if "sample" in dirs:
            dirs.remove("sample")

        for dir in dirs:
            file_path =  os.path.join(root, dir) + '/'
            with open( file_path + ALL_FILE_NAMES[0], 'r') as file:
                question = file.read()                
                
            with open( file_path + ALL_FILE_NAMES[1], 'r') as file:
                rough_answer = file.read()

            with open( file_path + ALL_FILE_NAMES[2], 'r') as file:
                chatgpt_answer = file.read()

            with open( file_path + ALL_FILE_NAMES[3], 'r') as file:
                final_answer = file.read()    

            # update the dictionary
            json_data = {
                "question": question,
                "rough_answer": rough_answer,
                "chatgpt_answer": chatgpt_answer,
                "final_answer": final_answer
            }
            qna_dict[dir] = json.dumps(json_data)     
            #print("qna_dict updated for ", qna_dict[dir])       
    print("qna_dict generated.")        

def init_session_state():
    """Initialize the session state variables."""
    if 'initialization_done' not in st.session_state:
        st.session_state.initialization_done = False

    if 'selected_question' not in st.session_state:
        st.session_state.selected_question = None

    if 'prev_selected_question' not in st.session_state:
        st.session_state.prev_selected_question = None

    if 'random_button_pressed' not in st.session_state:
        st.session_state.random_button_pressed = False

    if 'analyze_button_disable' not in st.session_state:
        st.session_state.analyze_button_disable = True        

    if 'rough_answer_text' not in st.session_state:
        st.session_state.rough_answer_text = ""    

    if 'chatgpt_answer_text' not in st.session_state:
        st.session_state.chatgpt_answer_text = ""

    if 'final_answer_text' not in st.session_state:
        st.session_state.final_answer_text = ""            

def reset_fields():    
    st.session_state.rough_answer_text = "" 
    st.session_state.chatgpt_answer_text = ""
    st.session_state.final_answer_text = ""

def display_sidebar(options):
    """Render the sidebar elements."""
    with st.sidebar:
        st.title("All Questions")
        expanded = st.checkbox("Interview Questions", True)
        if expanded:
            selected_option = st.radio("Select a question", options, index=0)
            idx = options.index(selected_option)
            st.session_state.selected_question = question_data[idx][0]            
            if selected_option != st.session_state.prev_selected_question:
                reset_fields()
                st.session_state.prev_selected_question = selected_option
                
                #print("Resetted all state variables")


def get_selected_folder_from_question(question):
    option = [pair[1] for pair in question_data if pair[0] == question][0]    
    return option

def get_user_confirmation():
    st.write('Are you sure you want to save this answer? This will overwrite the existing saved answer.')
    col1, col2 = st.columns([.2, 1])

    with col1:
        yes_btn = st.button('Yes', key='yes')
    with col2:
        no_btn = st.button('No', key='no')

    # Confirmation buttons
    if yes_btn:
        st.success('Confirmed!')
        print("Clicked Yes")
        return True
    if no_btn:
        st.error('Cancelled!')
        print("Clicked No")
        return False
    return False

def save_answer_to_file(directory, folder, filename, content=""):    
    file_path =  directory + '/' + folder + '/' + filename 
    print("Saving to file ", file_path)
    with open(file_path, 'w') as file:
        #print("content, ", content)
        file.write(content)
    # update dictionary as well for the saved folder
    read_qna_data(folder) 

def display_qna_widgets(user_dict):
    #global qna_dict

    selected_option = get_selected_folder_from_question(st.session_state.selected_question)
    #if(qna_dict == {}):
    #    read_qna_dict_from_file()
    
    if(selected_option in qna_dict):
        #st.write(f'First action for: {selected_option}')    
        question_data = json.loads(qna_dict[selected_option])
        #print(question_data)
        
        st.session_state.rough_answer_text = question_data["rough_answer"]        
        if "chatgpt_answer" in question_data and st.session_state.chatgpt_answer_text == "":
            st.session_state.chatgpt_answer_text = question_data["chatgpt_answer"]            
        if "final_answer" in question_data and st.session_state.final_answer_text == "":    
            st.session_state.final_answer_text = question_data["final_answer"]
            #print("final_answer_text ", st.session_state.final_answer_text)

    # =========================================================================================== #
    rough_answer = st.text_area("Enter your rough answer:", value=st.session_state.rough_answer_text, height=200)
    col1, col2 = st.columns([.2, 1])

    with col1:
        rough_answer_submit = st.button('Submit', key='rough_answer')
    with col2:
        rough_answer_save = st.button('Save', key='rough_answer_save')
    
    if rough_answer_submit:
        chatgpt_answer = generate_chatgpt_answer(st.session_state.selected_question, rough_answer, user_dict)
        st.session_state.rough_answer_text = rough_answer
        st.session_state.chatgpt_answer_text = chatgpt_answer

    if rough_answer_save:        
        st.session_state.rough_answer_text = rough_answer 
        save_answer_to_file(QNA_FOLDER, selected_option, ALL_FILE_NAMES[1], rough_answer)
    # =========================================================================================== #
    chatgpt_answer = st.text_area("ChatGPT refined answer:", value=st.session_state.chatgpt_answer_text, height=200)    
    col1, col2 = st.columns([.2, 1])

    with col1:
        chatgpt_answer_copy = st.button('Copy', key='chatgpt_answer')
    with col2:
        chatgpt_answer_save = st.button('Save', key='chatgpt_answer_save')        

    if chatgpt_answer_copy:
        st.session_state.chatgpt_answer_text = chatgpt_answer
        st.session_state.final_answer_text = chatgpt_answer
        #print("2 chatgpt_answer is ", st.session_state.chatgpt_answer_text)
    
    if chatgpt_answer_save:
        st.session_state.chatgpt_answer_text = chatgpt_answer 
        save_answer_to_file(QNA_FOLDER, selected_option, ALL_FILE_NAMES[2], chatgpt_answer)

    # =========================================================================================== #
    final_answer = st.text_area("Final answer:", value=st.session_state.final_answer_text, height=200)
    col1, col2 = st.columns([.2, 1])

    with col1:
        final_answer_submit = st.button('Submit', key='final_answer')
    with col2:
        final_answer_save = st.button('Save', key='final_answer_save')

    #print("3 final_answer is ", final_answer)
    if final_answer_submit:
        st.session_state.final_answer_text = final_answer    
        #st.write(f'Updated final answer: {final_answer}')    
        #print("4 final_answer is ", final_answer)

    if final_answer_save:
        st.session_state.final_answer_text = final_answer 
        save_answer_to_file(QNA_FOLDER, selected_option, ALL_FILE_NAMES[3], final_answer)  

def display_main_content(questions):
    """Render the main page of the application."""

    user_dict = {}
    # Show user input fields
    col1, col2, col3 = st.columns([1, .5, 1])
    with col1:
        user_dict["title"] = st.text_input('Job Title', DEFAULT_JOB_TITLE)
    with col2:
        user_dict["years"] = st.text_input('Years of Experience', DEFAULT_EXPERIENCE)
    with col3:
        user_dict["company"] = st.text_input('Interviewing Company', DEFAULT_COMPANY)    
    st.markdown("---")

    if st.button("Pick a Random Question"):
        selected_question = random.choice(questions)        
        # Don't select the same question twice
        while selected_question == st.session_state.selected_question:
            selected_question = random.choice(questions)
        st.session_state.selected_question = selected_question
        st.session_state.random_button_pressed = True
        reset_fields()
    else:
        st.session_state.random_button_pressed = False
    
    if st.session_state.selected_question:
        st.header(st.session_state.selected_question)
        
        display_qna_widgets(user_dict)       
        run_transcription_app(recordings_folder)        

        if st.button('Analyze', key='analyze', disabled=st.session_state.get("analyze_button_disable", True)):
            transcription = do_transcribe(recordings_folder, transcripts_folder)
            #selected_option = [pair[1] for pair in question_data if pair[0] == st.session_state.selected_question][0]
            selected_option = get_selected_folder_from_question(st.session_state.selected_question)
            eval_result = evaluation_result(transcription, selected_option, st.session_state.final_answer_text, user_dict)
            st.write(eval_result)
            st.session_state.analyze_button_disable = True            

# Main application logic
def main():
    init_session_state()    
    # Read the questions data and create qna folders for first time
    if st.session_state.initialization_done is False:
        create_folders_for_questions()
        create_folders_for_user_data()
        read_qna_data()
        st.session_state.initialization_done = True

    st.title("Welcome to Interview GPT")       
    _, extracted_words = zip(*question_data)
    display_sidebar(extracted_words)
    display_main_content([pair[0] for pair in question_data])

if __name__ == '__main__':
    main()
