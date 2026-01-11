from flask import Blueprint, render_template, redirect, request
from .db import get_db

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return redirect("/add")

@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        location = request.form.get("location")

        db = get_db()
        db.execute(
            "INSERT INTO books (title, author, genre, location) VALUES (?, ?, ?, ?)",
            (title, author, genre, location)
        )
        db.commit()

        return redirect("/books")

    return render_template("add_book.html")

@bp.route("/books")
def books():
    db = get_db()
    data = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", books=data)

@bp.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id):
    db = get_db()
    db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    return redirect("/books")
