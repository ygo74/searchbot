from typing import List
from pydantic import BaseModel
from pathlib import Path
# Importing CrewAI Flow related components
from crewai.flow.flow import Flow, listen, start

from .planning_agents import planning_crew
from .documentation_agents import documentation_crew

class DocumentationState(BaseModel):
    """
    State for the documentation flow
    """
    repo_path: Path = Path("./")
    docs: List[str] = []

class CreateDocumentationFlow(Flow[DocumentationState]):

    # add constructor to initialize the state with repo_path
    def __init__(self, repo_path: Path):
        super().__init__()
        self.state.repo_path = repo_path

    # Clone the repository, initial step
    # No need for AI Agents on this step, so we just use regular Python code

    @start()
    def plan_docs(self):
        print(f"# Planning documentation for: {self.state.repo_path}\n")
        result = planning_crew.kickoff(inputs={'repo_path': self.state.repo_path})
        print(f"# Planned docs for {self.state.repo_path}:")
        for doc in result.pydantic.docs:
            print(f"    - {doc.title}")
        return result

    @listen(plan_docs)
    def save_plan(self, plan):
        with open("docs/plan.json", "w") as f:
            f.write(plan.raw)

    @listen(plan_docs)
    def create_docs(self, plan):
        for doc in plan.pydantic.docs:
            print(f"\n# Creating documentation for: {doc.title}")
            result = documentation_crew.kickoff(inputs={
                'repo_path': self.state.repo_path,
                'title': doc.title,
                'overview': plan.pydantic.overview,
                'description': doc.description,
                'prerequisites': doc.prerequisites,
                'examples': '\n'.join(doc.examples),
                'goal': doc.goal
            })

            # Save documentation to file in docs folder
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)
            title = doc.title.lower().replace(" ", "_") + ".mdx"
            self.state.docs.append(str(docs_dir / title))
            with open(docs_dir / title, "w") as f:
                f.write(result.raw)

        print(f"\n# Documentation created for: {self.state.repo_path}")