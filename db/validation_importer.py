"""
A script to import validation plot information from validation files (/data/NoGO/validation/)
File name: Validation_<Alg>_<organism>_<GOcat>.txt
File format: 9-column. Discard first column. Next 8 columns, 8 validation plot figures

@auth dpb
@date 10/16/2013
"""


def parse_pointstr(pointstr):
    """Parses a string of form '(1,2)' and returns a tuple: (1,2) of ints"""
    points = pointstr.rstrip().replace("(", "").replace(")", "").split(',')
    if len(points) != 2:
        raise Exception("Point string {0} not in correct format".format(pointstr))
    return map(int, points)


import os
from db.nogoDB import Session, push_to_db, ValidationPlot
from db.prediction_importer import build_index_dict


algorithms = { 'Rocchio': 1, 'SNOB': 2, 'Ne': 3, 'Random': 4 }
organisms = ['arabidopsis', 'human', 'mouse', 'rice', 'worm', 'yeast']
categories = ['BP', 'CC', 'MF']
version = 1

go_dir = "/data/noGO/go_terms"
validation_dir = "/data/noGO/validation"

failed_files = []

session = Session()

# File loop
for algorithm in algorithms:
    for organism in organisms:
        for category in categories:

            # Get term index dict
            go_filename = os.path.join(go_dir, "GO_Terms_{0}_{1}.txt".format(organism, category))
            go_dict = build_index_dict(go_filename, start=1, header=False)

            # Open validation file
            filename = os.path.join(validation_dir, "Validation_{0}_{1}_{2}.txt".format(algorithm, organism, category))
            print "Importing Validation numbers from file {0}".format(filename)
            try:
                handle = open(filename)
            except Exception as e:
                print "Failed to open file {0}".format(filename)
                print "Exception: {0}".format(e)
                failed_files.append(filename)
                continue

            # Import all lines in file (except those with only 0 as a row)
            row_index = 1
            for line in handle:
                columns = line.rstrip().split()
                if len(columns) < 9:
                    print "No validation data for line '{0}'. Skipping...".format(line)
                    continue
                columns = columns[1:]
                points = map(parse_pointstr, columns)

                v = ValidationPlot(
                    organism=organism,
                    go_category=category,
                    algorithm_id=algorithms[algorithm],
                    version_id=version,
                    go_id=go_dict[row_index],
                    p1_x=points[0][0], p1_y=points[0][1],
                    p2_x=points[1][0], p2_y=points[1][1],
                    p3_x=points[2][0], p3_y=points[2][1],
                    p4_x=points[3][0], p4_y=points[3][1],
                    p5_x=points[4][0], p5_y=points[4][1],
                    p6_x=points[5][0], p6_y=points[5][1],
                    p7_x=points[6][0], p7_y=points[6][1],
                    p8_x=points[7][0], p8_y=points[7][1],
                )

                print "Pushing validation plot: {0}".format(v)
                print "\tPoints: {0}".format(points)

                #push_to_db(session, v, exception_str="Failed pushing plot for {0},{1},{2},{3} to DB".format(
                #    algorithm, organism, category, go_dict[row_index]))
                
                row_index += 1

            handle.close()

print "Complete"















