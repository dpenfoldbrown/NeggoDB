"""
Importer for noGO prediction files. Files are essentially matrices of negative examples ordered by
rank. 
Each row represents a GO term, where first row is first GO term found in 'GO_Terms...' file, etc.
Each col contains a number repsenting a Gene Name, where the number is the 1-based line number 
containing the Gene Name found in the 'Gene_Names...' file.

@author dpb
@date   9/11/2013
"""

#go_name_dict = "/data/noGO/allGO_name_dict.pkl"
go_name_dict = "/Users/dpb/dev/repos/NoGO/test/allGO_name_dict.pkl"

def build_index_dict(filename, start=1, header=False):
    """Builds and returns a dictionary: index => file line starting at index 'start'"""
    index_dict = {}
    with open(filename) as handle:
        if header:
            handle.next()
        for line in handle:
            index_dict[start] = line.rstrip()
            start += 1
    return index_dict


def import_predictions(go_file, gene_file, prediction_file, algorithm_id, organism, go_category, version):
    """
    Imports predictions in prediction_file (with GO terms and Gene names based on those found in
    the in-order go_file and gene_file files) into the handbanana noGO database. Failure leaves
    partial records in the DB - manually clean up!
    """
    import pickle
    from db.nogoDB import Session, push_to_db 
    from db.nogoDB import Arabidopsis3702, Human9606, Mouse10090, Rice39947, Worm6239, Yeast4932
    
    # Get DBO class reference based on organism
    dbc_dict = {
        'arabidopsis': Arabidopsis3702,
        'human': Human9606,
        'mouse': Mouse10090,
        'rice': Rice39947,
        'worm': Worm6239,
        'yeast': Yeast4932,
    }
    try:
        org_dbc = dbc_dict[organism]
    except KeyError as ke:
        raise KeyError("Organism {0} does not exist in database. Options:\n{1}".format(organism, 
                         dbc_dict))

    # Open Go Names dictionary and pull into memory
    with open(go_name_dict) as handle:
        go_names = pickle.load(handle)

    # Build go term and gene name dicts (key is 1-based index)
    go_dict = build_index_dict(go_file)
    gene_dict = build_index_dict(gene_file)

    # Open session to add entries
    session = Session()

    # Parse prediction file
    go_term_index = 1
    with open(prediction_file) as handle:
        for line in handle:
            go_term = go_dict[go_term_index]

            print "Processing GO term {0}".format(go_term)

            try:
                go_name = go_names[go_term]
            except KeyError as ke:
                print "Warning: Name not found for GO ID {0}".format(go_term)
                go_name = ""
            ranked_gene_indexes = map(int, line.rstrip().split())

            gene_rank = 1
            for gene_index in ranked_gene_indexes:
                if gene_index == 0:
                    # If the column entry is 0, there are no more ranked genes for this GO term
                    break
                gene_name = gene_dict[gene_index]
                db_entry = org_dbc(
                        go_id=go_term,
                        gene_symbol=gene_name,
                        algorithm_id=algorithm_id,
                        rank=gene_rank,
                        go_category=go_category,
                        go_name=go_name,
                        version_id=version)

                #TODO: Add db_entry to database! For now, just print for testing
                #print "Prediction entry: {0}".format(db_entry)
                push_to_db(session, db_entry, exception_str="Failed to add {0} to database".format(db_entry), 
                           raise_on_duplicate=False)

                gene_rank += 1

            go_term_index += 1     
        
    print "Processing prediction file {0} complete".format(prediction_file)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Import noGO prediction files to DB")

    parser.add_argument("--GOTerms", action="store", dest="go_file", required=True,
        help="File containing in-order GO terms for this organism (eg: Mouse) and category (eg: BP)")
    parser.add_argument("--GeneNames", action="store", dest="gene_file", required=True,
        help="File containing in-order Gene Names for this organism (eg: Mouse)")
    parser.add_argument("--Predictions", action="store", dest="prediction_file", required=True,
        help="File containing negative example predictions per GO Term and Gene Name (see comments \
            for format")
    parser.add_argument("--algID", action="store", dest="algorithm_id", required=True,
        help="The database (noGO.algorithm.id) ID for the algorithm of the imported data")
    parser.add_argument("--version", action="store", dest="version", default="1", 
        help="The version of the data importing. Deafaults to 1")
    parser.add_argument("--organism", action="store", dest="organism", required=True,
        help="The Organism Tag of the data importing. (eg: human9606, yeast4932, etc.)")
    parser.add_argument("--GOcat", action="store", dest="go_category", required=True,
        help="The GO category importing. Must be one of BP, MF, CC")


    args = parser.parse_args()

    # Check files for existence and readability (raises IOError if not)
    with open(args.go_file): pass
    with open(args.gene_file): pass
    with open(args.prediction_file): pass

    # Check GO category
    if args.go_category not in ("BP","MF","CC"):
        raise Exception("GO category {0} not valid (not BP, MF, or CC)".format(args.go_category))

    # Call importer
    import_predictions(
        args.go_file, 
        args.gene_file, 
        args.prediction_file, 
        args.algorithm_id, 
        args.organism,
        args.go_category,
        args.version)

