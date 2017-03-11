from flask import Flask, request, jsonify
from models import Author, Book, initialize
from schemas import author_schema, book_schema

from flask_cors import CORS

app = Flask(__name__)
CORS(app=app)


@app.route('/api/authors', methods=["POST"])
def create_author():
    author, errors = author_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    author.save()

    return jsonify(author_schema.dump(author).data), 201


@app.route('/api/authors', methods=["GET"])
def get_authors():
    authors = list(Author.select())
    return jsonify(author_schema.dump(authors, many=True).data)


@app.route('/api/books', methods=["POST"])
def create_book():
    book, errors = book_schema.load(request.json)

    if errors:
        return jsonify(errors), 400

    book.save()

    return jsonify(book_schema.dump(book).data), 201


@app.route('/api/books', methods=["GET"])
def get_books():
    return jsonify(book_schema.dump(list(Book.select()), many=True).data)


@app.route('/api/books/<int:id>', methods=["GET"])
def get_one_book(id):
    try:
        book = Book.get(id=id)
        return jsonify(book_schema.dump(book).data)
    except Book.DoesNotExist:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404


@app.route('/api/books/<int:id>', methods=["PUT"])
def update_book(id):
    try:
        book = Book.get(id=id)
    except Book.DoesNotExist:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404

    book, errors = book_schema.load(request.json, instance=book)

    if errors:
        return jsonify(errors), 400

    book.save()

    return jsonify(book_schema.dumps(book).data), 200

#Delete
@app.route('/api/books/<int:id>', methods=["DELETE"])
def delete_book(id):
    is_book_exists = Book.select().filter(id=id).exists()

    if not is_book_exists:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404

    Book.delete().where(Book.id == id).execute()
    return jsonify({}), 204


if __name__ == '__main__':
    initialize()
    #app.debug = True
    #app.run()
    app.run(use_reloader=True)
