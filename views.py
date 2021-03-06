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


@app.route('/api/authors/<int:id>', methods=["PUT"])
def update_author(id):
    try:
        author = Author.get(id=id)
    except Author.DoesNotExist:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404

    author, errors = author_schema.load(request.json, instance=author)

    if errors:
        return jsonify(errors), 400

    author.save()

    return jsonify(book_schema.dumps(author).data), 200


@app.route('/api/authors/<int:id>', methods=["DELETE"])
def delete_author(id):
    is_author_exists = Author.select().filter(id=id).exists()

    if not is_author_exists:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404

    # Проверка на связи явтора с книгами
    # Для сохранения целосности данных
    is_author_relation = Book.filter(Book.author == id).exists()

    if is_author_relation:
        return jsonify({"message": "An author with an with id - `{id}` can not be deleted because it is associated "
                                   "with books".format(id=id)}), 404

    Author.delete().where(Author.id == id).execute()
    return jsonify({}), 204


@app.route('/api/authors', methods=["GET"])
def get_authors():
    authors = list(Author.select())
    return jsonify(author_schema.dump(authors, many=True).data)


@app.route('/api/authors/<int:id>', methods=["GET"])
def get_one_author(id):
    try:
        author = Author.get(id=id)
        return jsonify(author_schema.dump(author).data)
    except Author.DoesNotExist:
        return jsonify({"message": "Can't find author with id - `{id}`".format(id=id)}), 404


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


@app.route('/api/books/<int:id>', methods=["DELETE"])
def delete_book(id):
    is_book_exists = Book.select().filter(id=id).exists()

    if not is_book_exists:
        return jsonify({"message": "Can't find book with id - `{id}`".format(id=id)}), 404

    Book.delete().where(Book.id == id).execute()
    return jsonify({}), 204


if __name__ == '__main__':
    initialize()
    # app.debug = True
    # app.run()
    app.run(use_reloader=True)
