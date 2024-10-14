---
layout: default
parent: Addresses validator
title: Local Databases
nav_order: 1
has_children: false
---

## Goal

Integrating official address sources on premise will allow you to validate your clients' addresses without exposing them online. This ensures both confidentiality and a reliable, complete database for your validations.

## Strategy

Import data from the following source :

1. France

    Use the Base d'Adresses Nationale (BAN), which is an official, accurate, and comprehensive source. It can be downloaded and imported into your on-premise PostgreSQL/PostGIS database.

    Advantages: Reliable data provided by public authorities.
    Format: Available for download in CSV, GeoJSON, or Shapefile format.

2. Other Countries

    Use OpenAddresses.io, which aggregates address data from multiple countries. These files can be downloaded and used locally to validate addresses without needing to connect to an online service.

    Advantages: Wide international coverage, easy to use.
    Format: Downloadable in CSV, GeoJSON, or Shapefile.

3. OpenStreetMap (OSM)

    Using OSM as a complementary source for obtaining addresses that may not be available elsewhere. While sometimes less accurate than official sources, OSM covers many countries and offers downloadable .osm.pbf files that can be processed locally

Remarks :

TIGER (Topologically Integrated Geographic Encoding and Referencing) data from the U.S. Census Bureau is another potential data source for U.S. addresses. I didn't include TIGER initially because it is generally less focused on detailed, up-to-date address information compared to other sources like OpenAddresses or official state-level databases.
