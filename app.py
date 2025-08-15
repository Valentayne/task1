from __future__ import annotations
import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ---- Конфіг ----
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Підключення до PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")


app = Flask(__name__)
app.config.update(
    SECRET_KEY="change-me-in-production",
    SQLALCHEMY_DATABASE_URI=DATABASE_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,  # 8 MB
)

db = SQLAlchemy(app)

# ---- Модель ----
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def image_url(self) -> str | None:
        if self.image_filename:
            return url_for("static", filename=f"uploads/{self.image_filename}")
        return None

# ---- Утиліти ----
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---- Роути ----
@app.route("/", methods=["GET"])
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["POST"])
def create_post():
    content = (request.form.get("content") or "").strip()
    file = request.files.get("image")

    if not content and (not file or file.filename == ""):
        flash("Додайте текст або фото", "warning")
        return redirect(url_for("home"))

    image_filename = None
    if file and file.filename:
        if not allowed_file(file.filename):
            flash("Підтримувані формати: png, jpg, jpeg, gif, webp", "danger")
            return redirect(url_for("home"))
        ext = file.filename.rsplit(".", 1)[1].lower()
        safe_name = secure_filename(f"{uuid.uuid4().hex}.{ext}")
        file.save(UPLOAD_DIR / safe_name)
        image_filename = safe_name

    post = Post(content=content, image_filename=image_filename)
    db.session.add(post)
    db.session.commit()

    flash("Пост опубліковано!", "success")
    return redirect(url_for("home"))

# ---- Ініціалізація БД ----
@app.cli.command("init-db")
def init_db_command():
    """Ініціалізувати базу даних, створивши всі таблиці."""
    db.create_all()
    print("Базу даних ініціалізовано.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
