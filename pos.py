import re
from pathlib import Path
from utils import open_ptb


def replace_pos_tags(treebank1: Path,
                     treebank2: Path):

    """This function takes a gold file with pos tagss and lemma information and inserts this information into a parsed output

    Args:
    treebank1: gold treebank with pos and lemmas
    treebank2: parsed treebank with tags and terminals to replace

    Returns:
    a parsed file with inserted gold pos tags and lemmas

    
    """
    
    trees1 = open_ptb(treebank1)
    trees2 = open_ptb(treebank2)

    replaced_sentences = []
    index = 1
    
    for tree1, tree2 in zip(trees1, trees2):

        tree1 = tree1.replace(" (", "(")
        tree2 = tree2.replace(" (", "(")  # this is done because the parsed output has spaces

        tags1 = re.findall("([^\(]+)\s", tree1)
        tags2 = re.findall("([^\(]+)\s", tree2)

        terminals1 = re.findall("\s[^\)]+", tree1)
        terminals2 = re.findall("\s[^\)]+", tree2)

        assert (len(tags1) == len(tags2))
        assert (len(terminals1) == len(terminals2))

        replaced = []
        if tree2.split():
            for i in tree2.split()[:-1]:
                tags = re.search("[^\(]+$", i)
                terminals = re.search("^[^\)\(]+", i)

                if tags and not terminals:
                    t1 = tags1.pop(0)
                    t2_replaced = re.sub(r"[^\(]+$", t1, i)
                    replaced.append(t2_replaced)
                if terminals and not tags:
                    t1 = terminals1.pop(0)
                    t2_replaced = re.sub(r"^[^\)\(]+", t1, i)
                    replaced.append(t2_replaced.lstrip())
                if tags and terminals:
                    t1 = tags1.pop(0)
                    t2_replaced = re.sub(r"[^\(]+$", t1, i)
                    t1 = terminals1.pop(0)
                    t3_replaced = re.sub(r"^[^\)\(]+", t1, t2_replaced)
                    replaced.append(t3_replaced.lstrip())
    
            replaced.append(tree2.split()[-1])


        replaced_sentences.append(" ".join(replaced))

        index += 1
        
    with open(str(treebank2) + "_replaced-with-gold-pos222", "w") as f:

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
