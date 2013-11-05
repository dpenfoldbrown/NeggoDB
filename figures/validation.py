"""
Generate figures for validation data
@auth dpb
@date 9/17/2013
"""

import matplotlib.pyplot as plt

def singleGO_validation_figure(r_x, r_y, n_x, n_y, s_x, s_y, rand_x, rand_y, go_term="GO:0000000", 
		go_cat="NN", organism="Unknown", outfile=None, show=False):
	
	xmax = max(r_x + n_x + s_x + rand_x)
	ymax = max(r_y + n_y + s_y + rand_y)
	xscale = int(xmax + (xmax * 0.01))
	yscale = int(ymax + (ymax * 0.20))

	plt.title("Sample Accuracy: {0} {1} {2}".format(organism, go_cat, go_term))
	plt.xlabel("Number of selected negative examples")
	plt.ylabel("Number of erroneous negative examples")

	plt.plot(r_x, r_y, 'm-', linewidth=2.0, label="Rocchio")
	plt.plot(n_x, n_y, 'r-', linewidth=2.0, label="NETL")
	plt.plot(s_x, s_y, 'y-', linewidth=2.0, label="SNOB")
	plt.plot(rand_x, rand_y, 'b-.', linewidth=2.0, label="Random")

	plt.axis([0, xscale, -1, yscale])
	plt.legend(loc='upper left')

	if outfile:
		plt.savefig(outfile)
	if show:
		plt.show()
	plt.close()


if __name__ == "__main__":

	# Sample data
	R_x = [6, 32, 64, 160, 319, 638, 957, 1275]
	R_y = [0,  0,  0,   0,   0,    2,  2,    4]

	N_x = [6, 32, 64, 160, 319, 638, 957, 1275]
	N_y = [1,  2,  3,   3,   3,    3,  4,    4]

	S_x = [6, 32, 64, 160, 319, 638, 957, 1275]
	S_y = [0,  1,  2,   2,   3,    4,  5,    5]

	rand_x = [6, 32, 64, 160, 319, 638, 957, 1275]
	rand_y = [4,  5,  5,   6,   6,   8,  9,    10]

	singleGO_validation_figure(
		R_x, R_y, 
		N_x, N_y, 
		S_x, S_y, 
		rand_x, rand_y, 
		go_term="GO:000TEST", 
		go_cat="TT", 
		organism="TestOrg", 
		show=True,
		outfile="test_figure_01.png")







