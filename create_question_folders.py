import os
from config import ALL_FILE_NAMES, QUESTIONS_DATA

def create_files_inside_folder(folder_path):
    # Create the files in the folder        
    for file_name in ALL_FILE_NAMES:
        file_path = os.path.join(folder_path, file_name)  # Assuming .txt extension
        with open(file_path, 'w') as f:
            # You can write initial content to the files here if needed
            pass

def write_question_data(folder_path, question_text):
    # Create the "question" file and write the question text to it
    question_file_path = os.path.join(folder_path, ALL_FILE_NAMES[0])
    with open(question_file_path, 'w') as f:
        f.write(question_text)

def create_folders_for_questions():    
    # Base directory where folders will be created
    base_dir = "qna"

    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    # Iterate over the questions to create folders and files
    for question in QUESTIONS_DATA:
        # Split question text and folder name
        split_parts = question.split("|")
        question_text = split_parts[0].strip()
        folder_name = split_parts[-1].strip()
        folder_path = os.path.join(base_dir, folder_name)
        
        # Create the folder if it doesn't already exist
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            create_files_inside_folder(folder_path)   
            write_question_data(folder_path, question_text)
            print("Folder " + folder_path + " created successfully!")    

# Main application logic
def main():
    create_folders_for_questions()

if __name__ == '__main__':
    main()    