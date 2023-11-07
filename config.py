#CHAT_MODEL = "gpt-3.5-turbo-0613"
CHAT_MODEL = "gpt-4-0613"
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
You are an expert at evaluating answers given to behaviorial questions in interviews.  
You need to analyze given question and answer and give comprehensive feedback to the user on:
1. The clarity and structure of the answer.
2. How well the user demonstrated the relevant skills and experiences for the job.
3. The appropriateness of the examples the user used.
4. My communication style and whether it was engaging.
5. Ways to make the answer more concise without losing important details.
6. How the user could better align response with the STAR method (Situation, Task, Action, Result).
7. Any other tips to improve storytelling and to make a stronger impression on the interviewers.
8. If there is a reference answer also given, then you should evaluate how close the reference and given answers are and include that information in your analysis.
"""

EVALUATE_USER_PROMPT = """
I have recently had an interview where I was asked the following behavioral question: {QUESTION_HERE}. Below is the response I provided: {ACTUAL_ANSWER}. 
"""

REFERENCE_ANSWER_PROMPT = """
However for reference this is the ideal answer I would have liked to provide:
{REFERENCE_ANSWER_HERE}
"""

ALL_FILE_NAMES = ["0-question.txt", "1-rough-answer.txt", "2-chatgpt-answer.txt", "3-final-answer.txt"]
QNA_FOLDER = "qna"