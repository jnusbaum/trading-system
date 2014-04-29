-- Table: em_realordersymbols

-- DROP TABLE em_realordersymbols;

CREATE TABLE em_realordersymbols
(
  id serial NOT NULL,
  orderid character(36) NOT NULL,
  symbol character varying(128) NOT NULL,
  quantity real NOT NULL,
  shortflag boolean NOT NULL,
  CONSTRAINT pk_em_realordersymbols PRIMARY KEY (id ),
  CONSTRAINT fk_em_realordersymbols_orderid FOREIGN KEY (orderid)
      REFERENCES em_realorders (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_realordersymbols
  OWNER TO rjn;
