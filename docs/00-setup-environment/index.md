---
layout: default
title: Setup environment
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

## Cuda wsl

sources :

- <https://learn.microsoft.com/fr-fr/windows/ai/directml/gpu-cuda-in-wsl>{:target="_blank"}
- <https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network>{:target="_blank"}

1. Update windows driver to latest version

    ```powershell
    nvidia-smi

    Sat Apr 20 09:16:07 2024
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 474.82       Driver Version: 474.82       CUDA Version: 11.4     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name            TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ... WDDM  | 00000000:01:00.0 N/A |                  N/A |
    | 20%    0C    P8    N/A /  N/A |    165MiB /  3072MiB |     N/A      Default |
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

1. Install Cuda toolkit

    ``` bash
    wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-12-3
    ```

1. Check gpu detection

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

## Jupyter notebook

1. Python

    Source : <https://docs.jupyter.org/en/latest/running.html>{:target="_blank"}

    ``` bash
    pip3 install --upgrade pip
    pip3 install jupyter
    ```

1. dotnet

    Source : <https://github.com/dotnet/interactive>{:target="_blank"}

    ``` bash
    # Install dotnet-sdk
    sudo apt-get update && \
    sudo apt-get install -y dotnet-sdk-8.0

    # Install dotnet interactive
    dotnet tool install -g Microsoft.dotnet-interactive

    # Install Jupyter
    dotnet interactive jupyter install

    ```

## Local environment

1. Install Azure AI Services

## Cloning models with git

1. Requires [git-lfs](https://git-lfs.com/){:target="_blank"}

1. Add "C:\Program Files\Git LFS" in the path

## WSL Ubuntu

``` bash
# Get list of installed packages
sudo apt list --installed
```

``` bash
# Get details of installed package
sudo apt show poppler-utils
```

## Langsmith

- <https://www.langchain.com/langsmith>{:target="_blank"}

LangSmith is a unified DevOps platform for developing, collaborating, testing, deploying, and monitoring LLM applications.
New Pricing:
All free accounts will be rate limited to 5k traces per month starting on July 1st. To avoid this, sign up for our paid plans


- <https://smith.langchain.com/>{:target="_blank"}
