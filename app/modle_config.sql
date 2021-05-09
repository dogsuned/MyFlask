DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS data;

CREATE TABLE user (
  id integer primary key autoincrement,
  name string not null,
  password string not null
);

CREATE TABLE data (
  id integer primary key autoincrement,
  year integer,
  month integer,
  wage string not null,
  user_id integer,
  FOREIGN KEY (user_id ) REFERENCES user(id)
);
