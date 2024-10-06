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


## Download file

<https://download.geofabrik.de/europe/france/rhone-alpes-latest.osm.pbf>

## Import address file

``` bash
osm2pgsql -H localhost -d serversDB -U adress_validator -W -P 32781 --create --slim -G --hstore -S /usr/share/osm2pgsql/default.style ../../geofabrick/rhone-alpes-latest.osm.pbf

```

