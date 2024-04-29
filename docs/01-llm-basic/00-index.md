---
layout: default
title: LLM basic
nav_order: 2
has_children: true
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>


## Definitions

### Transformers

Models like GPT-4, Codex, and PaLM-2 which are powering incredible tools such as ChatGPT, GitHub Copilot, and Bard, respectively.
These three models are part of a family of deep learning architectures called transformers.
Transformers are known for their ability to learn long-range dependencies between words in a sentence. This ability to learn from text makes them well-suited for tasks such as machine translation, text summarization, and question answering. The transformers architecture has been incredibly influential in the field of machine learning, and one of the tools at the heart of this is the transformers library.

- SentenceTransformers Documentation : <https://www.sbert.net/>{:target="_blank"}

  SentenceTransformers is a Python framework for state-of-the-art sentence, text and image embeddings
  You can use this framework to compute sentence / text embeddings for more than 100 languages. These embeddings can then be compared e.g. with cosine-similarity to find sentences with a similar meaning. This can be useful for semantic textual similarity, semantic search, or paraphrase mining.

  <https://www.sbert.net/docs/pretrained_models.html>{:target="_blank"}


### Tokenizing

Tokenizing is breaking down a sentence into smaller pieces called "tokens". These tokens can be words, numbers, curly brackets, or even punctuation marks. This process helps computers understand and analyze text more easily because they can treat each token as a separate unit and work with them individually.

[Natural Language Processing with Transformers Book](https://transformersbook.com/){:target="_blank"}

### Datasets

- <https://huggingface.co/datasets>{:target="_blank"}

### GGUF

GGUF (Graphical Generic Unified Format) is a format designed to facilitate efficient inference of large language models (LLMs). It provides a unified structure for representing the weights and layers of LLMs. GGUF files are typically binary and not human-readable.

### Quantization

Quantization is a model compression technique that converts the weights and activations of a Large Language Model (LLM) from a high-precision data representation to a lower-precision one, meaning from a data type capable of holding more information to one that holds less. In other words, it allows transitioning from continuous infinite values to a more restricted set of discrete and finite values

By default the parameters in Large Language Models are represented with 32-bit floating numbers. However, the GGML library can convert it into a 16-bit floating point representation thus reducing the memory requirement by 50%  to load & run the LLM

GGML library also supports integer quantization (e.g. 4-bit, 5-bit, 8-bit, etc.) that can further reduce the memory and compute power required to run LLMs locally on the end user’s system or edge devices.

## Sources

- Transformers : <https://colab.research.google.com/github/qdrant/examples/blob/master/qdrant_101_text_data/qdrant_and_text_data.ipynb#scrollTo=dbPGdticPWio>{:target="_blank"}


``` bash
# https://pytorch.org/get-started/previous-versions/
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```
