
drop table if exists  url_list;

create table if not exists   url_list (
   uid              serial   PRIMARY KEY,
   short_url        varchar( 4096 ) DEFAULT '',
   long_url         varchar( 4096 )
);

alter table url_list owner to url_shortener;



-- vim:ft=sqljsn:expandtab
