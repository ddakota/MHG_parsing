import re


def extract_export(exportFile, outputFile):

    with open(exportFile, "r") as f:
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
        ptb_format.append(remove_0s)

    with open(outputFile, "w") as f:
        for tree in ptb_format:
            f.write(tree + "\n")
