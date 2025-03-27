import sqlite3

from .. import db

def query_to_dict(rows):
  return [ { key: row[key] for key in row.keys() } for row in rows ]

def update_result(query, result):
  for ele in query_to_dict(query):
    result.update(ele)

def get_vocab(cur, word):
  res_dict = {}

  update_result(cur.execute(
    """
      SELECT * FROM words
      WHERE word LIKE (?)
    """, ('%' + word + '%',)
  ).fetchall(), res_dict)

  if 'id' not in res_dict:
    return res_dict

  update_result(cur.execute(
    """
      SELECT 
        wm.meaning, wm.example, 
        p.part_of_speech 
      FROM words_meanings wm
      JOIN parts_of_speech p
      ON p.id = wm.part_of_speech_id
      WHERE wm.word_id = (?)
    """, (res_dict['id'],)
  ).fetchall(), res_dict)
  
  update_result(cur.execute(
    """
      SELECT
        GROUP_CONCAT(k.kanji, ', ') kanji
      FROM kanji k
      JOIN kanji_words kw
      ON k.id = kw.kanji_id
      WHERE kw.word_id = (?)
      GROUP BY kw.word_id
    """, (res_dict['id'],)
  ).fetchall(), res_dict)

  update_result(cur.execute(
    """
      SELECT
        GROUP_CONCAT(wf.word_part, ', ') word_part,
        GROUP_CONCAT(wf.furigana, ', ') furigana
      FROM words_furigana wf
      JOIN words w
      ON wf.word_id = w.id
      WHERE w.id = (?)
      GROUP BY w.id
      ORDER BY wf.word_order
    """, (res_dict['id'],)
  ).fetchall(), res_dict)

  update_result(cur.execute(
    """
      SELECT
        GROUP_CONCAT(t.tag, ', ') tag
      FROM tags t
      JOIN tags_words tw
      ON t.id = tw.tag_id
      WHERE tw.word_id = (?)
    """, (res_dict['id'],)
  ).fetchall(), res_dict)

  return res_dict

def test_initialize_db():
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

  test.execute(
    """
      INSERT INTO kanji (kanji, meaning) VALUES
      ('先', 'before, ahead, previous, future, precedence'),
      ('生', 'life, genuine, birth')
    """
  )

  test.execute(
    """
      INSERT INTO reading_types (reading_type) VALUES
      ('kun-yomi'), ('on-yomi')
    """
  )

  test.execute(
    """
      INSERT INTO readings (kanji_id, reading, reading_type_id) VALUES
      (1, 'せん', 2), (1, 'さき', 1),
      (2, 'い', 1), (2, 'う', 1), (2, 'なま', 1), (2, 'な', 1), (2, 'せい', 2)
    """
  )

  test.execute(
    """
      INSERT INTO kanji_words (word_id, kanji_id, word_order) VALUES
      (1, 1, 1), (1, 2, 2)
    """
  )

  test.execute(
    """
      INSERT INTO tags (tag) VALUES
      ('n5'), ('school'), ('time')
    """
  )

  test.execute(
    """
      INSERT INTO tags_kanji (tag_id, kanji_id) VALUES
      (1, 1), (1, 2), (2, 1), (3, 1), (3, 2)
    """
  )

  test.execute(
    """
      INSERT INTO tags_words (tag_id, word_id) VALUES
      (1, 1), (2, 1)
    """
  )

  return test

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
    "kanji": "先",
    "meaning": "before, ahead, previous, future, precedence",
    "tags": ["n5", "time", "school"],
    "on-yomi": ["せん"],
    "kun-yomi": ["さき"]
  },
  {
    "kanji": "生",
    "meaning": "life, genuine, birth",
    "tags": ["n5", "school"],
    "on-yomi": ["せい"],
    "kun-yomi": ["い", "う", "なま", "な"]
  },
]