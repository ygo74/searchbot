import os
from dotenv import load_dotenv
import asyncio
import argparse
import logging
import yaml

# Set logging level to debug
# logging.basicConfig(level=logging.DEBUG)


def main():

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--code_path", help="code path", required=True)
    args = parser.parse_args()

    code_path = args.code_path
    # Check if code path exists
    if not os.path.exists(code_path):
        raise FileNotFoundError(f"Code path {code_path} not found")

    # Load the environment variables
    load_dotenv()

    from agents.documentation_flow import CreateDocumentationFlow

    flow = CreateDocumentationFlow(repo_path=code_path)
    flow.kickoff()

if __name__ == "__main__":
    main()
