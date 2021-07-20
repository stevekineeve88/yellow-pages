CREATE SCHEMA IF NOT EXISTS entity;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS entity.statuses
(
    id serial NOT NULL,
    const character varying(45) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Entity_Status_PK" PRIMARY KEY (id),
    CONSTRAINT "Entity_Status_Const_UNIQUE" UNIQUE (const)
);

INSERT INTO entity.statuses (const, description) VALUES
('ACTIVE', 'An active entity'),
('DELETED', 'A deleted entity');

CREATE TABLE IF NOT EXISTS entity.entities
(
    id serial NOT NULL,
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    name character varying(250) COLLATE pg_catalog."default" NOT NULL,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    address character varying(500) COLLATE pg_catalog."default" NOT NULL,
    status_id integer NOT NULL,
    CONSTRAINT "Entity_Entity_PK" PRIMARY KEY (id),
    CONSTRAINT "Entity_Entity_UUID_UNIQUE" UNIQUE (uuid),
    CONSTRAINT "FK_Entity_Entity_Status_ID" FOREIGN KEY (status_id)
        REFERENCES entity.statuses (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);