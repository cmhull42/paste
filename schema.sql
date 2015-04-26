drop table if exists entries;
create table entries (
  id integer primary key auto_increment,
  title text,
  text text not null,
  created_at timestamp,
  author text,
  options text not null,
  urlHash text
);
