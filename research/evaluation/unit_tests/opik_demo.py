from dotenv import load_dotenv

import opik

# Load environment variables from .venv
load_dotenv()

# import os

# os.environ["OPIK_BASE_URL"] = "http://localhost:5173"
# os.environ["OPIK_PROJECT_NAME"] = "openai-integration-demo"


opik.configure(use_local=True)
