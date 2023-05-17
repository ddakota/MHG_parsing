import re
from nltk.tree import Tree
from pathlib import Path

from utils import open_ptb, read_conllu


def extract_export(export_file: Path,
                   output_file: str):

    with open(export_file, "r") as f:
        export_sentences = f.read()

    sentences = re.findall("\*/([^~]+)", export_sentences)
    sentence_ids = re.findall(r"\(ID [^/]+\)", export_sentences)
    ptb_format = []
    for sentence in sentences[1:-1]:
        # This is used to figure out which sentence is missing.
        sentence_id = re.search("(\(ID [^\)]+\))", sentence)
        if sentence_id.group(1) + ")" in sentence_ids:
            index = sentence_ids.index(sentence_id.group(1) + ")")
            sentence_ids.pop(index)

        remove_id = re.sub("\(ID [^\)]+\)", "", sentence.lstrip().rstrip().rstrip("/"))
        remove_linebreaks = re.sub("\n", "", remove_id)
        remove_spaces = re.sub("\s+", " ", remove_linebreaks)
        remove_meta = re.sub("\(META.*?\)\) ", "", remove_spaces)
        remove_ortho = re.sub("\s+\(ORTHO ([^\)]+)\)", r" \1", remove_meta)
        remove_traces = re.sub("\s?\([^\(]+\*(ICH|T)\*\)", "", remove_ortho)
        remove_con_advprsp = re.sub("\s\(ADVP-RSP \*con\*\)", "", remove_traces)
        remove_npsbj_null = re.sub(
            "\s\(NP-SBJ \*(con|pro|exp|)\*\)", "", remove_con_advprsp
        )
        remove_star_null = re.sub("\([^\(]+ \*\)", "", remove_npsbj_null)
        remove_footer = re.sub("\/\*FOOTER.*", "", remove_star_null)
        remove_0s = re.sub("\([^\(]+ 0\)", "", remove_footer)
        t = Tree.fromstring(remove_0s)
        ptb_format.append(remove_0s)

    with open(output_file, "w") as f:
        for tree in ptb_format:
            f.write(tree + "\n")


def extract_enhg_gold(export_file: Path,
                 output_file: str):
    """todo make removing morph optional"""
    
    with open(export_file, "r") as f:
        export_sentences = f.read().split("\n\n")
    print(len(export_sentences))

    ptb_format = []
    sent_id = 1

    for sentence in export_sentences:
        remove_id = re.sub("\(ID [^\)]+\)", "", sentence.lstrip().rstrip().rstrip("/"))
        remove_code = re.sub("\(CODE([^\s]+)?", "(META", remove_id)  # converts code tags to meta tags
        remove_linebreaks = re.sub("\n", "", remove_code)
        remove_traces = re.sub("\s?\([^\(]+\*(ICH|T)\*[^\)]+\)", "", remove_linebreaks)
        remove_morph = re.sub("(\^[^\s]+)", " ", remove_traces)
        remove_0s = re.sub("\([^\(]+ 0\)", "", remove_morph)
        remove_con = re.sub("\([^\(]+ \*con\*\)", "", remove_0s)
        remove_exp = re.sub("\([^\(]+ \*exp\*\)", "", remove_con)
        remove_pro = re.sub("\([^\(]+ \*pro\*\)", "", remove_exp)
        ptb = " ".join(remove_pro.split())
        try:  # checks if correctly formed tree based on nltk tree
            t = Tree.fromstring(ptb)
            sent_id += 1
            ptb_format.append(ptb)
        except ValueError:
            print(sent_id)
            print(ptb)

    with open(output_file, "w") as f:
        for tree in ptb_format:
            f.write(tree + "\n")


def extract_terminals(treebank_file: Path):

    treebank = open_ptb(treebank_file)

    treebank_terminals = []
    for tree in treebank:

        terminals = re.findall(r"[^\s]+\)", tree)
        terminals = [w.translate(str.maketrans("", "", "\)")) for w in terminals]
        treebank_terminals.append(terminals)

    with open(str(treebank_file) + ".terminals", "w") as f:
        for tree in treebank_terminals:
            f.write(" ".join(tree) + "\n")


