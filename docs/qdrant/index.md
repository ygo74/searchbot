---
layout: default
title: Qdrant
nav_order: 2
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

- management console : http://localhost:6333/dashboard

## Get started

### Install python packages

``` bash
pip3 install --upgrade pip
pip install qdrant-client
```

<https://qdrant.tech/documentation/quick-start/>

- python client : https://python-client.qdrant.tech/
- dotnet client :

### langchain integration

https://python.langchain.com/docs/integrations/providers/qdrant/

###

https://github.com/qdrant/qdrant-markdown-indexer
