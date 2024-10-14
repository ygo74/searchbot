---
layout: default
parent: Local Databases
grand_parent: Addresses validator
title: French BAN
nav_order: 1
has_children: false
---

## Goal

Import data from BANO

## details

1. Download data from BANO <https://bano.openstreetmap.fr/data/>

2. Create table to store addresses

    ``` sql
    CREATE TABLE bano_addresses (
        id SERIAL PRIMARY KEY,
        ref VARCHAR(255),           -- Identifiant unique de l'adresse
        numero VARCHAR(10),         -- Numéro de rue
        nom_voie VARCHAR(255),      -- Nom de la rue
        code_postal VARCHAR(5),     -- Code postal
        nom_commune VARCHAR(255),   -- Nom de la commune
        source VARCHAR(50),         -- Source de l'adresse (BAN, OSM, etc.)
        latitude FLOAT,             -- Latitude (WGS84)
        longitude FLOAT,            -- Longitude (WGS84)
        geom GEOMETRY(Point, 4326)  -- Colonne géométrique pour stockage spatial
    );

    ```

3. Import Data to table

    ``` sql
    COPY bano_addresses(ref, numero, nom_voie, code_postal, nom_commune, source, latitude, longitude)
    FROM '/path/to/bano_data.csv'
    WITH (FORMAT csv, DELIMITER ',', HEADER false);

    ```

4. Update geom column

    ``` sql
    UPDATE bano_addresses
    SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326);

    ```

5. Verify data

    ``` sql
    SELECT ref, numero, nom_voie, nom_commune, ST_AsText(geom)
    FROM bano_addresses
    LIMIT 10;

    ```

## Sources

- BANO:
  - https://bano.openstreetmap.fr/data/
  - https://bano.openstreetmap.fr/
  - https://github.com/osm-fr/bano

- https://adresse.data.gouv.fr/

