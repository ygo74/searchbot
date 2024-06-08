---
layout: default
parent: Semantic Kernel
title: Memory Kernel
nav_order: 1
has_children: false
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Sources

- <https://github.com/microsoft/kernel-memory/tree/main>
- <https://microsoft.github.io/kernel-memory/>

## Execution environment

### Kernel Memory Service configuration

1.

### Docker

1. Create network

    ``` powershell
    docker network create kmnet
    ```

2. Start Qdrant

    ``` bash
    docker run --rm -it \
               -p 6333:6333 -p 6334:6334 \
               -v $(pwd)/qdrant_storage:/qdrant/storage:z \
               --network kmnet \
               --name qdrant \
               qdrant/qdrant

    ```

3. Start RabbitMQ

    ``` bash
    docker run -it --rm \
               -p 5672:5762 -p 15672:15672 \
               --name rabbitmq \
               --network kmnet \
               rabbitmq:3-management-alpine

    ```

4. Start Kernel Memory services

    ``` powershell
    docker run -it --rm `
               -v .\kernel-memory\service\Service\appsettings.Development.json:/app/appsettings.Production.json `
               -p 9001:9001 `
               --network kmnet `
               kernelmemory/service

    ```

### Docker compose

``` bash
docker compose -f docker-compose.yml up -d
```

{: .note }
> If services doesn't start, you can check the health state logs
>
> ``` bash
> docker inspect --format "{{json .State.Health }}" backends-rabbitmq-1
> ```
