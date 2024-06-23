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

Sources :

- <https://python.langchain.com/docs/integrations/providers/qdrant/>{:target="_blank"}
- <https://python.langchain.com/v0.2/docs/integrations/vectorstores/qdrant/>{:target="_blank"}

``` powershell
pip install langchain-qdrant langchain-openai langchain langchain-community
```

### Fastembed

Sources :

- <https://github.com/qdrant/fastembed>{:target="_blank"}
- <https://qdrant.tech/articles/fastembed/>{:target="_blank"}


FastEmbed is a lightweight, fast, Python library built for embedding generation.
FastEmbed is a lightweight library with few external dependencies. It doesn't require a GPU and doesn't download GBs of PyTorch dependencies, and instead use the ONNX Runtime.

{: .note }
> The ONNX Runtime is faster than PyTorch
> FastEmbed uses data-parallelism for encoding large datasets
> FastEmbed is better than OpenAI Ada-002

``` powershell
pip install qdrant-client[fastembed]

## A module that was compiled using NumPy 1.x cannot be run in NumPy 2.0.0 as it may crash. To support both 1.x and 2.x versions of NumPy, modules must be compiled with NumPy 2.0.
# Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

# If you are a user of the module, the easiest solution will be to downgrade to 'numpy<2' or try to upgrade the affected module.
# We expect that some modules will need time to support NumPy 2.
pip install numpy==1.26.4
```

### samples

- <https://github.com/qdrant/qdrant-markdown-indexer>{:target="_blank"}
