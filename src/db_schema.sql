
drop table if exists  url_list;

create table if not exists   url_list (
   uid              serial   PRIMARY KEY,
   short_url        varchar( 4096 ) DEFAULT '',
   long_url         varchar( 4096 )
);



-- vim:ft=sqljsn:expandtab
