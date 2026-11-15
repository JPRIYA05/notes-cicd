import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

DB_PATH = os.environ.get("DB_PATH", "notes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "title TEXT NOT NULL, content TEXT NOT NULL)"
        )


def create_app():
    app = Flask(__name__)
    init_db()

    @app.route("/")
    def index():
        with get_db() as conn:
            notes = conn.execute("SELECT * FROM notes ORDER BY id DESC").fetchall()
        return render_template("index.html", notes=notes)

    @app.route("/add", methods=["POST"])
    def add():
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if title and content:
            with get_db() as conn:
                conn.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        return redirect(url_for("index"))

    @app.route("/edit/<int:note_id>", methods=["POST"])
    def edit(note_id):
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if title and content:
            with get_db() as conn:
                conn.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
        return redirect(url_for("index"))

    @app.route("/delete/<int:note_id>", methods=["POST"])
    def delete(note_id):
        with get_db() as conn:
            conn.execute("DELETE FROM notes WHERE id=?", (note_id,))
        return redirect(url_for("index"))

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
