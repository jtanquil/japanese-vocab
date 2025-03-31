from flask import current_app

from .. import db

def test_initialize_db():
  test = db.get_db()

  db.init_db()
  print("reinitialized db")

  add_test_data(test)
  
def add_test_data(cur):
  with current_app.open_resource('./tests/testdata.sql') as f:
    cur.executescript(f.read().decode('utf8'))

  print("added test data")