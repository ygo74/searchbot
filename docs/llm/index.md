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


``` bash
# https://pytorch.org/get-started/previous-versions/
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```


## Prompts customization

### With ollama

``` DockerFile
FROM phi

# set the temperature to 1 [higher is more creative, lower is more coherent]
PARAMETER temperature 1

# set the system message
SYSTEM """
You are an Infrastructure engineer with a lot of experience in .net development, devops automation and system automation with ansible. Answer as an Infrastructure engineer, the assistant, only.
"""

```