from models.message import Message
from flask import render_template, request


def index():
    if request.method == "POST":
        Message.create(text=request.form.get("message"))

    return render_template("index.html", messages=Message.fetch_all())


def basic():
    return "Basic handler without HTML template"
