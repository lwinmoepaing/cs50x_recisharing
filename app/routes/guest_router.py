import logging
from app import app, db
from app.lib.helper import FormError, fillErrorDictionary
from flask import redirect, render_template, request, session, flash

from werkzeug.security import check_password_hash, generate_password_hash

# Guest Page


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """Log user in"""

    # Forget any user_id
    session.clear()
    errors = []
    errors_dict = {
        "old_username": "",
        "username": "",
        
        "old_password": "",
        "password": ""
    }

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            errors.append(FormError("username", "User name is required", username))

        # Ensure password was submitted
        if not password:
            errors.append(FormError("password", "Password is required", password))

        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("login.html", errors=errors_dict)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            errors.append(FormError("password", "Password is not correct", ""))

        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("login.html", errors=errors_dict)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/user")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", errors=errors)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user id
    session.clear()
    errors = []
    errors_dict = {
        "old_username": "",
        "username": "",
        
        "old_password": "",
        "password": "",
        
        "old_confirm_password": "",
        "confirm_password": ""
    }

    # If Request is 'POST' method , creating user
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            errors.append(FormError("username", "must provide username", username))

        # Ensure password was submitted
        if not password:
            errors.append(FormError("password", "must provide password", password))

        # Ensure password was submitted
        if not confirm_password:
            errors.append(FormError("confirm_password", "must provide confirm password", confirm_password))

        # So far alright, we need to check password is same again
        if not password == confirm_password:
            errors.append(FormError("confirm_password", "not the same confirm password and password", ""))

        # Errors Validation Re Redirect
        if len(errors) > 0:
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("register.html", errors=errors_dict)

        # All validation is passed
        try:
            hash = generate_password_hash(password)
            query = "INSERT INTO users (name, password) VALUES (?, ?)"
            new_user = db.execute(query, username, hash)

            # Remember which user has logged in, we need to add inserted user_id
            session["user_id"] = new_user

            # Flash Messaging
            flash("Registered!")

            # Redirect with new user session , to user page
            return redirect("/user")
        except:
            errors.append(FormError("confirm_password", "User already created", ""))
            errors_dict = fillErrorDictionary(errors, errors_dict)
            return render_template("register.html", errors=errors_dict)

    # Render RegisterPage if request is 'GET' method
    else:

        return render_template("register.html", errors=errors)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")