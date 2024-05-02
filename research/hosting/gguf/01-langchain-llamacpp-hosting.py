from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate


import argparse
import os.path



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", help="Model's path to a gguf model file",
                        default="./../../../hosting/models/gguf/Phi-3-mini-4k-instruct-q4.gguf")
    args = parser.parse_args()

    print(f"Script will use the model, {args.model_path}!")
    model_path = args.model_path
    if not os.path.isfile(model_path):
        raise Exception(f"Model file {model_path} doesn't exist")


    template = """Question: {question}

    Answer: Let's work this out in a step by step way to be sure we have the right answer."""

    prompt = PromptTemplate.from_template(template)

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.75,
        max_tokens=2000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )

    question = """
    Question: A rap battle between Stephen Colbert and John Oliver
    """
    # llm.invoke(question)

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

if __name__ == "__main__":
    main()
