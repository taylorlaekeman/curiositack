\c curiositack

drop table if exists users cascade;
drop table if exists tacks cascade;
drop table if exists posts cascade;

create table users (
	id serial primary key,
	email text not null unique,
	password_hash text not null
);

create table tacks (
	id serial primary key,
	link text not null unique
);

create table posts (
	id serial primary key,
	account integer references users not null,
	tack integer references tacks not null
);

\d users
\d tacks
\d posts
