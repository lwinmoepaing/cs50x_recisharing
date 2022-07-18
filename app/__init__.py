import os
from flask import Flask
from flask_session import Session
from cs50 import SQL

# Config Application and Template Directory
template_dir = os.path.abspath('./app/view')
static_dir = os.path.abspath('./public')
app = Flask(__name__, 
            template_folder=template_dir,
            static_url_path='',
            static_folder=static_dir)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Session
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# All the routes
from app.routes import guest_router
from app.routes import user_router