import os
from config import ALL_FILE_NAMES

# Sample text (You can extend this list for all your questions)
QUESTIONS_DATA = [
    "Tell me about yourself. | Self-introduction",
"How have you managed a poor performer on your team? | Management",
"How do you approach building a team roadmap? | Roadmapping",
"Tell me about a project that wasn't successful. | Failed project",
"Tell me about a conflict at work. | Conflict",
"Have you promoted someone? How do you go about it? | Promotion",
"As a manager, how do you handle trade-offs? | Trade-offs",
"How do you coach and develop your engineering team? | Coaching",
"Describe your work style. | Work style",
"What are the challenges you faced in your role? | Challenges",
"What did you like about your previous job? | Job like",
"What did you dislike about your previous job? | Job dislike",
"What major challenges and problems did you face? How did you handle them? | Problem-solving",
"What is your greatest strength? | Strength",
"What is your greatest weakness? | Weakness",
"How do you handle stress and pressure? | Stress",
"Describe a difficult work situation / project and how you overcame it. | Overcoming",
"What was the biggest accomplishment in this position? | Accomplishment",
"What was the biggest accomplishment in this position? | Failure",
"How do you evaluate success? | Evaluation",
"Why are you leaving or have left your job? | Departure",
"Why should we hire you? | Justification",
"What are your goals for the future? | Goals",
"What are your salary requirements? | Salary",
"Who was your best boss? | Best Boss",
"Who was your worst boss? | Worst Boss",
"What are you passionate about? | Passion",
"How would your supervisor or co-worker describe you? | Description",
"Have you ever had difficulty working with a manager or someone? | Difficulty",
"How would you handle it if your boss was wrong? | Disagreement",
"Is there a type of work environment you prefer? | Environment",
"What are you looking for in your next position? | Next position",
"What's your ideal company? | Ideal company",
"Give me an example of a time that you felt you went above and beyond the call of duty at work. | Exceeding",
"Can you describe a time when your work was criticized? | Criticism",
"Have you ever been on a team where someone was not pulling their own weight? How did you handle it? | Slackers",
"Tell me about a time when you had to give someone difficult feedback. How did you handle it? | Feedback",
"What is your greatest failure, and what did you learn from it? | Failure",
"What irritates you about other people, and how do you deal with it? | Irritation",
"If I were your supervisor and asked you to do something that you disagreed with, what would you do? | Disobedience",
"What was the most difficult period in your life, and how did you deal with it? | Difficult period",
"Give me an example of a time you did something wrong. How did you handle it? | Mistake",
"If you were at a business lunch and you ordered a rare steak and they brought it to you well done, what would you do? | Mismatch",
"What assignment was too difficult for you, and how did you resolve the issue? | Tough assignment",
"What's the most difficult decision you've made in the last two years and how did you come to that decision? | Decision-making",
"If you found out your company was doing something against the law, like fraud, what would you do? | Unethical",
"Describe how you would handle a situation if you were required to finish multiple tasks by the end of the day, and there was no conceivable way that you could finish them. | Impossible tasks",
"What are you looking for in terms of career development? | Career development",
"How do you want to improve yourself in the next year? | Improvement",
"How would you go about establishing your credibility quickly with the team? | Credibility",
"How long will it take for you to make a significant contribution? | Contribution",
"What do you see yourself doing within the first 30 days of this job? | First 30 days",
"If selected for this position, can you describe your strategy for the first 90 days? | First 90 days",
"What would be your ideal working environment? | Ideal environment",
"Give examples of ideas you've had or implemented. | Ideas",
"What techniques and tools do you use to keep yourself organized? | Organization",
"If you had to choose one, would you consider yourself a big-picture person or a detail-oriented person? | Perspective",
"Tell me about your proudest achievement. | Achievement",
"What kind of personality do you work best with and why? | Compatibility",
"What is your personal mission statement? | Mission statement",
"What are three positive things your last boss would say about you? | Positive traits",
"What negative thing would your last boss say about you? | Negative trait",
"What three character traits would your friends use to describe you? | Friends' perspective",
"What are three positive character traits you don't have? | Lacking traits",
"List five words that describe your character. | Character",
"What is your greatest fear? | Fear",
"What is your biggest regret and why? | Regret",
"What is your greatest achievement outside of work? | External achievement",
"What are the qualities of a good leader? A bad leader? | Leadership",
"Do you think a leader should be feared or liked? | Leader perception",
"How would you feel about working for someone who knows less than you? | Superior knowledge",
"Tell me one thing about yourself you wouldn't want me to know. | Secret",
"What's the last book you read? | Last book"
]

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
        
        # Create the folder
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        
        # Create the files in the folder        
        for file_name in ALL_FILE_NAMES:
            file_path = os.path.join(folder_path, file_name)  # Assuming .txt extension
            with open(file_path, 'w') as f:
                # You can write initial content to the files here if needed
                pass
        
        # Create the "question" file and write the question text to it
        question_file_path = os.path.join(folder_path, ALL_FILE_NAMES[0])
        with open(question_file_path, 'w') as f:
            f.write(question_text)

    print("Folders and files created successfully!")

# Main application logic
def main():
    create_folders_for_questions()

if __name__ == '__main__':
    main()    