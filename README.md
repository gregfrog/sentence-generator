# sentence-generator

Random sentence generator from context-free grammars.


#### Usage:

For example, to generate 10 random sentences using a grammar described in the file grammar.txt, run:

```python sentence_generator.py --grammar=grammar.txt --num_sentences=10 --print_terminal_symbols True```

#### Grammar file:

The file structure is:

- Lines are either comments, the starting symbol of the grammar or production rules (which must be written entirely on one line) 
- Comments are single lines beginning with a hash character: 
~~~~
# A comment
#Another comment
~~~~   
- The starting symbol of the grammar occurs on a line by itself as the first non-comment line in the file.  
~~~~
# A comment
startsymbol
~~~~   
- The following non-comment lines are the production rules of the grammar. The set of terminal and non-terminal symbols are inferred from the grammar. 
~~~~
# A comment
startsymbol
startsymbol -> 'A'
~~~~

### Symbols and Productions 

- Each production rule consists of a production name, the symbol -> which is followed by a list of terminal or non-terminal symbols separated by spaces:  X -> A B C
~~~~
# A comment
startsymbol
startsymbol -> 'A' B C
B -> D
C -> 'word'
~~~~
- If a symbol is not the name of a rule it is treated as a terminal symbol, a literal.  
~~~~
city -> 'Oodnadatta'
~~~~  
- If a literal and a symbol name resolve to the same string, a loop will occur, for example this will loop and not terminate   
~~~~
# do not do this
city -> 'city'
~~~~  
- Terminal symbols may be quoted, enabling embedded spaces in them.  
~~~~
B -> 'A terminal'
~~~~  
- Terminal symbols may end with "()" in which case they will invoke a function of the same name in the script file (no check is made for syntactic correctness, if a function exists with that name in the script it will be called), currently only digits() is implemented and returns a randomly chosen digit.  For example 
~~~~
C -> digit() '+' digit()
~~~~
- Where there are multiple productions with the same name, one alternative is chosen randomly each time the production is referenced.  
~~~~
C -> digit() '+' digit()
C -> digit() '-' digit()
C -> digit() '*' digit()
C -> digit() '/' digit()
~~~~
- To weight the productions to provide a certain distiribution, a production may be repeated.  
~~~~
# 3/4 are additions
C -> digit() '+' digit()
C -> digit() '+' digit()
C -> digit() '+' digit()
C -> digit() '-' digit()
~~~~

Unlike the original version of this code, there are no spaces between generated terms.  This enables using this to generate test data files.

#### Examples:

We provide 2 sample grammars: A very simple toy grammar, in the file `simple_grammar.txt`, and a grammar designed to represent a subset of Brazilian Sign Language (Libras) syntax, in the file `libras_grammar.txt`.
