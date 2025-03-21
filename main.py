from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello_name(name):
  return f'<p>Hello {name}!</p>'

with app.test_request_context():
  print(url_for('hello_world'))
  print(url_for('hello_name', name = 'test2'))