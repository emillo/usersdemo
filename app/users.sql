CREATE TABLE Users (
       ID INTEGER PRIMARY KEY AUTOINCREMENT,
       username varchar(80) UNIQUE NOT NULL,
       firstname varchar(80) NOT NULL,
       lastname varchar(80) NOT NULL,
       email varhchar(120) NOT NULL,
       password varchar(87) NOT NULL
);

INSERT INTO Users VALUES(1,"admin","John","Doe","johndoe@nonexistent.org","$pbkdf2-sha256$29000$4pyTEkJIae3dm/P.v5cy5g$bnh4Y6WkJ3nMs.csMbMwgamU3aMiYYrAN11SgOjRf7s");


















