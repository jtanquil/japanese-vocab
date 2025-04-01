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
    return query_db(get_db(), query_strings.vocab_query, search_query)
  elif len(parsed_search_query) == 2:
    query_type = parsed_search_query[0].lower()

    if query_type == 'vocab':
      return query_db(get_db(), query_strings.vocab_query, parsed_search_query[1])
    elif query_type == 'kanji':
      return query_db(get_db(), query_strings.kanji_query, parsed_search_query[1])
    elif query_type == 'tag':
      return query_db(get_db(), query_strings.tag_query, parsed_search_query[1])
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

# returns a list (possibly with 1 element) of results from a single table
def query_single_table(cur, db_query, search_query):
  unsorted_results = [ { key : row[key] for key in row.keys() } for row in cur.execute(
    db_query['query'], (search_query,)).fetchall() ]
  
  print(unsorted_results)
  
  results = []
  ids = { row['id'] : True for row in unsorted_results }

  for id in ids:
    result = {}
    results.append(result)

    for row in unsorted_results:
      if row['id'] == id:
        for col in db_query['col_groups']:
          if db_query['col_groups'][col] is None:
            result[col] = row[col]
          else:
            if col not in result:
              result[col] = {}

            if row[col] not in result[col]:
              result[col][row[col]] = {
                aggregated_col : row[aggregated_col] for aggregated_col in db_query['col_groups'][col]
              }
    
  return results

# outline for tag search:
# 1) get all words matching the tag
# 2) get all kanji matching the tag
# 3) return 1) + 2)
def query_tags(cur, db_query, search_query):
  results = []

  for subquery in db_query['query']:
    subquery_results = query_single_table(cur, subquery, search_query)

    if len(subquery_results) != 0:
      results += subquery_results

  return results

def query_db(cur, db_query, search_query):
  if isinstance(db_query['query'], str):
    # need to insert the wildcards here since the vocab/kanji queries use WHERE ... LIKE
    results = query_single_table(cur, db_query, '%' + search_query + '%')
  else:
    # don't need wildcards here because the tag search uses WHERE ... =
    results = query_tags(cur, db_query, search_query)

  if len(results) == 0:
    results = [{
      "search_query": search_query,
      "result": "no results found"
    }]

  return results