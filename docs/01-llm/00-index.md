---
layout: default
title: LLM basic
nav_order: 1
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

- SentenceTransformers Documentation : https://www.sbert.net/

  SentenceTransformers is a Python framework for state-of-the-art sentence, text and image embeddings
  You can use this framework to compute sentence / text embeddings for more than 100 languages. These embeddings can then be compared e.g. with cosine-similarity to find sentences with a similar meaning. This can be useful for semantic textual similarity, semantic search, or paraphrase mining.

  https://www.sbert.net/docs/pretrained_models.html


### Tokenizing

Tokenizing is breaking down a sentence into smaller pieces called "tokens". These tokens can be words, numbers, curly brackets, or even punctuation marks. This process helps computers understand and analyze text more easily because they can treat each token as a separate unit and work with them individually.

[Natural Language Processing with Transformers Book](https://transformersbook.com/)

### Datasets

- <https://huggingface.co/datasets>

## Sources

- Transformers : <https://colab.research.google.com/github/qdrant/examples/blob/master/qdrant_101_text_data/qdrant_and_text_data.ipynb#scrollTo=dbPGdticPWio>


``` bash
# https://pytorch.org/get-started/previous-versions/
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu118
```
