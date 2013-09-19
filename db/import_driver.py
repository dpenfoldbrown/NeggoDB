"""
A simple driver for running prediction imports. Runs per organism on all files.
@auth dpb
@date 9/19/2013
"""

def run_organism(organism, base_dir):
    import os
    from db.prediction_importer import import_predictions

    gene_dir = os.path.join(base_dir, "gene_names")
    go_dir = os.path.join(base_dir, "go_terms")
    prediction_dir = os.path.join(base_dir, "predictions")

    Organisms = ["arabidopsis", "human", "mouse", "rice", "worm", "yeast"]
    Algorithms = {
        "Rocchio": 1, 
        "SNOB": 2,
        "NETL": 3
    }
    GO_cats = ["BP", "MF", "CC"]

    if organism not in Organisms:
        raise Exception("Given organism {0} not valid. Options: {1}".format(organism, Organisms))

    gene_file = os.path.join(gene_dir, "Gene_Names_{0}.txt".format(organism))

    for alg in Algorithms:
        for cat in GO_cats:
            go_file = os.path.join(go_dir, "GO_Terms_{0}_{1}.txt".format(organism, cat))
            prediction_file = os.path.join(prediction_dir, "{0}_{1}_{2}.txt".format(alg, organism, cat))
            
            print "Importing files {0}, {1}, {2}".format(gene_file, go_file, prediction_file)
            # (go_file, gene_file, prediction_file, algorithm_id, organism, go_category, version)
            import_predictions(go_file, gene_file, prediction_file, Algorithms[a], organism, cat, 1)
    print "Complete"


if __name__ == "__main__":
    import os
    import argparse
    parser = argparse.ArgumentParser(description="Import prediction file driver")
    parser.add_argument("-o", "--organism", action="store", dest="organism", required=True,
        help="The organism to import. Options: arabidopsis, human, mouse, rice, worm, yeast")
    parser.add_argument("-d", "--dir", action="store", dest="dir", required=False, default="/data/noGO/",
        help="The base directory containing subdirs for all files (gene name, go term, and predictions")
    args = parser.parse_args()
    os.path.isdir(args.dir)
    run_organism(args.organism, args.dir)