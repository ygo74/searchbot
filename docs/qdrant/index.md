---
layout: default
title: Qdrant
nav_order: 2
has_children: true
---


## Development deployment

### Docker images

``` bash
docker pull qdrant/qdrant
```
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
``` bash
docker pull qdrant/qdrant
```

url : http://localhost:6333/dashboard

## Get started

https://docs.jupyter.org/en/latest/running.html

``` bash

pip3 install --upgrade pip
pip3 install jupyter

```



<https://qdrant.tech/documentation/quick-start/>

- python client : https://python-client.qdrant.tech/
- dotnet client :

### Pyhton

``` bash
python3 -m venv ./qdrant_linux_venv
pip3 install jupyter

```

### dotnet

sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0

dotnet tool install -g Microsoft.dotnet-interactive

dotnet interactive jupyter install

https://github.com/dotnet/interactive


## LLM frameworks

- SentenceTransformers Documentation : https://www.sbert.net/

  SentenceTransformers is a Python framework for state-of-the-art sentence, text and image embeddings
  You can use this framework to compute sentence / text embeddings for more than 100 languages. These embeddings can then be compared e.g. with cosine-similarity to find sentences with a similar meaning. This can be useful for semantic textual similarity, semantic search, or paraphrase mining.

  https://www.sbert.net/docs/pretrained_models.html