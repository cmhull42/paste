#!env/bin/python
import config

schema = """
drop table if exists entries;
create table entries (
  id integer primary key auto_increment,
  title text({titlelength}),
  text text({textlength}) not null,
  created_at timestamp,
  author text({authorlength}),
  options text not null,
  urlHash text
);
""".format(
            titlelength =config.MAX_TITLE_LENGTH,
            textlength  =config.MAX_TEXT_LENGTH,
            authorlength=config.MAX_AUTHOR_LENGTH)

with open("schema.sql", "w+") as f:
    f.write(schema)
