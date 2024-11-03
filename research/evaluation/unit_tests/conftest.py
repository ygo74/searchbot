import pytest
from datasets import load_dataset
import random
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import yaml
import os
import logging
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from unit_tests.lib.prompts_loading import load_yaml_files, extract_names
from unit_tests.lib.database import setup_database

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# import opik

# Load environment variables from .venv
load_dotenv()

# opik.configure(use_local=True)

# Liste pour stocker les résultats des tests
test_results = []
pytest.llm_results = {}


def pytest_addoption(parser):
    parser.addoption("--yaml_dir", action="store", default=".", help="chemin vers le répertoire contenant les fichiers YAML")
    parser.addoption("--file_pattern", action="store", default="*.yml", help="chemin vers le répertoire contenant les fichiers YAML")
    parser.addoption("--assistant_definition", action="store", default="*.yml", help="path to the assistant definition")
    parser.addoption("--assistant_name", action="store", default="", help="Assistant name")
    parser.addoption("--prompt_name", action="store", default="", help="specific prompt to test")


def pytest_sessionstart(session):
    """Hook executed at the start of the test session."""
    print("Starting Pytest session...")
    # Code de configuration, par exemple :
    # Connexion à une base de données, chargement de configurations, etc.
    # setup_database()


def get_data_for_tests():
    # Charger le dataset SQuAD depuis Hugging Face
    dataset = load_dataset("squad", split="validation")

    # Sélectionner 10 exemples aléatoires
    random_samples = random.sample(list(dataset), 2)

    return random_samples

# Connexion à PostgreSQL
def get_db_connection():

    dbname = os.getenv("DATABASE_NAME")
    dbserver = os.getenv("DATABASE_SERVER")
    dbuser = os.getenv("DATABASE_USERNAME")
    dbpassword = os.getenv("DATABASE_PASSWORD")

    logging.info(f"Open database {dbname} on server {dbserver} with user {dbuser}")

    return psycopg2.connect(
        dbname=dbname,
        user=dbuser,
        password=dbpassword,
        host=dbserver
    )

# Enregistrer les résultats du test
def save_test_result(test_name, status, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_results (test_name, status, message, timestamp)
        VALUES (%s, %s, %s, %s)
    """, (test_name, status, message, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

# Utiliser un hook pour paramétrer les tests avec les échantillons
def pytest_generate_tests(metafunc):

    # Load prompts
    yaml_dir = metafunc.config.getoption("yaml_dir")
    file_pattern = metafunc.config.getoption("file_pattern")
    prompts = load_yaml_files(yaml_dir, file_pattern)

    if metafunc.config.getoption("prompt_name") != "":
        prompts = [prompt_item for prompt_item in prompts if prompt_item["name"] == metafunc.config.getoption("prompt_name")]

    logging.debug(f"Prompts chargés : {prompts}")  # Débogage

    if "prompt_item" in metafunc.fixturenames:
        # Obtenir les échantillons de la fixture
        metafunc.parametrize("prompt_item", prompts)
    elif "prompt_name" in metafunc.fixturenames:
        metafunc.parametrize("prompt_name", extract_names(prompts))


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    if report.when == "call":
        print(f"{report.nodeid} - {report.outcome} - {report.duration}")
        test_name = report.nodeid
        status = "PASSED" if report.passed else "FAILED"
        message = report.longreprtext if report.failed else ""
        test_results.append((test_name, status, message))
        save_test_result(test_name, status, message)

def pytest_sessionfinish(session, exitstatus):
    print("\n===== Résumé des tests =====")
    for test_name, status, message in test_results:
        print(f"Test: {test_name} - Statut: {status}")
        if message:
            print(f"Message d'erreur:\n{message}\n")

    print("===== Fin du résumé des tests =====")

    for key, value in pytest.llm_results.items():
        print(value)


@pytest.fixture(scope="session")
def llm_chain(request):

    # load assistant definition
    assistant_name = request.config.getoption("assistant_name")
    if assistant_name == "":
        pytest.fail(f"Assistant name not defined", pytrace=False)

    assistant_file_path = request.config.getoption("assistant_definition")
    # check file exists
    if not os.path.isfile(assistant_file_path):
        pytest.fail(f"Assistant defintion file '{assistant_file_path}' doesn't exist", pytrace=False)

    # Lire le fichier YAML pour extraire la configuration
    with open(assistant_file_path, 'r', encoding='utf-8') as file:
        assistant_config = yaml.safe_load(file)

    if "system_prompt" not in assistant_config:
        pytest.fail(f"system prompt (key=system_prompt) not defined in '{assistant_file_path}'", pytrace=False)



    llm = AzureChatOpenAI(
        azure_deployment = assistant_config["deployment_model"] if "deployment_model" in assistant_config else "gpt-4o",
        api_version = assistant_config["azure_ai_version"] if "azure_ai_version" in assistant_config else "2024-02-01",
        temperature= assistant_config["temperature"] if "temperature" in assistant_config else 0,
        max_tokens=assistant_config["max_tokens"] if "max_tokens" in assistant_config else None,
        timeout=None,
        max_retries=2
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", assistant_config["system_prompt"]),
            ("human", "{user_prompt}"),
        ]
    )

    chain = prompt | llm

    return chain
