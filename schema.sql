CREATE TABLE entries (
    id INT AUTO_INCREMENT,
    title TEXT,
    content TEXT,
    posted_on DATETIME,
    primary key (id)
);

CREATE TABLE users
(
  id serial NOT NULL,
  user character varying(80) NOT NULL,
  pass character(40) NOT NULL,
  salt character(40) NOT NULL,
  email character varying(100) NOT NULL,
  privilege integer NOT NULL DEFAULT 0,
  CONSTRAINT utilisateur_pkey PRIMARY KEY (id)
)