import sqlalchemy
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


# configure SQLAlchemy to use db
# todo


@app.route("/", methods=["GET"])
# requite login
# todo
def homepage():
    if session.get("user_id") is None:
        return redirect("/login")

    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("apology.html")
        if not request.form.get("password"):
            return render_template("apology.html")

        # todo: check database for user

        # todo: start session

        # if all is right
        return redirect("/")

    else:
        return render_template("login.html")
