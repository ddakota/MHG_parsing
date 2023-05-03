# MHG_parsing# MHG_parsing
This repo contains ode and technical information for assisting in creating the Indiana Parsed Corpus of Historical High German

The app.py file contains sevral stand-alone commands that assist in various data transformations:

#### To extract single line ptb style treebank from the gold IPCHG treebank file (note: the user must specify the file name for extracted_treebank_name):
```
python app.py extract-gold 1533_johann_fierrabras.ver0_2.txt 1533_johann_fierrabras.ver0_2.brackets
```

This returns 1533_johann_fierrabras.ver0_2.brackets

#### To chceck how many subword tokens exist in a sentence in a ptb treebank (note: the user must specify the tokenizer (e.g.,dbmdz/bert-base-german-cased)  :
```
python app.py wordpiece-512check bert-tokenizer 1533_johann_fierrabras.ver0_2.brackets
```

This prints out to the screen the sentence number (i.e., line number), the length of the sentence based on subword tokens, the text setence, and the tree for all all sentences that are >512 subword units in length.


#### Many parsers need a vritual root attached to the top of the tree, but are not annotated with these. To add a vroot to a treebank:

```
python app.py add-treebank-root 1533_johann_fierrabras.ver0_2.brackets
```

This returns a file: 1533_johann_fierrabras.ver0_2_vroot.brackets


#### To replace parsed files with the gold POS tags:

```
python app.py replace-pos 1533_johann_fierrabras.ver0_2.brackets 1533_johann_fierrabras.ver0_2.brackets.parsed
```

This returns a file: 1533_johann_fierrabras.ver0_2.brackets.parsed_replaced-with-gold-pos


## Additional Tools

### treetools

We use treetools (https://github.com/wmaier/treetools) to extract trees from negra format and resolve their annotation issues, resulting in a single line ptb style trees
After downloading and installing treetools, use the following command:

```
treetools transform UlrichFüetrer.negra UlrichFüetrer.brackets --trans root_attach negra_mark_heads boyd_split raising --src-format export --dest-format brackets --src-enc iso-8859-1 --dest-enc utf8
```

### C6C
We use C6C (https://github.com/rubcompling/C6C) to extract trees from xml (more specifically coraxmlrefbo) and transform them into conlluplus formats (which we then will subsequently convert later to readable ptb format)

```
python C6C.py convert input_directory/ -i coraxmlrefbo -e conlluplus output_directory/
```

