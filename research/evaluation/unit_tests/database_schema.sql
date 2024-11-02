-- Remplacez 'nom_base' par le nom de votre base de données
-- Remplacez 'nom_utilisateur' par le nom de votre utilisateur PostgreSQL

-- Définir la variable pour le mot de passe, si elle est passée via `psql`
\set password :'password'

-- Vérifier si l'utilisateur existe, sinon le créer
DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'nom_utilisateur') THEN
      -- Utilisateur existe, changer le mot de passe
      EXECUTE 'ALTER ROLE nom_utilisateur WITH PASSWORD ' || quote_literal(:password);
   ELSE
      -- Utilisateur n'existe pas, le créer avec le mot de passe
      CREATE ROLE nom_utilisateur WITH LOGIN PASSWORD :'password';
   END IF;
END
$do$;

-- Vérifier si la base de données existe, sinon la créer
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nom_base') THEN
      CREATE DATABASE nom_base;
   END IF;
END
$do$;

-- Connecter à la base de données nouvellement créée pour exécuter les commandes suivantes
\c nom_base

-- Créer la table test_results si elle n'existe pas déjà
DROP TABLE IF EXISTS test_results;

CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    test_name VARCHAR(255) NOT NULL,
    status VARCHAR(10) NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accorder tous les privilèges sur toutes les tables du schéma public à l'utilisateur
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nom_utilisateur;

-- Accorder tous les privilèges sur toutes les séquences du schéma public à l'utilisateur
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nom_utilisateur;
