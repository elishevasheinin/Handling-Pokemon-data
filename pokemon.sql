USE pokemon;

CREATE TABLE pokemon(
  id INTEGER PRIMARY KEY,
  name VARCHAR(25),
  height INTEGER,
  weight INTEGER
);
CREATE TABLE trainer(
  id INTEGER PRIMARY KEY,
  name VARCHAR (25),
  town VARCHAR (25)
);
CREATE TABLE owned_by(
  pokemon_id INTEGER ,
  trainer_id INTEGER ,
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
  FOREIGN KEY (trainer_id) REFERENCES trainer(id) ON DELETE CASCADE,
  PRIMARY KEY (pokemon_id, trainer_id)
);
CREATE table types(
  id INTEGER PRIMARY KEY,
  type_name VARCHAR (25)
);
CREATE TABLE has_types(
  pokemon_id INTEGER,
  type_id INTEGER ,
  FOREIGN KEY (pokemon_id) REFERENCES pokemon(id) ON DELETE CASCADE,
  FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE CASCADE,
  PRIMARY KEY (pokemon_id, type_id)
<<<<<<< HEAD
);
=======
);
>>>>>>> master
