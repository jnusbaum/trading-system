-- Table: em_realorderconfigs

-- DROP TABLE em_realorderconfigs;

CREATE TABLE em_realorderconfigs
(
  id integer NOT NULL DEFAULT nextval('em_realorderconfigs_id_seq1'::regclass),
  orderid character(36) NOT NULL,
  param character varying(64) NOT NULL,
  val character varying(255),
  CONSTRAINT pk_realorderconfigs PRIMARY KEY (id ),
  CONSTRAINT fk_realorderconfigs_orderid FOREIGN KEY (orderid)
      REFERENCES em_realorders (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_realorderconfigs
  OWNER TO rjn;
