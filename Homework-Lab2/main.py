import nltk
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')


sentences = ["Papa eats octopus in pajamas", "John often eats seafood or octopus",
             "John and Mary eat often together"]

grammar = nltk.CFG.fromstring("""
S -> NP VP
NP -> 'Papa'
VP -> VB NP
VB -> 'eats'
NP -> NP PP
NP -> 'octopus'
PP -> P NP
P -> 'in'
NP -> 'pajamas'
VP -> VP PP
NP -> 'John'
VP -> VP NP
VP -> ADV VB
ADV -> 'often'
NP -> NP CONJ NP
NP -> 'seafood'
CONJ -> 'or'
NP -> 'Mary'
CONJ -> 'and'
VP -> VB ADVP
VB -> 'eat'
ADVP -> ADV ADV
ADV -> 'together'
""")

for sentence in sentences:
    print(f"Phrase structure tree(s) for '{sentence}'")
    sentence = sentence.split(" ")
    parser = nltk.ChartParser(grammar)
    for tree in parser.parse(sentence):
        print(tree)
    print("\n")


dependency_trees = []
for sentence in sentences:
    dependency_tree = nlp(sentence)
    dependency_trees.append(dependency_tree)

displacy.serve(dependency_trees, style='dep')

# When the program is running, go to http://localhost:5000 to see the dependency trees
