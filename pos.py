import re
from pathlib import Path
from utils import open_ptb


def replace_pos_tags(treebank1: Path,
                     treebank2: Path):

    trees1 = open_ptb(treebank1)
    trees2 = open_ptb(treebank2)

    replaced_sentences = []

    for tree1, tree2 in zip(trees1, trees2):

        tags1 = re.findall("([^\(]+)\s", tree1)
        tree2 = tree2.replace(" (", "(")  # this is done because the parsed output has spaces

        tags2 = re.findall("([^\(]+)\s", tree2)
        assert (len(tags1) == len(tags2))

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


def compare_pos_tags(treebank1: Path,
                     treebank2: Path):

    trees1 = open_ptb(treebank1)
    trees2 = open_ptb(treebank2)

    pos_dict = {}

    for tree1, tree2 in zip(trees1, trees2):

        tags1 = re.findall("([^\(]+)\s", tree1)
        tree2 = tree2.replace(" (", "(")  # this is done because the parsed output has spaces
        tags2 = re.findall("([^\(]+)\s", tree2)
        assert (len(tags1) == len(tags2))

        for tag1, tag2 in zip(tags1, tags2):
            if tag1 in pos_dict:
                if tag2 in pos_dict[tag1]:
                    pos_dict[tag1][tag2] += 1
                else:
                    pos_dict[tag1][tag2] = 1
            else:
                pos_dict[tag1] = {}
                pos_dict[tag1][tag2] = 1

    with open("pos_acc.txt", "w") as f:
        for k, v in pos_dict.items():
            total = 0
            gold = 0
            f.write("tag: " + k + "\n")
            for kk, vv in sorted(pos_dict[k].items(), key=lambda x: x[1], reverse=True):
                f.write(kk + "\t" + str(pos_dict[k][kk]) + "\n")
                total += pos_dict[k][kk]
                if kk == k:
                    gold = pos_dict[k][kk]
            f.write("tag accuracy: " + str(gold / total) + "\n\n")
