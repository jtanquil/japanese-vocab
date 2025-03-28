from flask import Blueprint, request, render_template
from .tests import testsearch
from .db import get_db

bp = Blueprint('search', __name__, url_prefix = '/search')

@bp.route('/', methods = ('GET', 'POST'))
def search(search_results = None):
  if request.method == 'GET':
     return render_template('search.html', search_results = search_results)
  elif request.method == 'POST':
    if 'search' in request.form and request.form['search'] != '':
        # parse the string for qualifiers (kanji:, tag: etc)
        # no qualifier = search for vocab
        testsearch.test_initialize_db()
        search_results = testsearch.get_vocab(get_db(), request.form['search'])
      
    return render_template('search.html', search_results = search_results)

@bp.route('/test_search/<word>')
def test_search(word):
   res = testsearch.test_initialize_db()
   return testsearch.get_vocab(res, word)