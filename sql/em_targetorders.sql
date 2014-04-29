-- Table: em_targetorders

-- DROP TABLE em_targetorders;

CREATE TABLE em_targetorders
(
  id character(36) NOT NULL,
  generatedby character varying(255) NOT NULL,
  type character varying(32) NOT NULL,
  route character varying(255) NOT NULL,
  state character varying(32) NOT NULL,
  timecreated timestamp without time zone NOT NULL,
  timesent timestamp without time zone,
  timeactive timestamp without time zone,
  timesuspended timestamp without time zone,
  timecomplete timestamp without time zone,
  timecancelled timestamp without time zone,
  expiretime timestamp without time zone,
  timeapproved timestamp without time zone,
  routeid character varying(255),
  CONSTRAINT em_targetorders_pkey PRIMARY KEY (id )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_targetorders
  OWNER TO rjn;
