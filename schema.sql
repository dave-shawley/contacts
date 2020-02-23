SET SEARCH_PATH TO public, pg_catalog;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS identifiers;
DROP TABLE IF EXISTS street_addresses;
DROP TABLE IF EXISTS contacts;
DROP COLLATION IF EXISTS case_insensitive;

CREATE COLLATION case_insensitive (PROVIDER = icu, LOCALE = 'und-u-ks-level2', deterministic = FALSE);

CREATE TABLE contacts (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    display       TEXT   NOT NULL,
    name          TEXT[] NOT NULL,
    primary_email TEXT COLLATE case_insensitive,
    company       TEXT
);

CREATE TABLE street_addresses (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_id     UUID REFERENCES contacts (id) ON DELETE CASCADE ON UPDATE CASCADE,
    label          TEXT NOT NULL,
    street_address TEXT NOT NULL,
    locality       TEXT,
    region         TEXT,
    country        TEXT NOT NULL
);

CREATE TABLE identifiers (
    contact_id UUID REFERENCES contacts (id) ON DELETE CASCADE ON UPDATE CASCADE,
    label      TEXT COLLATE case_insensitive NOT NULL,
    value      TEXT                          NOT NULL
);

