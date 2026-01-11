from flask import Blueprint, render_template, redirect, request
from .db import get_db

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return redirect("/add")

@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        location = request.form["location"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO books (title, author, genre, location) VALUES (%s, %s, %s, %s)",
            (title, author, genre, location)
        )
        db.commit()
        cur.close()

        return redirect("/books")

    return render_template("add_book.html")

@bp.route("/books")
def books():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT id, title, author, genre, location FROM books ORDER BY id DESC")
    data = cur.fetchall()
    cur.close()
    return render_template("books.html", books=data)

@bp.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()
    cur.close()
    return redirect("/books")
