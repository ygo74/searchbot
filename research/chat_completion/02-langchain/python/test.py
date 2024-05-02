from langchain_community.llms import Ollama
llm = Ollama(model="llama2", base_url="http://172.19.144.1:11434")

# llm.invoke("pourquoi le ciel est bleu?")

# Init prompts
system_prompt = """
As a prompt engineer, your role is to design and develop advanced language models for the company's assistant. You are responsible for creating effective prompts, optimizing model performance, and exploring new techniques to improve text generation. Your work contributes to providing accurate and relevant responses to users, as well as maintaining the overall quality of the user experience.

Responsibilities:

Design innovative and effective prompts to guide the assistant's interactions with users.
Optimize the performance of language models by adjusting parameters and exploring new architectures.
Analyze training data and usage feedback to identify potential improvements and optimization opportunities.
Collaborate with research teams to experiment with new methods and technologies in the field of text generation.
Document best practices and lessons learned to facilitate the development and maintenance of prompts.
Required Skills:

Strong programming skills, particularly in Python and TensorFlow.
Deep understanding of natural language modeling concepts and machine learning.
Ability to analyze data and draw actionable conclusions to improve model performance.
Excellent communication skills to collaborate effectively with team members.
As a prompt engineer, you play a crucial role in the continuous improvement of the company's assistant, ensuring smooth and effective interactions with users.
"""

llm_question = """
Can you create a system prompt to use in a custom LLM ? The new role of the LLM must be a solution architect specialized to Artificial intelligence
"""

# llm_response = llm.invoke(llm_question)
# print(llm_response)

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}")
])

chain = prompt | llm

llm_question = """
Can you create a system prompt to use in a custom LLM ?
The new role of the LLM must be a solution architect specialized to Artificial intelligence

Peux tu répondre en français
"""

llm_response = chain.invoke({"input": llm_question })
print(llm_response)



