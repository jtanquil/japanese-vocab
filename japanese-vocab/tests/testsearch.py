import sqlite3
from .query_strings import query_strings
from flask import current_app

from .. import db

def query_to_dict(rows):
  return [ { key: row[key] for key in row.keys() } for row in rows ]

def update_result(cur, query, params, result):
  for ele in query_to_dict(cur.execute(query, params)):
    result.update(ele)

def get_word_list(cur, word):
  return [ { key : row[key] for key in row.keys() } for row in cur.execute(
    query_strings['get_word_list'], ('%' + word + '%',)).fetchall() ]

# two cases: returning one result (redirect to word page),
# or > 1 (redirect to search page w/list)
def get_vocab(cur, word):
  # get words: returns a list (possibly with 1 element) of words from words table
  results = get_word_list(cur, word)

  if len(results) == 0:
    return [ {
      "search_query": word,
      "result": "no results found"
    } ]
  else:
    for result in results:
      id = result['id']
      update_result(cur, query_strings['get_word_meanings'], (id,), result)
      update_result(cur, query_strings['get_kanji_words'], (id,), result)
      update_result(cur, query_strings['get_word_furigana'], (id,), result)
      update_result(cur, query_strings['get_word_tags'], (id,), result)

    return results

def test_initialize_db():
  test = db.get_db()

  # reinitialize the db
  db.init_db()

  print("reinitialized db")

  add_test_data(test)

  print("added test data")

  return test

def add_test_data(cur):
  with current_app.open_resource('./tests/testdata.sql') as f:
    cur.executescript(f.read().decode('utf8'))

  print("added test data")

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