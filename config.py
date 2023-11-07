#CHAT_MODEL = "gpt-3.5-turbo-0613"
CHAT_MODEL = "gpt-4-0613"
EMBEDDINGS_MODEL = "text-embedding-ada-002"
# Set up the base template
SYSTEM_PROMPT = """You are an expert on answering interview questions, a helpful bot who provides polished and professional answers to commonly asked interview questions in a user-friendly tone.
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

EVALUATE_PROMPT = """
Begin by familiarizing yourself with the original text, understanding its key points, ideas, and overall message. Receive the submitted text from the individual and conduct a preliminary comparison to identify obvious similarities and differences, highlighting where these occur. Delve deeper into a detailed analysis, evaluating the submitted text for accuracy, completeness, coherence, and relevance in relation to the original text. Prepare feedback by listing down the similarities and affirming accurate representations, identifying and listing down discrepancies, missed points, or misinterpretations. Deliver your feedback, starting with positive aspects where the individual accurately reflected the original text, followed by pointing out areas of discrepancy and providing suggestions for improvement such as a more thorough review of the original text, seeking clarification when needed, and practicing articulation of key points. Encourage revision of the submitted text based on the feedback provided, offering to review the revised submission for further feedback. Reflect on the comparative analysis process and the feedback provided, considering any additional steps that might further support the individual in understanding and accurately representing the original text in future attempts. Through this structured approach, aim to foster a conducive learning environment that promotes self-awareness, constructive feedback, and continuous improvement in understanding and articulating textual materials.
"""

ALL_FILE_NAMES = ["0-question.txt", "1-rough-answer.txt", "2-chatgpt-answer.txt", "3-final-answer.txt"]