-- Table: em_targetorderconfigs

-- DROP TABLE em_targetorderconfigs;

CREATE TABLE em_targetorderconfigs
(
  id serial NOT NULL,
  orderid character(36) NOT NULL,
  param character varying(64) NOT NULL,
  val character varying(255),
  CONSTRAINT pk_order_configs PRIMARY KEY (id ),
  CONSTRAINT fk_order_configs_orderid FOREIGN KEY (orderid)
      REFERENCES em_targetorders (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_targetorderconfigs
  OWNER TO rjn;
