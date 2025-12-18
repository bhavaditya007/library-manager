from flask import Flask, render_template, request, redirect, abort
import sqlite3
import pytesseract
import cv2
import os
import re
import requests

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# ---------- UTILITIES ----------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def ocr_lines(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    return [l.strip() for l in text.split("\n") if l.strip()]

def extract_isbn(lines):
    isbn_regex = re.compile(r"(97[89]\d{10}|\d{9}[\dX])")
    for line in lines:
        match = isbn_regex.search(line.replace("-", "").replace(" ", ""))
        if match:
            return match.group()
    return None

def fetch_from_google_books(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    r = requests.get(url, timeout=5)
    data = r.json()

    if "items" not in data:
        return None, None

    info = data["items"][0]["volumeInfo"]
    title = info.get("title", "").strip()
    authors = info.get("authors", [])
    author = ", ".join(authors).strip() if authors else ""

    return title, author

# ---------- ROUTES ----------

@app.route("/")
def home():
    return redirect("/add")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        genre = request.form.get("genre", "").strip()
        location = request.form.get("location", "").strip()
        image = request.files.get("image")

        # HARD ENFORCEMENT
        if not location:
            abort(400, "Location is required")

        # IMAGE FLOW (OCR + PREVIEW)
        if image and image.filename:
            if not allowed_file(image.filename):
                abort(400, "Only image files allowed")

            path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
            image.save(path)

            lines = ocr_lines(path)
            isbn = extract_isbn(lines)

            if isbn:
                title, author = fetch_from_google_books(isbn)

            if not title and lines:
                title = lines[0]
            if not author and len(lines) > 1:
                author = lines[1]

            return render_template(
                "preview.html",
                title=title,
                author=author,
                genre=genre,
                location=location
            )

        # MANUAL ENTRY FLOW
        if not title or not author:
            abort(400, "Title and Author are required")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, genre, location) VALUES (?, ?, ?, ?)",
            (title, author, genre, location)
        )
        conn.commit()
        conn.close()

        return redirect("/books")

    return render_template("add_book.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    genre = request.form.get("genre", "").strip()
    location = request.form.get("location", "").strip()

    # FINAL GUARANTEE
    if not title or not author or not location:
        abort(400, "Title, Author, and Location are required")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, genre, location) VALUES (?, ?, ?, ?)",
        (title, author, genre, location)
    )
    conn.commit()
    conn.close()

    return redirect("/books")

@app.route("/books")
def books():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    data = cur.fetchall()
    conn.close()
    return render_template("books.html", books=data)

@app.route("/delete/<int:book_id>")
def delete(book_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return redirect("/books")

# ---------- RUN ----------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


