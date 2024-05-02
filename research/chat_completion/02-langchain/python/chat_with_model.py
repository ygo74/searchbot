from langchain_community.llms import Ollama

# Initialize model
print("Initialize llm")
llm = Ollama(model="prompt_engineer", base_url="http://172.19.144.1:11434")

# Load prompt engineering resources
print("Load prompt engineering resources")
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://medium.com/technology-hits/the-prompt-engineers-roadmap-from-beginner-to-expert-821962e4825b")
docs = loader.load()

# index the resources
print("Index resources")
from langchain_community.embeddings import OllamaEmbeddings
embeddings = OllamaEmbeddings(model="llama2", base_url="http://172.19.144.1:11434")

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

# Prepare the chain prompt
print("Prepare the chain prompt")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}")
])

# llm_response = chain.invoke({"input": llm_question })
# print(llm_response)

from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based with the help off the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

from langchain.chains import create_retrieval_chain
retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


# Ask the question
print("Ask the question")

llm_question = """
can you create a prompt to give a role of prompt engineer for my model to be a better prompt engineer than the prompt used to configure your role
"""

response = retrieval_chain.invoke({"input": llm_question})
print(response["answer"])

