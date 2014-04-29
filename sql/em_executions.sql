-- Table: em_executions

-- DROP TABLE em_executions;

CREATE TABLE em_executions
(
  id character(36) NOT NULL,
  parent character(36) NOT NULL,
  route character varying(255) NOT NULL,
  routeid character varying(255),
  timecreated timestamp without time zone NOT NULL,
  quantity real NOT NULL,
  price real NOT NULL,
  symbol character varying(255) NOT NULL,
  CONSTRAINT em_executions_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_executions
  OWNER TO rjn;
