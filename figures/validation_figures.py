"""
Generate figures for validation data
@auth dpb
@date 9/17/2013
"""

import matplotlib.pyplot as plt

R_x = [6, 32, 64, 160, 319, 638, 957, 1275]
R_y = [0,  0,  0,   0,   0,    2,  2,    4]

N_x = [6, 32, 64, 160, 319, 638, 957, 1275]
N_y = [1,  2,  3,   1,   0,    3,  1,    4]

S_x = [6, 32, 64, 160, 319, 638, 957, 1275]
S_y = [1,  1,  0,   0,   0,    1,  2,    3]

rand_x = [6, 32, 64, 160, 319, 638, 957, 1275]
rand_y = [4,  5,  5,   2,   6,   8,  4,     7]

#TODO: Do not use scale data to pad charts

xmax = max(R_x + N_x + S_x + rand_x)
ymax = max(R_y + N_y + S_y + rand_y)
xscale = int(xmax + (xmax * 0.01))
yscale = int(ymax + (ymax * 0.4))
scale_x = [0, xscale]
scale_y = [0, yscale]

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.75, 0.75])

ax.set_title("Sample Accuracy: GO <GoID>, <GO Category>, <Organism>")
ax.set_xlabel("Number of selected negative examples")
ax.set_ylabel("Number of erroneous negative examples")

ax.plot(scale_x, scale_y, ' ')
ax.plot(R_x, R_y, 'm-', linewidth=2.0, label="Rocchio")
ax.plot(N_x, N_y, 'r-', linewidth=2.0, label="NETL")
ax.plot(S_x, S_y, 'y-', linewidth=2.0, label="SNOB")
ax.plot(rand_x, rand_y, 'b-.', linewidth=2.0, label="Random")

ax.legend(loc='upper left')

plt.show()
plt.close()
