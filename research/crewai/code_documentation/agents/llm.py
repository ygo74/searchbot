import os
from crewai import LLM
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction


# init LLM
llm = LLM(
    model="azure/gpt-4o",
    api_version="2024-06-01",
    temperature=0.7,        # Higher for more creative outputs
    timeout=120,           # Seconds to wait for response
    max_tokens=16384,       # Maximum length of response
    top_p=0.9,            # Nucleus sampling parameter
    frequency_penalty=0.1, # Reduce repetition
    presence_penalty=0.1,  # Encourage topic diversity
    # response_format={"type": "json"},  # For structured outputs
    seed=42               # For reproducible results
)

embedder = {
    "provider": "azure_openai",
    "config": {
        "api_key": os.getenv("AZURE_API_KEY"),
        # "api_version": os.getenv('AZURE_API_VERSION'),
        "api_base": os.getenv('AZURE_API_BASE'),
        # "api_type": 'azure_openai',
        "model": "text-embedding-ada-002"
    },
}
