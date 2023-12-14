from flask import Flask, g, redirect
from flask import render_template as rt
from flask import request, session
from lxml.html.clean import clean_html
from markdown import markdown
from werkzeug.security import check_password_hash, generate_password_hash

from database import MarkdownFile, User
from database import session as db_session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# makes it so everytime there's a render template, global user is passed. (for logout and username in navbar)
def render_template(template_name_or_list, **context):
    return rt(
        template_name_or_list,
        username=g.user.username if g.user else None,
        **context,
    )


@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        rows = db_session.query(User).filter(User.id == user_id).all()
        g.user = rows[0] if rows else None
    else:
        g.user = None


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


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    username = request.form.get("username")
    password = request.form.get("password")

    error = None

    if request.method == "POST":
        if not username:
            error = "Sorry! Can't Do The Thing"
        if not password:
            error = "Sorry! Can't Do The Thing"
        # Query database for username
        rows = db_session.query(User).where(User.username == username).all()
        if len(rows) != 1 or not check_password_hash(rows[0].password, password):
            error = "Sorry! Can't Do The Thing"

        # Remember which user has logged in
        session["user_id"] = rows[0].id  # check this!

        if error:
            return render_template("login.html", error=error)
        else:
            return redirect("/")

    else:
        return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    error = None

    if request.method == "POST":
        if not request.form.get("username"):
            error = "Sorry! Can't Do The Thing"
        elif not request.form.get("password"):
            error = "Sorry! Can't Do The Thing"
        elif not request.form.get("confirmation"):
            error = "Sorry! Can't Do The Thing"
        elif request.form.get("password") != request.form.get("confirmation"):
            error = "Sorry! Can't Do The Thing"
        else:
            # check for others with the same username
            ## rows = SELECT * FROM users WHERE username = ?, request get username
            rows = db_session.query(User).where(User.username == username).all()

            if len(rows) > 0:
                error = "Sorry! Can't Do The Thing"
            else:
                # add user to database
                hashed_password = generate_password_hash(password)
                user = User(username=username, password=hashed_password)
                db_session.add(user)
                db_session.commit()
                # start session
                session["user_id"] = user.id
                return redirect("/")

        if error:
            return render_template("register.html", error=error)

    else:
        return render_template("register.html", error=error)


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return redirect("/")


@app.route("/results", methods=["GET"])
def results():
    query = request.form.get("search")
    results = perform_search(query)
    return render_template("results.html", results=results)


def perform_search(query):
    # search logic
    # return search results
    pass


@app.route("/results/<int:result_id>", methods=["GET"])
def result(result_id: int):
    markdown_file = (
        db_session.query(MarkdownFile).where(MarkdownFile.id == result_id).first()
    )
    if markdown_file:
        return render_template(
            "result.html",
            result_id=result_id,
            markdown=clean_html(
                markdown(
                    text=markdown_file.content,
                    output_format="html",
                )
            ),
        )
    else:
        # Handle the case when the result with the specified ID is not found
        return render_template("404.html")
