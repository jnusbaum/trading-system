-- Table: em_targetordersymbols

-- DROP TABLE em_targetordersymbols;

CREATE TABLE em_targetordersymbols
(
  id serial NOT NULL,
  orderid character(36) NOT NULL,
  symbol character varying(128) NOT NULL,
  quantity real NOT NULL,
  shortflag boolean NOT NULL,
  liqest character(3),
  CONSTRAINT pk_em_symbollists PRIMARY KEY (id ),
  CONSTRAINT fk_em_symbollists_orderid FOREIGN KEY (orderid)
      REFERENCES em_targetorders (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_targetordersymbols
  OWNER TO rjn;
