-- test with a few tables: kanji, reading, reading_types, kanji_tags

DROP TABLE IF EXISTS kanji;
DROP TABLE IF EXISTS readings;
DROP TABLE IF EXISTS reading_groups;
DROP TABLE IF EXISTS tags;

CREATE TABLE kanji (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kanji TEXT NOT NULL,
  meaning TEXT NOT NULL
);

CREATE TABLE readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kanji_id INTEGER NOT NULL,
  reading TEXT NOT NULL,
  reading_type_id INTEGER NOT NULL,
  FOREIGN KEY (kanji_id) REFERENCES kanji (id),
  FOREIGN KEY (reading_type_id) REFERENCES reading_type(id)
);

CREATE TABLE reading_types (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reading_type TEXT NOT NULL
);

-- only kanji tags for now
CREATE TABLE tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag TEXT NOT NULL
);

CREATE TABLE kanji_tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_id INTEGER NOT NULL,
  kanji_id INTEGER NOT NULL,
  FOREIGN KEY (tag_id) REFERENCES tags(id),
  FOREIGN KEY (kanji_id) REFERENCES kanji (id)
);