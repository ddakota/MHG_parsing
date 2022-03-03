import re

from utils import openPTB


def replace_pos_tags(treebank1, treebank2):

    trees1 = openPTB(treebank1)
    trees2 = openPTB(treebank2)

    replaced_sentences = []

    for tree1, tree2 in zip(trees1, trees2):

        tags1 = re.findall("([^\(]+)\s", tree1)
        #this is done because the parsed output has spaces
        tree2 = tree2.replace(" (", "(")
        tags2 = re.findall("([^\(]+)\s", tree2)
        assert(len(tags1) == len(tags2))
        
        replaced_tags = []
        if tree2.split():
            for i in tree2.split()[:-1]:

                tags = re.search("[^\(]+$", i)

                if tags:
                    t1 = tags1.pop(0)
                    t2_replaced = re.sub(r"[^\(]+$", t1, i)
                    replaced_tags.append(t2_replaced)
                else:
                    replaced_tags.append(i)

            replaced_tags.append(tree2.split()[-1])
        replaced_sentences.append(" ".join(replaced_tags))

    with open(str(treebank2) + "_replaced-with-gold-pos", "w") as f:

        for s in replaced_sentences:
            f.write(s + "\n")


def compare_pos_tags(treebank1, treebank2):

    trees1 = openPTB(treebank1)
    trees2 = openPTB(treebank2)

    posDict = {}

    for tree1, tree2 in zip(trees1, trees2):

        tags1 = re.findall("([^\(]+)\s", tree1)
        #this is done because the parsed output has spaces
        tree2 = tree2.replace(" (", "(")
        tags2 = re.findall("([^\(]+)\s", tree2)
        assert(len(tags1) == len(tags2))


        for tag1, tag2 in zip(tags1, tags2):
            if tag1 in posDict:
                if tag2 in posDict[tag1]:
                    posDict[tag1][tag2] += 1
                else:
                    posDict[tag1][tag2] = 1
            else:
                posDict[tag1] = {}
                posDict[tag1][tag2] = 1

    with open("pos_acc.txt", "w") as f:
        for k, v in posDict.items():
            total = 0
            gold = 0
            f.write("tag: " + k + "\n")
            for kk, vv in sorted(posDict[k].items(), key=lambda x: x[1], reverse=True):
                f.write(kk + "\t" + str(posDict[k][kk]) + "\n")
                total += posDict[k][kk]
                if kk == k:
                    gold = posDict[k][kk]
            f.write("tag accuracy: " + str(gold / total) + "\n\n")
