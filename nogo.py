"""
NeggoDB (negative gene annotation database) Python+Flask-based web site definition

@auth: dpb
@date: 8/28/2013
"""

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy

from db.nogoDB import *

# Flask init
app = Flask(__name__)


# Routes

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


if __name__ == "__main__":
    #WARNING: Do not run in debug mode publicly (allows for code execution)
    app.debug = True
    app.run()
