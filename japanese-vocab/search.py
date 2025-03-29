from flask import Blueprint, request, render_template

from .db import get_db
from . import query_strings

from .tests import testdb

bp = Blueprint('search', __name__, url_prefix = '/search')

@bp.route('/', methods = ('GET', 'POST'))
def search(search_results = None):
  if request.method == 'POST' and 'search' in request.form and request.form['search'] != '':
    testdb.test_initialize_db()

    search_results = get_results(request.form['search'])
      
  return render_template('search.html', search_results = search_results)

# parse the string for qualifiers
# no qualifier = search for vocab
def get_results(search_query):
  parsed_search_query = search_query.split(":")

  if len(parsed_search_query) == 1:
    return query_db(get_db(), query_strings.vocab, search_query)
  elif len(parsed_search_query) == 2:
    query_type = parsed_search_query[0].lower()

    if query_type == 'vocab':
      return query_db(get_db(), query_strings.vocab, parsed_search_query[1])
    elif query_type == 'kanji':
      return query_db(get_db(), query_strings.kanji, parsed_search_query[1])
    elif query_type == 'tag':
      return query_db(get_db(), query_strings.tag, parsed_search_query[1])
    else:
      return [ {
        "search_query": search_query,
        "result": "invalid query ([vocab/kanji/tag]:query)"
      }]
  else:
    return [ {
      "search_query": search_query,
      "result": "invalid query ([vocab/kanji/tag]:query)"
    }]
  
# converts a list of sqlite3.Row objects into a list of dicts with column/value pairs
def db_query_to_dict(rows):
  return [ { key: row[key] for key in row.keys() } for row in rows ]

# updates each result with columns from join tables
def update_result(cur, db_query, params, result):
  for ele in db_query_to_dict(cur.execute(db_query, params)):
    result.update(ele)

# returns a list (possibly with 1 element) of results from a "main" table (words/kanji/tags)
def get_result_list(cur, list_query, search_query):
  return [ { key : row[key] for key in row.keys() } for row in cur.execute(
    list_query, ('%' + search_query + '%',)).fetchall() ]

# each query type does two things:
# 1) searches a "main table" (words/kanji/tags) and gets a list of results
# 2) fills out each result with data from the corresponding join tables
def query_db(cur, db_queries, search_query):
  results = get_result_list(cur, db_queries['get_result_list'], search_query)

  if len(results) == 0:
    return [ {
      "search_query": search_query,
      "result": "no results found"
    } ]
  else:
    for result in results:
      id = result['id']

      for join in db_queries['joins']:
        update_result(cur, join, (id,), result)

    return results
  
# outline for tag search:
# 1) get all words matching the tag
# 2) get all kanji matching the tag
# 3) return 1) + 2)