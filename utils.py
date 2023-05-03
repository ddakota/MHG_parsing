from pathlib import Path


def open_ptb(treebank: Path):
    
    with open(treebank) as f:
        trees = f.read()
        trees = trees.split("\n")

    return trees
