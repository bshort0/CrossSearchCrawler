CREATE TABLE IF NOT EXISTS authors (
	id INTEGER PRIMARY KEY, 
	name text
);

CREATE TABLE IF NOT EXISTS publications (
	id INTEGER PRIMARY KEY, 
	title text, 
	year text, 
	doi text, 
	isbn text, 
	issn text, 
	url text, 
	startpage text, 
	endpage text
);

CREATE TABLE IF NOT EXISTS tags (
	id INTEGER PRIMARY KEY, 
	name text
);

CREATE TABLE IF NOT EXISTS authorpublink (
	authorID INTEGER, 
	pubID INTEGER
);

CREATE TABLE IF NOT EXISTS tagpublink (
	tagID INTEGER, 
	pubID INTEGER
);

CREATE TABLE IF NOT EXISTS searches (
	id INTEGER PRIMARY KEY, 
	searchText text, 
	site text
);

CREATE TABLE IF NOT EXISTS searchpublink (
	searchID INTEGER, 
	pubID INTEGER
);

