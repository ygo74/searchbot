import pytest
from datasets import load_dataset
import random
from dotenv import load_dotenv

# import opik

# Load environment variables from .venv
load_dotenv()

# opik.configure(use_local=True)



def get_data_for_tests():
    # Charger le dataset SQuAD depuis Hugging Face
    dataset = load_dataset("squad", split="validation")

    # Sélectionner 10 exemples aléatoires
    random_samples = random.sample(list(dataset), 2)

    return random_samples

@pytest.fixture(scope="class")
def dataset_item(request):
    class DummyDB:
        pass

# Utiliser un hook pour paramétrer les tests avec les échantillons
def pytest_generate_tests(metafunc):
    if "sample" in metafunc.fixturenames:
        # Obtenir les échantillons de la fixture
        samples = get_data_for_tests()
        metafunc.parametrize("sample", samples)
    elif "dataset_item" in metafunc.fixturenames:
        samples = get_data_for_tests()
        metafunc.parametrize("dataset_item", samples)


def pytest_runtest_logreport(report):
    if report.when == "call":
        print(f"{report.nodeid} - {report.outcome} - {report.duration}")