from crewai import LLM
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task


from dotenv import load_dotenv
import os
import yaml
import logging

# Set logging level to debug
logging.basicConfig(level=logging.DEBUG)

# Load the environment variables
load_dotenv()
print(os.getenv("AZURE_API_BASE"))


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

# https://github.com/joserodr68/LLM-Toolbox/blob/main/backend/aux_crewai.py
# Define file paths for YAML configurations
files = {
    'agents': 'Get-Started/config/agents.yaml',
    'tasks': 'Get-Started/config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

print(tasks_config['research_task'])

# Creating Agents
web_search_agent = Agent(
    config=agents_config['researcher'],
    verbose=True,
    llm=llm

)

# Creating tasks
search_task = Task(
    config=tasks_config['research_task']
)



agents_crew = Crew(
    agents=[web_search_agent],
    tasks=[search_task],
    process=Process.sequential,
    verbose=True
)

result = agents_crew.kickoff(
    inputs={
        'topic': 'AI LLMs'
    }
)

print(result)

# # Define your agents
# researcher = Agent(
#     role="Researcher",
#     goal="Conduct thorough research and analysis on AI and AI agents",
#     backstory="You're an expert researcher, specialized in technology, software engineering, AI, and startups. You work as a freelancer and are currently researching for a new client.",
#     allow_delegation=False,
# )

# writer = Agent(
#     role="Senior Writer",
#     goal="Create compelling content about AI and AI agents",
#     backstory="You're a senior writer, specialized in technology, software engineering, AI, and startups. You work as a freelancer and are currently writing content for a new client.",
#     allow_delegation=False,
# )

# # Define your task
# task = Task(
#     description="Generate a list of 5 interesting ideas for an article, then write one captivating paragraph for each idea that showcases the potential of a full article on this topic. Return the list of ideas with their paragraphs and your notes.",
#     expected_output="5 bullet points, each with a paragraph and accompanying notes.",
#     agent=researcher
# )

# # Define the manager agent
# manager = Agent(
#     role="Project Manager",
#     goal="Efficiently manage the crew and ensure high-quality task completion",
#     backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
#     allow_delegation=True,
# )

# # Instantiate your crew with a custom manager
# crew = Crew(
#     # agents=[researcher, writer],
#     tasks=[task],
#     # manager_agent=manager,
#     # process=Process.hierarchical,
#     agents=[researcher],
#     process=Process.sequential,
#     verbose=True
# )

# # Start the crew's work
# result = crew.kickoff()
# print(result)