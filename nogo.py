"""
NeggoDB (negative gene annotation database) Python+Flask-based web site definition

@auth: dpb
@date: 8/28/2013
"""

from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, send_file
from flask.ext.sqlalchemy import SQLAlchemy

from db.nogoDB import *

# Flask init
app = Flask(__name__)

# DB init via flask's sqlAlchemy extension
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dpb:dpb_nyu@handbanana.bio.nyu.edu:3306/noGO'
db = SQLAlchemy(app)

# Config
File_Location = "./static/files/generated/"
NoGO_Version = 1
Algorithm_ID_Dict = {
    "Rocchio": 1, 
    "SNOB": 2,
    "NETL": 3
}
Organism_DBC_Dict = {
    'Arabidopsis3702': Arabidopsis3702,
    'Human9606': Human9606,
    'Mouse10090': Mouse10090,
    'Rice39947': Rice39947,
    'Worm6239': Worm6239,
    'Yeast4932': Yeast4932,
}

# Utility functions
def generate_nogo_file(organism, branch, term, rocchio, netl, snob):
    """
    Queries NoGO DB for negative example entries for given org, branch, and term (per alg). Writes 
    neg examples to file, one row per alg. File also contains header info (on params).
    Returns a tuple of (message, Filename URI). If creating the file fails for any reason, return is
    ("error message", None). If successfull, returns path of file generated.
    """

    # Set up variables for DB query
    try:
        organism_dbc = Organism_DBC_Dict[organism]
    except KeyError as e:
        return ("Organism {0} not valid".format(organism), None)

    # Query DB for data set for each algorithm (just get cursors, for now)
    rocchio_examples = None
    netl_examples = None
    snob_examples = None
    if rocchio:
        rocchio_examples = db.session.query(organism_dbc).filter_by(
                go_category=branch, 
                go_id=term, 
                algorithm_id=Algorithm_ID_Dict["Rocchio"])
    if netl:
        netl_examples = db.session.query(organism_dbc).filter_by(
                go_category=branch, 
                go_id=term,
                algorithm_id=Algorithm_ID_Dict["NETL"])
    if snob:
        snob_examples = db.session.query(organism_dbc).filter_by(
                go_category=branch, 
                go_id=term,
                algorithm_id=Algorithm_ID_Dict["SNOB"])

    # Check query results. If all empty, return None with error message "No results"
    # TODO: May have to/want to do this with counts, not existence (if no results, what is query return value with no all() or first()?)
    if rocchio_examples == None and netl_examples == None and snob_examples == None:
        return ("No results returned for given values (check GO Term!)", None)

    # Create filename from parameters
    # TODO: Create secure temporary filename for results in the File_Location dir (via python module secure file of whatever)
    outfile = os.path.join(File_Location, "{0}-{1}-{2}-{3}.txt".format(organism, branch, term, datetime.now()))
    with open(outfile) as outhandle:

        # Print file header information
        outhandle.write("--------->NoGO Negative gene examples: {0},{1},{2}\n".format(organism, term, branch))
        outhandle.write("<Algorithm>:    <1stMostNegGene>    <2ndMostNegGene>    <3rdMostNegGene>...\n")

        if rocchio_examples:
            _write_genes_to_file("Rocchio", rocchio_examples, outhandle)
        if netl:
            _write_genes_to_file("NETL", netl_examples, outhandle)
        if snob:
            _write_genes_to_file("SNOB", snob_examples, outhandle)

    return ("Successfuly wrote outfile {0}".format(outfile), outfile)


def _write_genes_to_file(algorithm_name, results_cursor, file_handle):
    """Writes gene_symbol from every item in results cursor to a tab-delimed line in file_handle"""
    file_handle.write("{0}:".format(algorithm_name))
    for neg_eg in results_cursor.all():
        file_handle.write("\t{0}".format(neg_eg.gene_symbol))
    file_handle.write("\n")


# Routes
@app.route('/data', methods=['POST'])
def data_request():
    """
    Method to handle requests for data. Parameters in the 'request' object (parse and check first).
    Should have: Organism, Go Category, Go Term [optional], Algorithm [1+]
    """
    # Check request
    if request.method != "POST":
        return render_template('bad_request.html', request=request, message="Server Error: Request not POST")
    
    # Get values from request
    if "Organism" not in request.form:
        return render_template('bad_request.html', request=request, message="Must select a valid Organism")
    organism = request.form["Organism"]
    
    if "Branch" not in request.form:
        return render_template('bad_request.html', request=request, message="Must select a valid GO Branch")
    branch = request.form["Branch"]
        
    if "Term" not in request.form:
        return render_template('bad_request.html', request=request, message="Must specify a valid GO Term")
    term = request.form["Term"]

    rocchio = True if "Rocchio" in request.form else False
    netl = True if "NETL" in request.form else False
    snob = True if "SNOB" in request.form else False
    if not (rocchio or netl or snob):
        return render_template('bad_request.html', request=request, message="Must select at least one Algorithm")

    # Call file-generator with request values
    (file_message, results_file) = generate_nogo_file(organism, branch, term, rocchio, netl, snob)
    if results_file == None:
        return render_template(
                'bad_request.html', 
                request=request, 
                message="Generating Negative Example file failed: {0}".format(file_message))

    # Send file to user. TODO: Look at send_file docs, see options
    try:
        send_file(results_file, mimetype="application/text", as_attachment=True)
        #TODO: Re-render the home template, or render a "Download will begin shortly (with loading icon) page?"
    except Exception as e:
        print "Exception when attempting send_file: {0}".format(e)
        return render_template('bad_request.html', request=request, message="Failed to send file")

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

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

    #WARNING: Do not share the secret key (obviously). Generate: os.urandom(24)
    app.secret_key = '\xbf\x18\xbc\xb2O#\xf7!{\t\xd3$i\xd7$_w\xeb\x01}V\xb1{p'

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
