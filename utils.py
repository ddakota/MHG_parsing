def openPTB(treebank):

    with open(treebank) as f:
        trees = f.read()
        trees = trees.split("\n")

    return trees
