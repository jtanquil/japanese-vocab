import sqlite3

from .. import db

def query_to_dict(rows):
  return [ { key: row[key] for key in row.keys() } for row in rows ]

def test_db():
  test = db.get_db()

  # reinitialize the db
  db.init_db()

  print("reinitialized db")

  test.execute(
    """
      INSERT INTO words (word) VALUES ('先生')
    """
  )
  
  test.execute(
    """
      INSERT INTO words_furigana (word_id, word_order, word_part, furigana) VALUES
      (1, 1, '先', 'せん'),
      (1, 2, '生', 'せい')
    """
  )

  test.execute(
    """
      INSERT INTO parts_of_speech (part_of_speech) VALUES
      ('noun')
    """
  )

  test.execute(
    """
      INSERT INTO words_meanings (word_id, meaning, example, part_of_speech_id) VALUES
      (1, 'teacher', '私は日本語の先生があります。(I have a Japanese teacher.)', 1)
    """
  )

  # res = test.execute(
  #   """
  #     SELECT * FROM words
  #   """
  # ).fetchone()

  res = test.execute(
    """
      SELECT * FROM words
      JOIN words_furigana
      ON words.id = words_furigana.word_id
      JOIN words_meanings
      ON words.id = words_meanings.word_id
    """
  ).fetchall()

  return query_to_dict(res)

testdata = [
  {
    "word": "先生",
    "meaning": "teacher",
    "pronounciation": "せんせい",
    "part_of_speech": "noun",
    "tags": ["n5", "school"],
    "kanji": ["先", "生"],
  },
  {
    "word": "上る",
    "meaning": "to go up; to climb",
    "pronounciation": "のぼる",
    "part_of_speech": "verb",
    "tags": ["n5"],
    "kanji": ["上"],
    "conjugation_group": "godan",
  },
  {
    "word": "かわいい",
    "meaning": "cute",
    "part_of_speech": "adjective",
    "tags": ["n5"],
    "conjugation_group": "い-adjective",
  },
  {
    "kanji": "今",
    "meaning": "now",
    "tags": ["n5", "time"],
    "on-yomi": ["こん", "こ"],
    "kun-yomi": ["いま"],
    "words": ["今「いま」", "今年「ことし」", "今月「こんがつ」", "今日「きょう」"],
    "notes": "The common reading for 今日 is きょう.",
  }
]