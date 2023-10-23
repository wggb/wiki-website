import sqlalchemy
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure SQLAlchemy to use db
# todo

@app.route("/", methods=["GET"])
# requite login
# todo
def homepage():

    if session.get("user_id") is None:
            return redirect("/login")
    
    return render_template('homepage.html')

@app.route('/login', methods=["GET", "POST"])
def login():

    session.clear()
    if request.method == 'POST':
        if not request.form.get("username"):
            return render_template('apology.html')
        if not request.form.get("password"):
            return render_template('apology.html')

        # todo: check database for user

        # todo: start session

        # if all is right
        return redirect('/')
    
    else:
        return render_template('login.html')