drop table if exists measurements;

create table measurements(
	id integer primary key,
	ml real,
	timestamp datetime default current_timestamp
);
