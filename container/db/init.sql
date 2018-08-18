CREATE DATABASE employee;
use employee;

CREATE TABLE info (
  first_name VARCHAR(20),
  last_name VARCHAR(20),
  age int,
  sex CHAR(1)
);

INSERT INTO info
  (first_name,last_name,age,sex)
VALUES
  ('anshul', 'sogani', 21 , 'M');