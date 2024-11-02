import pytest
from datasets import load_dataset
import random
from dotenv import load_dotenv
import psycopg2
from datetime import datetime
import yaml
import os
import logging

from unit_tests.lib.prompts_loading import load_yaml_files

# Configurer le logging
logging.basicConfig(level=logging.INFO)

# import opik

# Load environment variables from .venv
load_dotenv()

# opik.configure(use_local=True)

# Liste pour stocker les résultats des tests
test_results = []
pytest.llm_results = []


def pytest_addoption(parser):
    parser.addoption("--yaml_dir", action="store", default=".", help="chemin vers le répertoire contenant les fichiers YAML")
    parser.addoption("--file_pattern", action="store", default="*.yml", help="chemin vers le répertoire contenant les fichiers YAML")


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
    logging.debug(f"Prompts chargés : {prompts}")  # Débogage

    if "prompt_item" in metafunc.fixturenames:
        # Obtenir les échantillons de la fixture
        metafunc.parametrize("prompt_item", prompts)


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