import os
import fnmatch
import yaml
import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def find_files(directory, pattern):
    """Cherche tous les fichiers dans un répertoire donné qui correspondent à un motif.

    Args:
        directory (str): Le chemin du répertoire dans lequel chercher.
        pattern (str): Le motif à utiliser pour filtrer les fichiers.

    Returns:
        list: Une liste de chemins de fichiers qui correspondent au motif.
    """
    matched_files = []

    # Parcourir tous les fichiers et sous-répertoires dans le répertoire donné
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            # Créer le chemin complet du fichier et l'ajouter à la liste
            matched_files.append(os.path.join(root, filename))

    return matched_files

def load_yaml_files(directory, pattern):
    """Charge tous les fichiers YAML d'un répertoire donné.

    Args:
        directory (str): Le chemin du répertoire à charger.

    Returns:
        list: Une liste de dictionnaires contenant les données YAML.
    """

    logging.debug(f"Chargement des fichiers YAML de {directory} avec le motif {pattern}")
    yaml_files = find_files(directory, pattern)
    logging.debug(f"Found files {yaml_files}")
    loaded_data = []

    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)  # Charger le contenu YAML
            if "prompts" in data:
                loaded_data.extend(data["prompts"])

    return loaded_data

def extract_names(prompts):
    """extract name attributes from the prompts"""
    return [prompt["name"] for prompt in prompts if "name" in prompt]

# Exemple d'utilisation
if __name__ == "__main__":
    directory_to_search = "./research/evaluation/dataset"  # Remplacez par votre chemin

    # Charger les fichiers YAML
    yaml_data = load_yaml_files(directory_to_search, "*.yml")

    # Afficher les données chargées
    for data in yaml_data:
        print(data)
