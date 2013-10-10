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

# DB init via flask's sqlAlchemy extension
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dpb:dpb_nyu@handbanana.bio.nyu.edu:3306/noGO'
db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data_request():
    """
    Method to handle requests for data. Parameters in the 'request' object (parse and check first).
    Should have: Organism, Go Category, Go Term [optional], Algorithm [1+]
    """
    return render_template('bad_request.html', request=request)

@app.route('/downloads')
def downloads():
    """Static downloads page"""
    return render_template('downloads.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == "__main__":
    #WARNING: Do not run in debug mode publicly (allows for code execution)
    app.debug = True

    # Logging setup
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        log_file = "nogo.web.log"
        log_bytes = 10 * 1024 * 1024

        file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=log_bytes, backupCount=0)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s ' '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

    # app.run(host='0.0.0.0')
    app.run()
