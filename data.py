import random
import re
from pathlib import Path
from utils import open_ptb


def add_root(treebank: Path):
    """this adds roots to languages that have no roots to make numbers match, assumes ptb format"""

    treebank_file = open_ptb(treebank)
    rooted_trees = []
    for tree in treebank_file:
        tree = re.sub("^\(", "(VROOT", tree)
        rooted_trees.append(tree)

    with open(str(treebank)[:-4] + "_vroot.ptb", "w") as f:
        for s in rooted_trees:
            f.write(s + "\n")


def get_splits(treebank: Path):
    """creates data splits for treebank"""

    ptb = open_ptb(treebank)
    random.shuffle(ptb)

    train = ptb[:100]
    dev = ptb[100:150]
    test = ptb[151:]

    with open(str(treebank)[:3] + "_train" + str(treebank)[16:], "w") as f:
        for s in train:
            f.write(s + "\n")
    with open(str(treebank)[:3] + "_dev" + str(treebank)[16:], "w") as f:
        for s in dev:
            f.write(s + "\n")
    with open(str(treebank)[:3] + "_test" + str(treebank)[16:], "w") as f:
        for s in test:
            f.write(s + "\n")
