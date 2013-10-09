NoGO DB
=======

Web resource for Gene/GO negative example exposition

Initially, will use:

Backend: Python, Flask

Frontend: jQuery, Knockout, Bootstrap (or other fancy-pants deal)


Algorithms
==========

Rocchio
Algorithm adapted from a text-mining PU algorithm in [Rocchio, 1971]. The original method has been adapted from a binary decision to a score, allowing a variable number of negative examples to be chosen.

SNOB (Selection of Negatives Through Observed)
SNOB chooses negative examples by scoring proteins based on the empirical conditional probability of the function in question occurring, based on the other annotations in the protein.

NETL (Negative Examples from Topic Likelihood)
NETL selects negative examples by creating a latent topic model for each function, and then scoring a protein by the similarity of its topic profile to the average topic profile of the positive class of proteins annotated with the function in question.


