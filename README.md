# MHG_parsing# MHG_parsing
This repo contains ode and technical information for assisting in creating the Indiana Parsed Corpus of Historical High German

The app.py file contains sevral stand-alone commands that assist in various data transformations:

#### To extract single line ptb style treebank from the gold IPCHG treebank file (note: the user must specify the file name for extracted_treebank_name):
```
python app.py extract-gold 1533_johann_fierrabras.ver0_2.txt 1533_johann_fierrabras.ver0_2.brackets
```

This returns 1533_johann_fierrabras.ver0_2.brackets

#### To extract single line ptb style treebank from the conlluplus files
```
python app.py convert-conlluplus _KoelhoffChronik#(F163#).conllup
```

This returns _KoelhoffChronik#(F163#).conllup.brackets

**ATTENTION the following issues have been identified in the outputs that need to be manually corrected:**
- | is extracted as a stand-alone token and should be removed
- (_ ) is sometimes extracted incorrectly and should be replaced with (_ _)
- (") is sometimes extracted incorrectly and should be replaced with (META ")

Failure to correct any of these issues will not allow the treebank to be read correctly in various applications. Any future issues should be noted and added to the list.


#### To check how many subword tokens exist in a sentence in a ptb treebank (note: the user must specify the tokenizer (e.g.,dbmdz/bert-base-german-cased)  :
```
python app.py wordpiece-512check 1533_johann_fierrabras.ver0_2.brackets dbmdz/bert-base-german-cased
 
```

This prints out to the screen the sentence number (i.e., line number), the length of the sentence based on subword tokens, the text setence, and the tree for all all sentences that are >512 subword units in length.


#### Many parsers need a vritual root attached to the top of the tree, but are not annotated with these. To add a vroot to a treebank:

```
python app.py add-treebank-root 1533_johann_fierrabras.ver0_2.brackets
```

This returns a file: 1533_johann_fierrabras.ver0_2_vroot.brackets


#### We want to replace the parsed trees with gold POS tags (when available). To replace parsed files with the gold POS tags after parsing:

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

treetools will do some internal conversions and add a virtual root by default.

**ATTENTION note that the following issues have been identified in conversion process in the outputs and need to be manually corrected:**

- LRB.RRB should be changed to <.>
- LRB,RRB should be changed to <,>
- LRB:RRB should be changed to <:>
- LRB;RRB should be changed to <;>
- LRB!RRB should be changed to <!>
- LRB.RRB should be changed to <?>
- LRB"RRB should be changed to <">
- ($LRB LRB) should be changed to (, PARENL)
- ($LRB RRB) should be changed to (, PARENR)
After replacing those, find LRB and RRB to catch any remaining instances.

Failure to correct any of these issues will not allow the treebank to be read correctly in various applications. Any future issues should be noted and added to the list.

### C6C
We use C6C (https://github.com/rubcompling/C6C) to extract trees from xml (more specifically coraxmlrefbo) and transform them into conlluplus formats (which we then will subsequently convert later to readable ptb format). The desired xml files should be placed in a directory (here input_directory) and an output directory should be created (here output_directory).

```
python C6C.py convert input_directory/ -i coraxmlrefbo -e conlluplus output_directory/
```

This will convert the xml files to a conlluplus and be named as such (e.g., _KoelhoffChronik#(F163#).conllup) which can subsequently be converted into a ptb format via the above command (see convert-conlluplus).

### Parser
Currently we use the Berkeley Nueral Parser (https://github.com/nikitakit/self-attentive-parser) for parsing (and POS tagging). The parser should be cloned (or downloaded). Note that one may be required to separately compile the evaluation scripts in the EVALB and EVALB_SPMRL folders (which require a gcc compiler) for them to be sucessfully executed during training and prediction.

## Using Carbonate 

Currently, the parser is trained on GPUs using Carbonate (a high performance computng cluster, https://kb.iu.edu/d/aolp, note this also contains information on requesting access and logging into the HPC) and a person needs an account to access the clusters. Alternatively, if an individual possesses a computer with a GPU that has sufficient enough memory, models can also be trained locally (but may very in time needed to train).

To login to carbonte

There are two basic bash scripts needed to train and predict the parser (provided below). **Before training the --model-path-base directory MUST already be created**

**All jobs must have #SBATCH --account r00103 (the current project id associated with the project provided by UITS) specified in the job script order for a job to be sent to a GPU partition, failure to do so will result in a permissions error**

<ol>
<li> <details><summary>Carbonate Bash Train Example</summary><blockquote>
#!/bin/bash                                                                     

#SBATCH -J enhg                                                                 
#SBATCH -p gpu                                                                  
#SBATCH -o filename_%j.txt                                                      
#SBATCH -e filename_%j.err                                                      
#SBATCH --mail-type=ALL                                                         
#SBATCH --mail-user=xxx@gmail.com                                          
#SBATCH --nodes=1                                                               
#SBATCH --ntasks-per-node=1                                                     
#SBATCH --gpus v100:1                                                           
#SBATCH --time=08:00:00                                                         
#SBATCH --account r00103                                                        

module load cudatoolkit
module unload python/3.6.8
module load python/3.8.2

cd ./self-attentive-parser/

python src/main.py train --train-path enhg_train_vroot.ptb --dev-\
path enhg_dev_vroot.ptb --evalb-dir "EVALB_SPMRL" --checks-per-epoc\
h 1 --use-pretrained --pretrained-model "dbmdz/bert-base-german-cased" --model-\
path-base ./enhg/enhg_ptb --num-layers 4 --batch-size 32 --use-encoder --predic\
t-tags 
</blockquote>

</li>
<li> <details><summary>Carbonate Bash Test Example</summary><blockquote>
#!/bin/bash                                                                     

#SBATCH -J enhg                                                                 
#SBATCH -p gpu                                                                  
#SBATCH -o filename_%j.txt                                                      
#SBATCH -e filename_%j.err                                                      
#SBATCH --mail-type=ALL                                                         
#SBATCH --mail-user=xxx@gmail.com                                          
#SBATCH --nodes=1                                                               
#SBATCH --ntasks-per-node=1                                                     
#SBATCH --gpus v100:1                                                           
#SBATCH --time=08:00:00                                                         
#SBATCH --account r00103                                                        

module load cudatoolkit
module unload python/3.6.8
module load python/3.8.2

cd ./self-attentive-parser/

python src/main.py test --test-path enhg_test_vroot.ptb --evalb-dir EVALB_SPMRL --model-path enhg/enhg_ptb_dev=71.02.pt* --output-path enhg_test_vroot.ptb.parsed
</blockquote>
</li>
</ol>
