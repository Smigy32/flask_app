from flask import jsonify, request, Blueprint
books_bp = Blueprint("books_bp", __name__)
books = [
    {
        "id": 1,
        "title": "Harry Potter",
        "author": "Joanne Rowling",
        "genre": "fantasy"
    },
    {
        "id": 2,
        "title": "The Witcher",
        "author": "Andrzej Sapkowski",
        "genre": "fantasy"
    },
    {
        "id": 3,
        "title": "The Red and the Black",
        "author": "Stendhal",
        "genre": "bildungsroman"
    }
]


@books_bp.route("/")  # start page
def index():
    return "<h1>It's a library! :)<h1>"


@books_bp.route("/books/", methods=["GET"])  # get all books
def get_books():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")
    if None not in (title, author, genre):  # just a simple filter by QUERY params if they all are not None
        some_books = [book for book in books if (title in book["title"].lower() and
                                                 author in book["author"].lower() and
                                                 genre in book["genre"].lower())]
        return jsonify(some_books)
    if title:
        some_books = [book for book in books if title in book["title"].lower()]
        return jsonify(some_books)
    if author:
        some_books = [book for book in books if author in book["author"].lower()]
        return jsonify(some_books)
    if genre:
        some_books = [book for book in books if genre in book["genre"].lower()]
        return jsonify(some_books)
    return jsonify(books)


@books_bp.route("/books/<int:book_id>/", methods=["GET"])  # get a book by its id
def get_book(book_id):
    book = list(filter(lambda b: b["id"] == book_id, books))
    if not book:
        return jsonify({"message": "Book not found."}), 404
    book = book[0]
    return jsonify(book)


@books_bp.route("/books/", methods=["POST"])  # create a new book
def create_book():
    if not request.json:  # a post request mustn't be empty
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    title, author, genre = request.json.get("title"), request.json.get("author"), request.json.get("genre")
    if not title or not author or not genre:  # to create a book we need to set all values
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": title,
        "author": author,
        "genre": genre
    }
    books.append(book)
    return jsonify({"message": "The book is created!"})


@books_bp.route("/books/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    book = list(filter(lambda b: b["id"] == book_id, books))
    if not book:
        return jsonify({"message": "Book not found."}), 404
    if not request.json:  # a patch request mustn't be empty
        return jsonify({"message": "Please fill in all information about the book!"}), 400
    book = book[0]
    title, author, genre = request.json.get("title"), request.json.get("author"), request.json.get("genre")
    # we need to check if the entered property exists
    for key in request.json:
        if key not in book:
            return jsonify({"message": f"The property {key} does not exist!"})
    if title:
        book["title"] = title
    if author:
        book["author"] = author
    if genre:
        book["genre"] = genre
    return jsonify({"message": "The book was updated"})


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = list(filter(lambda b: b["id"] == book_id, books))
    if not book:
        return jsonify({"message": "Book not found."}), 404
    books.remove(book[0])
    return jsonify({"message": "The book was deleted!"})