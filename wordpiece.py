from transformers import BertTokenizer

from utils import openPTB


def wp_512_check(treebank_sentences):

    tokenizer = BertTokenizer.from_pretrained("bert-base-cased")
    sentences = openPTB(treebank_sentences)

    sentid = 1
    for sentence in sentences:
        wordpiece = tokenizer.tokenize(sentence)
        # print (wordpiece)
        if len(wordpiece) > 512:
            print(sentid)
            # print (sentence)
        sentid += 1
