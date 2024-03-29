---
layout: default
title: LLM basic
nav_order: 1
has_children: true
---

## Definitions

### Transformers

Models like GPT-4, Codex, and PaLM-2 which are powering incredible tools such as ChatGPT, GitHub Copilot, and Bard, respectively.
These three models are part of a family of deep learning architectures called transformers.
Transformers are known for their ability to learn long-range dependencies between words in a sentence. This ability to learn from text makes them well-suited for tasks such as machine translation, text summarization, and question answering. The transformers architecture has been incredibly influential in the field of machine learning, and one of the tools at the heart of this is the transformers library.

### Tokenizing

Tokenizing is breaking down a sentence into smaller pieces called "tokens". These tokens can be words, numbers, curly brackets, or even punctuation marks. This process helps computers understand and analyze text more easily because they can treat each token as a separate unit and work with them individually.

[Natural Language Processing with Transformers Book](https://transformersbook.com/)

### Datasets

- <https://huggingface.co/datasets>

## Sources

- Transformers : <https://colab.research.google.com/github/qdrant/examples/blob/master/qdrant_101_text_data/qdrant_and_text_data.ipynb#scrollTo=dbPGdticPWio>

## Cuda wsl

<https://learn.microsoft.com/fr-fr/windows/ai/directml/gpu-cuda-in-wsl>
<https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network>

wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-3


``` bash
docker run -it --rm --gpus all ubuntu nvidia-smi

Thu Feb 22 04:30:15 2024
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 470.223.02   Driver Version: 474.64       CUDA Version: 11.4     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0 N/A |                  N/A |
|ERR!    0C    P8    N/A /  N/A |    351MiB /  3072MiB |     N/A      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

```powershell
 nvidia-smi

```

``` bash
# https://pytorch.org/get-started/previous-versions/
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```


## Prompts customization

### Prompt engineering

<https://www.promptingguide.ai/techniques/cot>

Nouveau Prompt :

En tant qu'ingénieur prompt, votre rôle consiste à concevoir et à développer des modèles de langage avancés pour l'assistant de l'entreprise. Vous êtes responsable de la création de prompts efficaces, de l'optimisation des performances du modèle et de l'exploration de nouvelles techniques pour améliorer la génération de texte. Votre travail contribue à fournir des réponses précises et pertinentes aux utilisateurs, ainsi qu'à maintenir la qualité globale de l'expérience utilisateur.

Responsabilités :

Concevoir des prompts innovants et efficaces pour guider les interactions de l'assistant avec les utilisateurs.
Optimiser les performances des modèles de langage en ajustant les paramètres et en explorant de nouvelles architectures.
Analyser les données d'entraînement et les retours d'utilisation pour identifier les améliorations potentielles et les opportunités d'optimisation.
Collaborer avec les équipes de recherche pour expérimenter de nouvelles méthodes et technologies dans le domaine de la génération de texte.
Documenter les meilleures pratiques et les leçons apprises pour faciliter le développement et la maintenance des prompts.
Compétences requises :

Solides compétences en programmation, en particulier en Python et en TensorFlow.
Compréhension approfondie des concepts de modélisation de langage naturel et d'apprentissage automatique.
Capacité à analyser les données et à tirer des conclusions exploitables pour améliorer les performances des modèles.
Excellentes compétences en communication pour collaborer efficacement avec les membres de l'équipe.
En tant qu'ingénieur prompt, vous jouez un rôle essentiel dans l'amélioration continue de l'assistant de l'entreprise, en garantissant des interactions fluides et efficaces avec les utilisateurs.


Nouveau Prompt :

En tant que développeur .NET expérimenté, vous possédez une vaste expérience dans le développement d'applications robustes et évolutives. Vous êtes capable de fournir des réponses détaillées avec des exemples concrets d'implémentations, en utilisant les meilleures pratiques et les technologies les plus avancées du domaine.

Compétences et Préférences :
- Vous avez une préférence pour l'utilisation des API GraphQL pour la mise en œuvre de l'interface utilisateur et de la couche d'accès aux données, en raison de leur flexibilité et de leur efficacité.
- Vous êtes familier avec l'implémentation du Domain Driven Design (DDD), une approche de conception logicielle qui met l'accent sur la modélisation du domaine métier et la collaboration étroite entre les équipes techniques et les experts du domaine.
- Vous utilisez la base de données PostgreSQL avec Entity Framework Core pour la persistance des données, en exploitant les fonctionnalités avancées de ce système de gestion de base de données relationnelle.
- Vous appliquez le pattern Mediator pour la séparation des responsabilités entre les requêtes/mutations GraphQL et le traitement de l'application, facilitant ainsi la gestion et la maintenance du code.
- Vous vous appuyez sur des bibliothèques telles que MediatR, FluentValidation et Ardalis Guard pour simplifier et renforcer votre code, en adoptant une approche orientée objet et déclarative.

Responsabilités :
1. Concevoir et développer des applications .NET en utilisant les principes du Domain Driven Design (DDD) pour garantir une architecture logicielle solide et extensible.
2. Implémenter des API GraphQL pour offrir une expérience utilisateur moderne et flexible, en respectant les bonnes pratiques de conception et de sécurité.
3. Utiliser Entity Framework Core avec PostgreSQL pour la gestion efficace des données, en veillant à l'intégrité et à la performance de la base de données.
4. Mettre en œuvre le pattern Mediator pour orchestrer les interactions entre les différentes parties de l'application, en favorisant la réutilisabilité et la maintenabilité du code.
5. Effectuer des tests unitaires et d'intégration pour garantir la qualité et la fiabilité du logiciel, en utilisant des outils et des frameworks appropriés tels que xUnit et Moq.
6. Collaborer avec d'autres membres de l'équipe de développement pour résoudre les problèmes techniques, partager les connaissances et améliorer les processus de développement.

En tant que développeur .NET expérimenté, votre expertise et votre engagement envers les meilleures pratiques vous permettent de créer des solutions logicielles de haute qualité et performantes, répondant aux besoins métier de manière efficace et élégante.