CREATE SCHEMA IF NOT EXISTS contact;

CREATE TABLE IF NOT EXISTS contact.types
(
    id serial NOT NULL,
    const character varying(45) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Contact_Type_PK" PRIMARY KEY (id),
    CONSTRAINT "Contact_Type_Const_UNIQUE" UNIQUE (const)
);

INSERT INTO contact.types (const, description) VALUES
('PHONE', 'Phone'),
('EMAIL', 'Email'),
('WEBSITE', 'Website');

CREATE TABLE IF NOT EXISTS contact.contacts
(
    id serial NOT NULL,
    entity_id integer NOT NULL,
    type_id integer NOT NULL,
    info character varying(250) COLLATE pg_catalog."default" NOT NULL,
    description character varying(250) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Contact_Contact_PK" PRIMARY KEY (id),
    CONSTRAINT "FK_Contact_Contact_Entity_ID" FOREIGN KEY (entity_id)
        REFERENCES entity.entities (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "FK_Contact_Contact_Type_ID" FOREIGN KEY (type_id)
        REFERENCES contact.types (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);