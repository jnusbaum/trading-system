-- Table: em_realorders

-- DROP TABLE em_realorders;

CREATE TABLE em_realorders
(
  id character(36) NOT NULL,
  parent character(36) NOT NULL,
  type character varying(32) NOT NULL,
  route character varying(255) NOT NULL,
  routeid character varying(255),
  state character varying(32) NOT NULL,
  timecreated timestamp without time zone NOT NULL,
  timecomplete timestamp without time zone,
  timecancelled timestamp without time zone,
  CONSTRAINT em_realorders_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_realorders
  OWNER TO rjn;
