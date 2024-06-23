---
layout: default
parent: Vectors databases
title: Milvus
nav_order: 2
has_children: true

---


## Development deployment

### Docker images

- quay.io/coreos/etcd:v3.5.5

  - description : globally distributed key-value store

- minio/minio:RELEASE.2023-03-20T20-16-18Z

  - source : <https://github.com/minio/minio>{:target="_blank"}
  - description : MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service

- milvusdb/milvus:v2.3.0

  - source : <https://github.com/milvus-io/milvus>{:target="_blank"}
  - description : Milvus is an open-source vector database built to power embedding similarity search and AI applications

### Milvius development docker images

- quay.io/coreos/etcd:v3.5.5

  - description : globally distributed key-value store

- apachepulsar/pulsar:2.8.2

  - source : <https://pulsar.apache.org/>{:target="_blank"}
  - description : Apache Pulsar is an all-in-one messaging and streaming platform

- minio/minio:RELEASE.2023-03-20T20-16-18Z

  - source : <https://github.com/minio/minio>{:target="_blank"}
  - description : MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service

- mcr.microsoft.com/azure-storage/azurite

  - source : <https://hub.docker.com/_/microsoft-azure-storage-azurite>{:target="_blank"}
  - description : Azurite is an open source Azure Storage API compatible server (emulator). Based on Node.js, Azurite provides cross platform experiences for customers wanting to try Azure Storage easily in a local environment. Azurite simulates most of the commands supported by Azure Storage with minimal dependencies.

- jaegertracing/all-in-one:latest

  - source : <https://www.jaegertracing.io/>{:target="_blank"}
  - description : Distributed tracing observability platforms

- wurstmeister/zookeeper:latest

  - source : <https://zookeeper.apache.org/>{:target="_blank"}
  - description : ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. All of these kinds of services are used in some form or another by distributed applications



## Get started

- <https://milvus.io/blog/how-to-get-started-with-milvus.md>{:target="_blank"}

- python client : <https://github.com/zilliztech/milvus_cli>{:target="_blank"}
