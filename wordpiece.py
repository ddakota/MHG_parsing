from transformers import BertTokenizer, AutoTokenizer
from typing import List
from utils import open_ptb
import re

def wp_512_check(treebank_sentences: List,
                 tokenizer: str):

    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    treebank = open_ptb(treebank_sentences)

    treebank_terminals = []
    for tree in treebank:

        terminals = re.findall(r"[^\s]+\)", tree)
        terminals = [w.translate(str.maketrans("", "", "\)")) for w in terminals]
        treebank_terminals.append(" ".join(terminals))
        
    sent_id = 1
    for sentence in treebank_terminals:
        wordpiece = tokenizer.tokenize(sentence)
        if len(wordpiece) > 512:
            print(sent_id, len(wordpiece))
            print(sentence)
            print(treebank[sent_id-1])
        sent_id += 1


