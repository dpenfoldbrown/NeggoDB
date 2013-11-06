"""
Quick script to generate pre-generated images for NoGO Validation data.
24 figures generated. 1/organism (6), AND 1/organism x branch  (18).

Uses data from validation average files (currently on handbanana).

@auth dpb
@date 11/05/2013
"""

from os import path
from validation import singleGO_validation_figure

# Config
Organisms = {
    "arabidopsis": "Arabidopsis3702",
    "human": "Human9606",
    "mouse": "Mouse10090",
    "rice": "Rice39947",
    "worm": "Worm6239",
    "yeast": "Yeast4932"
}
Categories = ["BP", "CC", "MF"]
Algorithms = ["Rocchio", "Ne", "SNOB", "Random"]

file_dir = "/Users/dpb/data/nogo/validation"
file_prefix = "Average_Validation"


# Utility functions
def parse_validation_file(filename):
    """
    Parses a given Average Validation file (format: single line, 8 points tab-separated). Returns
    a list of x-values and corresponding list of y-values.
    """
    x_vals = []
    y_vals = []
    with open(filename) as handle:
        points = handle.next().rstrip().split()
        for point in points:
            values = point.replace("(", "").replace(")", "").split(',')
            if len(values) != 2:
                raise Exception("Point string {0} not in correct format".format(point))
            x_val = float(values[0])
            y_val = float(values[1])
            x_vals.append(x_val)
            y_vals.append(y_val)
    assert len(x_vals) == 8
    assert len(y_vals) == 8
    return (x_vals, y_vals)

# Generate average plot across all organisms and categories
rocc_file = path.join(file_dir, "{0}_{1}.txt".format(file_prefix, "Rocchio"))
netl_file = path.join(file_dir, "{0}_{1}.txt".format(file_prefix, "Ne"))
snob_file = path.join(file_dir, "{0}_{1}.txt".format(file_prefix, "SNOB"))
rand_file = path.join(file_dir, "{0}_{1}.txt".format(file_prefix, "Random"))

rocc_x, rocc_y = parse_validation_file(rocc_file)
netl_x, netl_y = parse_validation_file(netl_file)
snob_x, snob_y = parse_validation_file(snob_file)
rand_x, rand_y = parse_validation_file(rand_file)

fig_file = "AllOrganismAverage.png"
singleGO_validation_figure(rocc_x, rocc_y, netl_x, netl_y, snob_x, snob_y, rand_x, rand_y, 
    go_term="", go_cat="", organism="Average Accuracy", outfile=fig_file, show=False)
print "Completed All Average plot: {0}".format(fig_file)

# Generate plots for all organisms and categories
for organism in Organisms:
    # Generate organism plot and save
    rocc_file = path.join(file_dir, "{0}_{1}_{2}.txt".format(file_prefix, "Rocchio", organism))
    netl_file = path.join(file_dir, "{0}_{1}_{2}.txt".format(file_prefix, "Ne", organism))
    snob_file = path.join(file_dir, "{0}_{1}_{2}.txt".format(file_prefix, "SNOB", organism))
    rand_file = path.join(file_dir, "{0}_{1}_{2}.txt".format(file_prefix, "Random", organism))

    rocc_x, rocc_y = parse_validation_file(rocc_file)
    netl_x, netl_y = parse_validation_file(netl_file)
    snob_x, snob_y = parse_validation_file(snob_file)
    rand_x, rand_y = parse_validation_file(rand_file)

    fig_file = "{0}.png".format(Organisms[organism])
    singleGO_validation_figure(rocc_x, rocc_y, netl_x, netl_y, snob_x, snob_y, rand_x, rand_y, 
        go_term="", go_cat="", organism=Organisms[organism], outfile=fig_file, show=False)

    # Loop through Categories, generate plots for each
    for cat in Categories:

        rocc_file = path.join(file_dir, "{0}_{1}_{2}_{3}.txt".format(file_prefix, "Rocchio", organism, cat))
        netl_file = path.join(file_dir, "{0}_{1}_{2}_{3}.txt".format(file_prefix, "Ne", organism, cat))
        snob_file = path.join(file_dir, "{0}_{1}_{2}_{3}.txt".format(file_prefix, "SNOB", organism, cat))
        rand_file = path.join(file_dir, "{0}_{1}_{2}_{3}.txt".format(file_prefix, "Random", organism, cat))

        rocc_x, rocc_y = parse_validation_file(rocc_file)
        netl_x, netl_y = parse_validation_file(netl_file)
        snob_x, snob_y = parse_validation_file(snob_file)
        rand_x, rand_y = parse_validation_file(rand_file)

        fig_file = "{0}_{1}.png".format(Organisms[organism], cat)
        singleGO_validation_figure(rocc_x, rocc_y, netl_x, netl_y, snob_x, snob_y, rand_x, rand_y,
            go_term="", go_cat=cat, organism=Organisms[organism], outfile=fig_file, show=False)

    print "Completed plots for {0}".format(organism)
print "Generating plots complete"



