create table strategies (
  id serial not null primary key,
  filepath text,
  body text not null,
  md5sum varchar(32) not null,
  CONSTRAINT checksum UNIQUE(md5sum)
);

create table test_runs (
  id serial not null,
  strategy_id integer references strategies (id) not null,
  created_at timestamptz not null,
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  parameters jsonb not null,
  results jsonb not null,
  pickle bytea not null
);
