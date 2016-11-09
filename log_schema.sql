drop table if exists entries;
create table entries (
  uid text not null,
  latitude float(53) not null,
  longitude float(53) not null,
  'date' datetime not null
);
