---
layout: default
parent: Addresses validator
title: Address parser
nav_order: 1
has_children: false
---


## Goal

## Tools

### Libpostal

sources :

- <https://github.com/openvenues/libpostal>
- Binding python : <https://github.com/openvenues/pypostal>

Installation:

1. Prerequisites

    ``` bash
    sudo apt-get install curl autoconf automake libtool python-dev-is-python3 pkg-config

    ```

2. Installation from github

    ``` bash
    git clone https://github.com/openvenues/libpostal
    cd libpostal
    ./bootstrap.sh
    ./configure --datadir=[...some dir with a few GB of space...]
    make
    sudo make install

    # On Linux it's probably a good idea to run
    sudo ldconfig
    ```

3. Installation

    ``` bash
    python -m venv ./venv/linuv_venv_libpostal
    . ./venv/linuv_venv_libpostal/bin/activate

    ```

## Sample

