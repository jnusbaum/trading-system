-- Table: em_users

-- DROP TABLE em_users;

CREATE TABLE em_users
(
  username character varying(255) NOT NULL,
  passwd character varying(255) NOT NULL,
  role character varying(64) NOT NULL,
  dbusername character varying(64),
  dbpasswd character varying(64),
  CONSTRAINT pk_users_name PRIMARY KEY (username )
)
WITH (
  OIDS=FALSE
);
ALTER TABLE em_users
  OWNER TO rjn;
GRANT ALL ON TABLE em_users TO rjn;
