---
layout: default
parent: Vectors databases
title: Qdrant
nav_order: 1
has_children: true
---


## Development deployment

### Docker images

``` bash
# Get the latest image
docker pull qdrant/qdrant

# interactive run
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```

Endpoints :

- management console : <http://localhost:6333/dashboard>{:target="_blank"}

## Get started

### Install python packages

``` bash
pip3 install --upgrade pip
pip install qdrant-client
```

<https://qdrant.tech/documentation/quick-start/>{:target="_blank"}

- python client : <https://python-client.qdrant.tech/>{:target="_blank"}
- dotnet client :

### qdrant client

- <https://github.com/qdrant/qdrant-client>{:target="_blank"}

### langchain integration

- <https://python.langchain.com/docs/integrations/providers/qdrant/>{:target="_blank"}

### Fastembed

- <https://github.com/qdrant/fastembed>{:target="_blank"}

### samples

- <https://github.com/qdrant/qdrant-markdown-indexer>{:target="_blank"}
