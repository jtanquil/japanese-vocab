import os

from flask import Flask, render_template, request
from .tests import testdata

def create_app(test_config = None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config = True)
  app.config.from_mapping(
    SECRET_KEY = 'dev',
    DATABASE = os.path.join(app.instance_path, 'japanese_vocab.sqlite'),
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent = True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
      os.makedirs(app.instance_path)
  except OSError:
     pass
  
  @app.route('/', methods = ('GET', 'POST'))
  def get_search_page(search_results = None):
    if 'search' in request.form and request.form['search'] is not '':
       search_results = testdata.testdata
    return render_template('search.html', search_results = search_results)
  
  return app