def extract_conlluplus(treebank_file: Path,
                       morph: False):

    trees = read_conllu(treebank_file)
    all_ptb_trees = []
    print(len(trees))
    for tree in trees:
        ptb_tree = []
        rows = tree.split("\n")
        c = 0
        for row in rows:
            #print(row)
            if row == "": # this is because the last sentence has a empty single row
                continue
            if row[0].startswith("#"): # skips the meta data
                continue

            columns = row.split("\t")
            if "-" not in columns[0]: #1 word, 2 lemma, 10 ascii, 14 boundary, 20 morph, 21 pos
                columns[20] = re.sub("_", "", columns[20])
                columns[20] = re.sub("\*\.", "", columns[20])
                columns[20] = re.sub("\.", "^", columns[20])
                columns[20] = re.sub("\*", "", columns[20])
                columns[2] = re.sub("\(", "<", columns[2])
                columns[2] = re.sub("\)", ">", columns[2])
                columns[2] = re.sub(" ", "", columns[2])
                columns[10] = re.sub("\(\)","<>", columns[10])
                columns[10] = re.sub("\(","<", columns[10])
                columns[10] = re.sub("\)",">", columns[10])



                if not morph:
                    #print (columns)
                    # # pos word
                    if columns[14] == "_":
                        #print("14 == _")
                        if columns[20] != "":
                            c += 1
                            ptb_tree.append("("+columns[21]+" "+columns[10]+")")
                        else:
                            c += 1
                            ptb_tree.append("("+columns[21]+" "+columns[10]+")")
                    if columns[14] != "_":
                        #print("14 != _")
                        #print(columns[14])
                        boundaries = columns[14].split()
                        #print(boundaries)
                        if columns[20] != "":
                            #print("columns 20 != ''")
                            c += 1
                            ptb_tree.append("("+columns[21]+" "+columns[10]+")")
                            for boundary in boundaries:
                                if boundary != "|":
                                    ptb_tree.append("(META " + boundary[1:])
                                    #print(ptb_tree)
                                if boundary == "|":
                                    ptb_tree.append("(META |)")
                                    #print(ptb_tree)
                                    #input()

                        else:
                            #print("else")
                            boundaries = columns[14].split()
                            c += 1
                            ptb_tree.append("("+columns[21]+" "+columns[10]+")")
                            for boundary in boundaries:
                                if boundary != "|":
                                    ptb_tree.append("(META " + boundary[1:])
                                    #print(ptb_tree)
                                if boundary == "|":
                                    ptb_tree.append("(META |)")
                                    #print(ptb_tree)
                                    #input()
                            #ptb_tree.append("(META " + columns[14][1:])

                    #input()
                if morph:
                    # # pos+morph word=lemma
                    if columns[14] == "_":
                        boundaries = columns[14].split()

                        if columns[20] != "":
                            c += 1
                            ptb_tree.append("("+columns[21]+"^"+columns[20]+" "+columns[10]+"="+columns[2]+")")
                        else:
                            c += 1
                            ptb_tree.append("("+columns[21]+" "+columns[10]+"="+columns[2]+")")
                    if columns[14] != "_":


                        if columns[20] != "":
                            boundaries = columns[14].split()

                            c += 1
                            ptb_tree.append("("+columns[21]+"^"+columns[20]+" "+columns[10]+"="+columns[2]+")")
                            for boundary in boundaries:
                                if boundary != "|":
                                    ptb_tree.append("(META " + boundary[1:])
                                    #print(ptb_tree)
                                if boundary == "|":
                                    ptb_tree.append("(META |)")
                                    #print(ptb_tree)
                                    #input()
                            #ptb_tree.append("(META " + columns[14][1:])

                        else:
                            c += 1
                            boundaries = columns[14].split()

                            ptb_tree.append("("+columns[21]+" "+columns[10]+"="+columns[2]+")")
                            for boundary in boundaries:
                                if boundary != "|":
                                    ptb_tree.append("(META " + boundary[1:])
                                    #print(ptb_tree)
                                if boundary == "|":
                                    ptb_tree.append("(META |)")
                                    #print(ptb_tree)
                                    #input()
                            #ptb_tree.append("(META " + columns[14][1:])
        #print(ptb_tree)
        #input()
        all_ptb_trees.append(" ".join(ptb_tree))

    if not morph:
        with open(str(treebank_file) + ".brackets_gold", "w") as f:
            for tree in all_ptb_trees:
                f.write("(VROOT " + tree + ")\n")

    if morph:
        with open(str(treebank_file) + ".brackets_gold_w_morph_and_lemma", "w") as f:
            for tree in all_ptb_trees:
                f.write("(VROOT " + tree + ")\n")
