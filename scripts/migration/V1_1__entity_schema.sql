CREATE SCHEMA IF NOT EXISTS entity;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS entity.statuses
(
    id serial NOT NULL,
    const character varying(45) COLLATE pg_catalog."default" NOT NULL UNIQUE,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Entity_Status_PK" PRIMARY KEY (id)
);

INSERT INTO entity.statuses (const, description) VALUES
('ACTIVE', 'An active entity'),
('DELETED', 'A deleted entity');