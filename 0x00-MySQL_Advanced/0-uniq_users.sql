-- This SQL script creates a table users
CREATE TABLE IF EXISTS users(
	id INT NOT NULL AUTO_INCREMENT,
	email  VARCHAR(255) NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY(id),
	UNIQUE(email));
