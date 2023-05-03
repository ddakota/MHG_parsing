from pathlib import Path


def open_ptb(treebank: Path):
    
    with open(treebank) as f:
        trees = f.read()
        trees = trees.split("\n")

    return trees


def read_conllu(conllu_file: Path):

    with open(conllu_file) as conllu_treebank:
        treebank = conllu_treebank.read()
        trees = treebank.split("\n\n")
    return trees
