from transformers import BertTokenizer, AutoTokenizer
from typing import List
from utils import open_ptb


def wp_512_check(treebank_sentences: List,
                 tokenizer: str):

    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    sentences = open_ptb(treebank_sentences)
    sent_id = 1
    for sentence in sentences:
        wordpiece = tokenizer.tokenize(sentence)
        if len(wordpiece) > 512:
            print(sent_id, len(wordpiece))
        sent_id += 1


