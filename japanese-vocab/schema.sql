DROP TABLE IF EXISTS words;
DROP TABLE IF EXISTS words_furigana;
DROP TABLE IF EXISTS conjugation_groups;
DROP TABLE IF EXISTS parts_of_speech;
DROP TABLE IF EXISTS words_meanings;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS tags_words;
DROP TABLE IF EXISTS kanji;
DROP TABLE IF EXISTS reading_types;
DROP TABLE IF EXISTS readings;
DROP TABLE IF EXISTS tags_kanji;
DROP TABLE IF EXISTS kanji_words;

CREATE TABLE words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word TEXT NOT NULL
);

CREATE TABLE words_furigana (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word_id INTEGER NOT NULL,
  word_order INTEGER NOT NULL CHECK (word_order > 0),
  word_part TEXT NOT NULL,
  furigana TEXT,
  FOREIGN KEY (word_id) REFERENCES words (id),
  UNIQUE (word_id, word_order)
);

CREATE TABLE conjugation_groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conjugation_group TEXT NOT NULL
);

CREATE TABLE parts_of_speech (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  part_of_speech TEXT NOT NULL
);

CREATE TABLE words_meanings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word_id INTEGER NOT NULL,
  meaning TEXT NOT NULL,
  example TEXT NOT NULL,
  part_of_speech_id INTEGER NOT NULL,
  conjugation_group_id INTEGER,
  FOREIGN KEY (part_of_speech_id) REFERENCES parts_of_speech(id),
  FOREIGN KEY (conjugation_group_id) REFERENCES conjugation_group (id)
);

CREATE TABLE tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag TEXT NOT NULL
);

CREATE TABLE tags_words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_id INTEGER NOT NULL,
  word_id INTEGER NOT NULL,
  FOREIGN KEY (tag_id) REFERENCES tags (id),
  FOREIGN KEY (word_id) REFERENCES words (id),
  UNIQUE (tag_id, word_id)
);

CREATE TABLE kanji (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kanji TEXT NOT NULL,
  meaning TEXT NOT NULL
);

CREATE TABLE reading_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reading_type TEXT NOT NULL
);

CREATE TABLE readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kanji_id INTEGER NOT NULL,
  reading TEXT NOT NULL,
  reading_type_id INTEGER NOT NULL,
  FOREIGN KEY (kanji_id) REFERENCES kanji (id),
  FOREIGN KEY (reading_type_id) REFERENCES reading_type(id)
);

CREATE TABLE tags_kanji (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_id INTEGER NOT NULL,
  kanji_id INTEGER NOT NULL,
  FOREIGN KEY (tag_id) REFERENCES tags(id),
  FOREIGN KEY (kanji_id) REFERENCES kanji (id),
  UNIQUE (tag_id, kanji_id)
);

CREATE TABLE kanji_words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  word_id INTEGER NOT NULL,
  kanji_id INTEGER NOT NULL,
  word_order INTEGER NOT NULL CHECK (word_order > 0),
  FOREIGN KEY (word_id) REFERENCES words (id),
  FOREIGN KEY (kanji_id) REFERENCES kanji (id),
  UNIQUE (word_id, word_order)
);