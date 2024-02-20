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