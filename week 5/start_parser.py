import nltk
import sys
import string

def preprocess(sentence):
    """
    Convert `sentence` to a list of its words. Pre-process sentence by converting all characters
    to lowercase and removing any word that does not contain at least one alphabetic character.
    """
    words = nltk.word_tokenize(sentence.lower())
    words_without_punctuation = [word for word in words if any(c.isalpha() for c in word)]
    words_without_punctuation = [''.join(c for c in word if c not in string.punctuation) for word in words_without_punctuation]
    return [word for word in words_without_punctuation if word]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree. A noun phrase chunk is defined
    as any subtree of the sentence whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    def is_np_chunk(t):
        if t.label() != 'NP':
            return False
        
        result = True
        for s in t.subtrees():
            if t == s:
                continue
            
            result &= not is_np_chunk(s)

        return result

    return [subtree for subtree in tree.subtrees() if is_np_chunk(subtree)]

def main():

    slist = [None for x in range(10)]
    slist[0] = "Jip roept moeder."
    slist[1] = "Jip en Janneke spelen in de slaapkamer."
    slist[2] = "Jip is nu heel voorzichtig."
    slist[3] = "Bijna valt Takkie overboord."
    slist[4] = "Takkie loopt weg, met zijn staart tussen zijn pootjes."
    slist[5] = "Er komt een grote rode brandweerauto voorbij."
    slist[6] = "Janneke komt terug met de keukentrap."
    slist[7] = "Hij heeft een slee gezien met twee jongetjes erop en twee hondjes ervoor."
    slist[8] = "De volgende morgen kijkt Jip uit het raam."
    slist[9] = "En als ze klaar zijn, wil Jip direct weer met de trein gaan spelen."

    TERMINALS = """
    N -> "jip" | "moeder" | "janneke" | "takkie" | "brandweerauto" | "staart" | "pootjes" | "slaapkamer" | "keukentrap" | "hij" | "slee" | "jongetjes" | "hondjes" | "raam" | "morgen" | "trein" | "ze"
    V -> "roept" | "spelen" | "valt" | "loopt" | "komt" | "heeft" | "kijkt" | "is" | "gezien" | "kijkt" | "wil" | "gaan" | "zijn"
    Con -> "en" | "dan" | "nadat" | "voordat" | "als"
    Det -> "de" | "het" | "een" | "zijn" | "twee"
    P -> "in" | "tussen" | "met" | "uit"
    Adj -> "grote" | "rode" | "voorzichtig" | "volgende" | "klaar"
    Adv -> "heel" | "bijna" | "overboord" | "weg" | "voorbij" | "nu" | "er" | "terug"  | "erop" | "ervoor" | "morgen" | "direct" | "weer"
    """

    NONTERMINALS = """
    S -> NP VP | VP VP | Con S
    PP -> P NP
    VP -> V | V NP | VP PP | VP V | S V | V NP PP
    NP -> N | Det Nom | NP Con NP | Adv NP | NP Adv | Adv NP | NP Adj | Adv
    Nom -> N | Adj Nom
    """


    # Con Con N  Adj   V    V   N   Adv    Adv  P   Det N     V    V
    # en  als ze klaar zijn wil jip direct weer met de  trein gaan spelen
    # N = """
    # S -> NP VP
    # PP -> P NP
    # VP -> V | V VP | VP PP
    # NP -> Adv | Adv NP | Con NP | Con
    # """

    # parse CFG from strings
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    # nltk.ChartParser(grammar, trace=2) # debug
    # # to show rules:
    # for p in grammar.productions():
    #    print(p)

    count = [0 for x in range(10)]

    for i,s in enumerate(slist):
        print(s)

        s = preprocess(s)

        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            return
        if not trees:
            print("Could not parse sentence.")
            return

        # print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            count[i] += 1

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))

    print("aantal runs", count, sum(count))
if __name__ == "__main__":
    main()
