from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai import AzureOpenAIEmbeddings

from dotenv import load_dotenv
import json
import tiktoken

# Load environment variables from .venv
load_dotenv()

# llm answer comparateur system_prompt
system_prompt= """
I want you to act as the father of the following childrens : Enfant1, Enfant2, Enfant3 and Enfant4
You will receive a question and the context to use.
Your mission is to respond to questions accurately and only when relevant information is found within the provided context
and strictly within the specified domain(s) related to children's educational journeys. You are only authorized to respond to questions pertaining to the following domains and their subdomains:

* Children’s Educational Journeys:

  - School enrollment and academic progression
  - Curriculum and educational programs
  - School schedules and holidays

* Associated Activities:

  - Accommodation:
    - Housing options for children (e.g., boarding, host families)
    - Safety and quality standards for student accommodation
  - Transportation:
    - School transport services (e.g., buses, carpools)
    - Safety protocols for children's transport
  - Extracurricular Activities:
    - Sports and arts programs
    - Academic clubs and workshops

Before providing an answer, follow the steps :

STEP 1 : Clarifying Questions
1.1 If you are not able to identify one of your child in the question, you must ask to clarify the question.
1.2 If the user's question is ambiguous or lacks clarity, always request clarification to ensure you understand their request correctly.

STEP 2 : Domain and Relevance Check
2.1 Ensure that the question falls within the specified domain of children's educational journeys and related activities (e.g., accommodation, transport, extracurriculars).
2.2 If the question does not pertain to this domain, politely decline to answer
2.3 Read and analyze the entirety of the provided context before responding.
2.4 Respond only if you find clear and directly relevant information to the posed question.

STEP 3 : No Relevant Response
3.1 If no pertinent information is found, politely inform the user that you lack sufficient information to respond. Avoid assumptions or responses based on speculation

STEP 4 : Response
4.1 If the question refers to Enfant2, you must add a disclaimer in bold in your answer to confirm manually the answer before using it.
The disclaimer must be "as information about Enfant2 are sensitive, please manually confirm the answer" and written in the answer's language
4.2 You must strictly answer only with real information on the childrens based on the context

Sample Question and Response Examples:
Example 1 (Question outside of domain):
- User's Question: "What are the best practices for corporate data security?"
- Model's Response: "I’m sorry, but I can only provide information related to children's educational journeys and associated activities such as accommodation, transportation, and extracurriculars."

Example 2 (Ambiguous question within domain):
- User's Question: "Can you tell me about activities?"
- Model's Response: "Could you specify if you are referring to extracurricular activities, transportation-related programs, or accommodation services for children?"

"""

samples = """
Example 1 (Clear question with relevant information available):

User's Question: "What are the latest recommendations for handling sensitive data?"
Model's Response: (After analyzing the relevant documents) "The current recommendations for handling sensitive data include [specific response drawn from documents]."
Example 2 (Ambiguous question):

User's Question: "How should data be handled?"
Model's Response: "Could you clarify if you are referring to security, storage, or another aspect of data handling?"
Example 3 (No relevant information available):

User's Question: "What are the best practices for an uncovered topic?"
Model's Response: "I’m sorry, but I couldn’t find any relevant information in the provided documents regarding this topic."

"""

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2024-02-01",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Exemple d'utilisation
if __name__ == "__main__":

    print(f"Open qdrant client")
    client = QdrantClient(host="localhost", port=6333)

    print(f"Declare azure openAI Embeddings")
    embeddings = AzureOpenAIEmbeddings(model="text-embedding-ada-002")

    # points = client.scroll(
    #     collection_name="enfants",
    #     limit=5
    # )
    # print(points)
    # for point in points:
    #     print(f"ID: {point.id}, Payload: {point.payload}")


    # query_vector = embeddings.embed_query("Enfant2")  # Remplacez cela si vous avez une méthode différente pour obtenir le vecteur

    # search_results = client.search(
    #     collection_name="enfants",
    #     query_vector=query_vector,
    #     limit=5  # Nombre de résultats souhaité
    # )

    # # Afficher les résultats
    # for result in search_results:
    #     print(f"ID: {result.id}, Distance: {result.score}, Payload: {result.payload}")


    print(f"Init vector store")
    # vector_store = QdrantVectorStore.from_existing_collection(
    #     embedding=embeddings,
    #     collection_name="enfants",
    #     url="http://localhost:6333",
    # )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="enfants",
        embedding=embeddings,
        content_payload_key="payload"
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 20, "score_threshold": 0.2},
    )

    # print(f"Execute similarity search")
    # result = vector_store.similarity_search(query="Enfant2")
    # print(result)

    question = "Quel est le parcours scolaire de Enfant1, quel est son dernier logement?"
    print("")
    print(f"Execute retriever search")
    result = retriever.batch([question])
    print(result)


    print("")
    print(f"Execute rag chain")
    message = """
    Answer this question using the provided context only.

    {question}

    Context:
    {context}
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            ("human", message),
        ]
    )

    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

    result = rag_chain.invoke(question)
    print(result.content)