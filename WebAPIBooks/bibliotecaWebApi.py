import flask
from flask import jsonify, request, render_template
import sqlite3
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def home():
    return "<h1>Biblioteca online</h1>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    database = sqlite3.connect('db/books.db')
    c = database.cursor()
    c.execute("SELECT * FROM books ORDER BY year_published")
    all_books = c.fetchall()
    return jsonify(all_books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    database = sqlite3.connect('db/books.db')
    c = database.cursor()
    print(request.args)
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Errore: Non è stato immesso alcun id"

    c.execute(f"SELECT * FROM books WHERE id LIKE '{id}'")
    book = c.fetchall()

    return jsonify(book)

app.run()