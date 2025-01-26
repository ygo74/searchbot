import yaml
from .llm import llm

# importing output agent models
from models.document_planner import DocPlan, DocItem

# Importing Crew related components
from crewai import Agent, Task, Crew


# Create the crew
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
)

# Load agent and task configurations from YAML files
with open('config/planner_agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/planner_tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

code_explorer = Agent(
    config=agents_config['code_explorer'],
    tools=[
        DirectoryReadTool(),
        FileReadTool()
    ],
    llm=llm,
    verbose=True
)
documentation_planner = Agent(
    config=agents_config['documentation_planner'],
    tools=[
        DirectoryReadTool(),
        FileReadTool()
    ],
    llm=llm,
    verbose=True

)

analyze_codebase = Task(
    config=tasks_config['analyze_codebase'],
    agent=code_explorer,
    verbose=True

)
create_documentation_plan = Task(
    config=tasks_config['create_documentation_plan'],
    agent=documentation_planner,
    output_pydantic=DocPlan,
    verbose=True
)

planning_crew = Crew(
    agents=[code_explorer, documentation_planner],
    tasks=[analyze_codebase, create_documentation_plan],
    verbose=False
)
