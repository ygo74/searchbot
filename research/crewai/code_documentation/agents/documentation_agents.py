import yaml
from .llm import llm, embedder

# importing output agent models
from models.document_planner import DocPlan, DocItem

# Importing Crew related components
from crewai import Agent, Task, Crew
from crewai.tasks import TaskOutput
import re

def check_mermaid_syntax(task_output: TaskOutput):
    text = task_output.raw

    # Find all mermaid code blocks in the text
    mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', text, re.DOTALL)

    for block in mermaid_blocks:
        diagram_text = block.strip()
        lines = diagram_text.split('\n')
        corrected_lines = []

        for line in lines:
            corrected_line = re.sub(r'\|.*?\|>', lambda match: match.group(0).replace('|>', '|'), line)
            corrected_lines.append(corrected_line)

        text = text.replace(block, "\n".join(corrected_lines))

    task_output.raw = text
    return (True, task_output)

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    WebsiteSearchTool
)

# Load agent and task configurations from YAML files
with open('config/documentation_agents.yaml', 'r') as f:
    agents_config = yaml.safe_load(f)

with open('config/documentation_tasks.yaml', 'r') as f:
    tasks_config = yaml.safe_load(f)

overview_writer = Agent(
    config=agents_config['overview_writer'],
    tools=[
        DirectoryReadTool(),
        FileReadTool(),
        WebsiteSearchTool(
            website="https://mermaid.js.org/intro/",
            config=dict(
                embedder=embedder
            )
        )
    ],
    llm=llm
)

documentation_reviewer = Agent(
    config=agents_config['documentation_reviewer'],
    tools=[
        DirectoryReadTool(directory="docs/", name="Check existing documentation folder"),
        FileReadTool(),
    ],
    llm=llm
)

draft_documentation = Task(
  config=tasks_config['draft_documentation'],
  agent=overview_writer
)

qa_review_documentation = Task(
  config=tasks_config['qa_review_documentation'],
  agent=documentation_reviewer,
  guardrail=check_mermaid_syntax,
  max_retries=5
)

documentation_crew = Crew(
    agents=[overview_writer, documentation_reviewer],
    tasks=[draft_documentation, qa_review_documentation],
    verbose=False
)