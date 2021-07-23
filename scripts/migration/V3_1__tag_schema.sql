CREATE SCHEMA IF NOT EXISTS tag;

CREATE TABLE IF NOT EXISTS tag.types
(
    id serial NOT NULL,
    const character varying(45) COLLATE pg_catalog."default" NOT NULL,
    description character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Tag_Type_PK" PRIMARY KEY (id),
    CONSTRAINT "Tag_Type_Const_UNIQUE" UNIQUE (const)
);

INSERT INTO tag.types (const, description) VALUES
('RESTAURANT', 'Restaurant'),
('BAR', 'Bar');

CREATE TABLE IF NOT EXISTS tag.tags
(
    id serial NOT NULL,
    entity_id integer NOT NULL,
    type_id integer NOT NULL,
    CONSTRAINT "Tag_Tag_PK" PRIMARY KEY (id),
    CONSTRAINT "FK_Tag_Tag_Entity_ID" FOREIGN KEY (entity_id)
        REFERENCES entity.entities (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "FK_Tag_Tag_Type_ID" FOREIGN KEY (type_id)
        REFERENCES tag.types (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);