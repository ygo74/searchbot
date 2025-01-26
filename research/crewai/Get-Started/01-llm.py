from crewai import LLM
from dotenv import load_dotenv
from litellm import completion
import os


# Load the environment variables
load_dotenv()
print(os.getenv("AZURE_API_BASE"))

# messages
messages = [
    {
        "content": "Translate the following text to French: 'Hello, how are you?'",
        "role": "user"
    }
]

# azure call
# response = completion(
#     model = "azure/gpt-4o",
#     messages = messages
# )

# print(response)


# Advanced configuration with detailed parameters
llm = LLM(
    model="azure/gpt-4o",
    api_version="2024-06-01",
    temperature=0.7,        # Higher for more creative outputs
    timeout=120,           # Seconds to wait for response
    max_tokens=4000,       # Maximum length of response
    top_p=0.9,            # Nucleus sampling parameter
    frequency_penalty=0.1, # Reduce repetition
    presence_penalty=0.1,  # Encourage topic diversity
    # response_format={"type": "json"},  # For structured outputs
    seed=42               # For reproducible results
)

# Query the model
result = llm.call(messages)
print(result)
