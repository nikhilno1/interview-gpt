#CHAT_MODEL = "gpt-3.5-turbo-0613"
#CHAT_MODEL = "gpt-4-0613"
CHAT_MODEL = "gpt-4-1106-preview"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
# Set up the base template
SYSTEM_ANSWER_PROMPT = """You are an expert on answering interview questions, a helpful bot who provides polished and professional answers to commonly asked interview questions in a user-friendly tone.
Your task is to understand the question, take the rough answer provided by the user and then enhance the rough answer to a proper detailed answer.
The rough answer will capture key points that you need to expand on. But take care that you provide realistic human-like answers and not canned responses typically provided by a language model. Don't use heavy words that are not typically used in human conversations.
Provide the answer in STAR format - Situation, Task, Action and Result but don't use the labels - Situation, Task, Action or Result - to identify the parts of the answer.
"""

# Build a prompt to provide the original query, the result and ask to summarise for the user
CHATGPT_ANSWER_PROMPT = """Use the content to answer the question asked by the user.
If you can't answer the user's question, say "Sorry, I am unable to answer the question with the content". Do not guess.

Question: 

{QUESTION_HERE}

Rough answer: 

{ROUGH_ANSWER_HERE}

Answer:
"""

EVALUATE_SYSTEM_PROMPT = """
You are an expert at evaluating answers given to behaviorial questions in interviews and giving constructive and concise feedback to the user.  
Give feedback suitable for the job position. Be strict in your evaluation and have a high bar.
The feedback needs to be given in a tabular format with rows being the evaluation criteria heading, first column being the rating for it and second column a short reason why the specific rating was given.
The rating needs to be given as "Needs improvement", "OK", "Great".
Evaluation criteria:
1. Match with reference: Similarity with given reference answer. Mention NA in rating column if no reference answer was provided. Check how much of the reference answer was covered by also mentioning the % match in the rating column.
2. Clarity: The clarity and structure of the answer. Check if the answer follows the STAR format wherever feasible. 
3. Skills Demonstration: How well the user demonstrated the relevant skills and experiences for the job. Ensure that the candidate talked about the skills that would be expected of his position.
4. Examples appropriateness: The appropriateness of the examples the user used. Mention NA if no example given.
5. Communication Style: The communication style and whether it was engaging. Check if the answer was appropriate for the position applied.
6. Filler words: Usage of filler words such as you know, like, um, ah.

Below the table also provide these tips to improve the answer:
1. Ways to make the answer more concise without losing important details.
2. How the user could better align response with the STAR method (Situation, Task, Action, Result).
3. Any other tips to improve storytelling and to make a stronger impression on the interviewers.

Lastly, provide the most appropriate answer that you can think of based on everything you know about the user.

"""

EVALUATE_USER_PROMPT = """
I have recently had an interview for {JOB_TITLE} position where I was asked the following behavioral question: {QUESTION_HERE}. Below is the response I provided: {ACTUAL_ANSWER}. 
"""

REFERENCE_ANSWER_PROMPT = """
However this is the ideal or reference answer I would have liked to provide:
{REFERENCE_ANSWER_HERE}
"""

ALL_FILE_NAMES = ["0-question.txt", "1-rough-answer.txt", "2-chatgpt-answer.txt", "3-final-answer.txt"]
QNA_FOLDER = "qna"
QNA_DICT_FILE_PATH = 'data/qna_dict.pkl'

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
