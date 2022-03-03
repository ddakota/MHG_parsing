from pathlib import Path
from typing import List

import typer

from extract import extract_export
from pos import compare_pos_tags, replace_pos_tags
from wordpiece import wp_512_check

app = typer.Typer()


@app.command()
def extract_mhg(
    treebank: Path,
    outputfile: str,
):
    '''This commands reads in the export.txt file generated from the MHG
    treebank and returns it in an PTB style
    '''
    assert treebank.exists()
    extract_export(treebank, outputfile)


@app.command()
def wordpiece_512check(
    sentences: Path,
):
    '''This commands reads in sentences (1 per line) and calculates the
    number of wordpieces to see which sentences are > 512.
    '''
    assert sentences.exists()
    wp_512_check(sentences)


@app.command()
def replace_pos(
    treebank1: Path,
    treebank2: Path,
):
    '''This command replaces the POS tags from treebank with that
    of the other treebank
    '''
    assert treebank1.exists()
    assert treebank2.exists()
    replace_pos_tags(treebank1, treebank2)


@app.command()
def compare_pos(
    treebank1: Path,
    treebank2: Path,
):
    '''This command compares the POS accuracy of one treebank against
    the other. The output file (pos_acc.txt) is currently hardcoded.
    '''
    assert treebank1.exists()
    assert treebank2.exists()
    compare_pos_tags(treebank1, treebank2)


if __name__ == "__main__":
    app()
