from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request, session
from flask_login import login_required, logout_user, current_user, login_user
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, allowed_file, modal
from datetime import timedelta

# from run import auth_bp

# will house routes: login, logout and register.
auth_bp = Blueprint('auth_bp', __name__)

from run import login_manager
from database import db, User

@auth_bp.route("/check", methods=["GET"])
def check():
    ''' A function to check if username exist in database or not.
    If yes, return false. If no, return true.
    The Ajax function will call this function when form in register is submitted.
    '''

    username = request.args.get("username")
    user = User.query.filter_by(username = username).first()

    if not user:
        # print("username is available")
        return jsonify(True)
    else:
        # print("User is {}".format(user.username))
        return jsonify(False)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in
    Converted to Bakery as at 6 Oct 5:09pm """

    modaltext = modal()

    # return user to where he was at before.
    if current_user.is_authenticated:
        return redirect("/")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Please provide a username")
            return redirect(url_for("auth_bp.login"))

        # Ensure password was submitted
        if not password:
            flash("Please provide a password.")
            return redirect(url_for("auth_bp.login"))

        # Get the object associated with the user.
        alluser = User.query.filter_by(username = username).all()
        if len(alluser) == 1:
            user = alluser[0]
            if user.check_password(password = password):
                user.authenticated = True
                db.session.add(user)

                session["user"] = user.username
                session["usertype"] = user.usertype
                # print(session["usertype"])
                login_user(user, remember = True, duration = timedelta(minutes = 15))

                db.session.commit()

                return redirect(url_for("index"))
            else:
                flash("Wrong credentials.")
                return render_template("authentication/login.html"), 400
        elif len(alluser) == 0:
            flash("Wrong credentials.")
            return render_template("authentication/login.html"), 400
        else:
            print("Database is bugged. Please check")
    else:
        return render_template("authentication/login.html", modal = modaltext), 200

@auth_bp.route("/logout")
@login_required
def logout():
    """Log user out"""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    # Redirect user to index.
    return redirect("/")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user
    Converted to bakery @ 6 Oct 4:45pm """

    modaltext = modal()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmpass = request.form.get("confirmation")
        usertype = request.form.get("buysell")

        existing_user = User.query.filter_by(username=username).first()
        if username and password and password == confirmpass and len(password) > 8 and confirmpass:
            # creates an instance of the User class and adds it into the database (session only).
            if not existing_user:
                new_user = User(username = username, password = password, usertype = usertype)
                new_user.authenticated = True
                db.session.add(new_user)

                logged = User.query.filter_by(username = username).first()
                session["user"] = new_user.username
                session["usertype"] = new_user.usertype
                login_user(new_user, remember = True, duration = timedelta(minutes = 15))

                db.session.commit()
                flash("Welcome, {}".format(username))
                return redirect(url_for("index"))
            else:
                flash('A user already exists with that username.')
                return render_template("authentication/register.html", modal = modaltext), 400
        else:

            flash("Please ensure you have filled in all the details, and adhered to the guidelines.", 400)
            return render_template("authentication/register.html", modal = modaltext), 400
    else:
        return render_template("authentication/register.html", modal = modaltext), 200

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        try:
            # print("user_id is {}".format(user_id))
            return User.query.filter_by(username = user_id).first()
        except:
            return None
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
