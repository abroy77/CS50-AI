import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NONTERMINALS = """
# S -> NP VP | NP VP NP | S Conj S | S Conj VP | S Conj NP 
# PP -> P NP
# NP -> N | Det N | AP N | N PP | NP Conj NP
# AP -> Adj | Adj AP
# VP -> V | V NP | V NP PP 

# """

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det NP | NP PP | AP NP | NP Adv
VP -> V | VP NP | VP PP | Adv VP | VP Adv | VP Conj VP
PP -> P NP 
AP -> Adj | Adj AP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.lower()
    sentence = nltk.word_tokenize(sentence)
    words_2_remove=[]
    for word in sentence:
        has_alpha=False
        for char in word:
            if char.isalpha():
                has_alpha=True
        if not has_alpha:
            words_2_remove.append(word)
    
    for word in words_2_remove:
        sentence.remove(word)
    
    return sentence
        



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    # loop through all subtrees
    for subtree in tree.subtrees():
        # if subtree is NP
        if subtree.label() == "NP":
            # if subtree has no NP children
            has_np_children = False
            for branch in subtree.subtrees():
                if branch.label() == "NP" and branch != subtree:
                    has_np_children = True
                    break
            if not has_np_children:
                chunks.append(subtree)
            
    
    return chunks
    


if __name__ == "__main__":
    main()
