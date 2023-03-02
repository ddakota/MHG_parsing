from pathlib import Path
import typer

from extract import extract_export, extract_test, extract_terminals
from pos import compare_pos_tags, replace_pos_tags
from data import get_splits, add_root
from wordpiece import wp_512_check

app = typer.Typer()


@app.command()
def extract_mhg_export(
        treebank: Path,
        output_file: str,
):
    """This commands reads in the export.txt file generated from the MHG
    treebank and returns it in an PTB style
    """
    assert treebank.exists()
    extract_export(treebank, output_file)


@app.command()
def extract_gold(
        treebank: Path,
        output_file: str,
):
    """This commands reads in the export.txt file generated from the MHG
    treebank and returns it in an PTB style
    """
    assert treebank.exists()
    extract_test(treebank, output_file)


@app.command()
def wordpiece_512check(
        sentences: Path,
        tokenizer: str,
):
    """This commands reads in sentences (1 per line) and calculates the
    number of wordpieces to see which sentences are > 512.
    """
    assert sentences.exists()
    wp_512_check(sentences, tokenizer)


@app.command()
def replace_pos(
        treebank1: Path,
        treebank2: Path,
):
    """This command replaces the POS tags from treebank with that
    of the other treebank
    """
    assert treebank1.exists()
    assert treebank2.exists()
    replace_pos_tags(treebank1, treebank2)


@app.command()
def compare_pos(
        treebank1: Path,
        treebank2: Path,
):
    """This command compares the POS accuracy of one treebank against
    the other. The output file (pos_acc.txt) is currently hardcoded.
    """
    assert treebank1.exists()
    assert treebank2.exists()
    compare_pos_tags(treebank1, treebank2)


@app.command()
def extract_treebank_terminals(
        treebank: Path,
):
    """This command compares the POS accuracy of one treebank against
    the other. The output file (pos_acc.txt) is currently hardcoded.
    """
    assert treebank.exists()
    extract_terminals(treebank)


@app.command()
def add_treebank_root(
        treebank: Path,
):
    """This command compares the POS accuracy of one treebank against
    the other. The output file (pos_acc.txt) is currently hardcoded.
    """
    assert treebank.exists()
    add_root(treebank)


@app.command()
def make_splits(
        treebank: Path,
):
    """This commands reads in the export.txt file generated from the MHG
    treebank and returns it in an PTB style

    Args:
        treebank: path to treebank file
    Returns:
        Train, dev, and test splits for a treebank
    """
    assert treebank.exists()
    get_splits(treebank)


if __name__ == "__main__":
    app()
