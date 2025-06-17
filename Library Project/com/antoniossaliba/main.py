from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    db = sqlite3.connect("books.db")
    cursor = db.cursor()
    books = cursor.execute("SELECT * FROM library")
    return render_template("index.html", books=books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    the_title = request.form["book-name"]
    the_author = request.form["book-author"]
    the_rating = request.form["book-rating"]
    db = sqlite3.connect("books.db")
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO library (title, author, rating) VALUES (?, ?, ?)", (the_title, the_author, the_rating))
    db.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        db = sqlite3.connect("books.db")
        cursor = db.cursor()
        book = cursor.execute("SELECT id, title, rating FROM library WHERE id = ?", [id])
        book_name = ""
        rating = 0
        the_id = 0
        for row in book:
            the_id = row[0]
            book_name = row[1]
            rating = row[2]
        return render_template("edit.html", book_name=book_name, rating=rating, the_id=the_id)
    the_new_rating = request.form["rating"]
    db = sqlite3.connect("books.db")
    cursor = db.cursor()
    cursor.execute("UPDATE library SET rating = ? WHERE id = ?", [the_new_rating, id])
    db.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    db = sqlite3.connect("books.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM library WHERE id = ?", [id])
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

