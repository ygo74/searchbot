from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json
from opik import track, llm_unit

# Load environment variables from .venv
load_dotenv()

# llm answer comparateur system_prompt
comparison_system_prompt= """
You are an assistant using the GPT-4o model and helping to compare two results for a question
You receive the question in the balise <question></question>.
You receive the expected result in the balise <expected></expected>.
You received the current result in the balise <current><current>.
You always must answer with a Json structure and give the following information : comparison, score, best_answer, reason
You must compare the two results and indicate if they mean the same idea and wich score
if the two ansers are identical, you must answer 'both' in the best_answer

Exemples :
1. Comparison where expected is better than current
Prompt:
<question>Dans quel département se trouve la ville de Boulogne sur mer</question>
<expected>Pas de calais</expected>
<current>Le Pas de calais dans la région Haut de France</current>

Expected result:
{{
    "comparison": "OK",
    "score": 1
    "best_answer": "expected",
    "reason": "la réponse current contient des informations additionelles alors que la question est fermée, la réponse ne doit contenir que le département"
}}

2. Comparison where expected is equal to current
Prompt:
<question>How many branches does the Rhine branch into?</question>
<expected>Three</expected>
<current>Three branches</current>

Expected result:
{{
    "comparison": "OK",
    "score": 1
    "best_answer": "both",
    "reason": "expecte dand current have the same value, even if current add the unit of this answer"
}}

2. Comparison where current is better than current
Prompt:
<question>Which sea was oil discovered in?</question>
<expected>North</expected>
<current>The North Sea</current>

Expected result:
{{
    "comparison": "OK",
    "score": 1
    "best_answer": "current",
    "reason": "expected and current have the same value, but current uses the real name of the sea"
}}

"""

user_system_prompt = """
<question>{question}</question>
<expected>{expected}</expected>
<current>{current}</current>
"""

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2024-02-01",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


# Fonction pour tester le LLM
@track
def get_llm_response(prompt):
    return llm.invoke(prompt)

# Fonction pour comparer les résultats
def compare_result(question, expected, current):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", comparison_system_prompt),
            ("human", user_system_prompt),
        ]
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "question": question,
            "expected": expected,
            "current": current
        }
    )

    data = json.loads(result.content)
    return data
