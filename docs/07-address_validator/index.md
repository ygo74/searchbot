---
layout: default
title: Addresses validator
nav_order: 7
has_children: false
---

## Environment

### PostGIS

source : <https://postgis.net/documentation/getting_started/>

Docker image : <https://hub.docker.com/r/postgis/postgis>

``` bash
docker pull postgis/postgis
```

Add extension :

``` bash
docker exec -ti c7c1f966c4c4 psql serversDB -U adress_validator
CREATE EXTENSION hstore;
```

### OSM2PGSQL

source : <https://osm2pgsql.org/>

Installation : <https://osm2pgsql.org/doc/install/linux.html>

``` bash
sudo apt-get update
sudo apt install osm2pgsql
```

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

## Download file

<https://download.geofabrik.de/europe/france/rhone-alpes-latest.osm.pbf>

## Import address file

``` bash
osm2pgsql -H localhost -d serversDB -U adress_validator -W -P 32781 --create --slim -G --hstore -S /usr/share/osm2pgsql/default.style ../../geofabrick/rhone-alpes-latest.osm.pbf

```

Import sans mapping, toutes les valeurs sont dans tags

``` bash
osm2pgsql -H localhost -d serversDB -U adress_validator -W --create --slim -G --hstore ../../geofabrick/rhone-alpes-latest.osm.pbf
osm2pgsql -H localhost -d serversDB -U adress_validator -W -P 32781 --create --slim -G --hstore ../../geofabrick/rhone-alpes-latest.osm.pbf


```


## Query database

``` sql
SELECT tags->'addr:city' AS city, count(*)
FROM planet_osm_roads
WHERE tags->'addr:city' is not null
GROUP BY city
Order By City

SELECT tags
FROM planet_osm_point
WHERE tags->'addr:city' = 'Onnion'

SELECT tags
FROM planet_osm_line
WHERE tags->'addr:city' = 'Onnion'

SELECT tags
FROM planet_osm_polygon
WHERE tags->'addr:city' = 'Onnion'

SELECT tags
FROM planet_osm_roads
WHERE tags->'addr:city' = 'Onnion'



SELECT osm_id, "addr:housenumber", "addr:street"
FROM planet_osm_polygon
WHERE "addr:housenumber" = 'xxx'
  AND "addr:street" = 'xxxx';

```

``` sql
SELECT a.osm_id, a."addr:housenumber", a."addr:street"
FROM planet_osm_polygon a -- table des adresses/bâtiments
JOIN planet_osm_polygon p -- table des limites administratives
  ON ST_Intersects(a.way, p.way) -- intersection géographique
WHERE p.name = 'XXX' -- nom de la ville
  AND p.boundary = 'administrative'
  AND p.admin_level = '8'
  AND a."addr:housenumber" IS NOT NULL -- filtrer uniquement les adresses avec des numéros
  AND a."addr:street" IS NOT NULL; -- filtrer uniquement les adresses avec des rues

```

## additional sources

Sources :

- <https://wiki.openstreetmap.org/wiki/Addresses>