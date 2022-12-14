import string
from nltk.corpus import wordnet as wn


def get_synset(domain):
    domain_synset = wn.synset(f'{domain}.n.01')
    return domain_synset


def get_hyponyms(domain):
    domain_synset = get_synset(domain)

    domain_hyponyms = domain_synset.hyponyms()

    hyponyms = []
    for hyponym in domain_hyponyms:
        hyponyms.append(hyponym.name().split(".")[0])

    return hyponyms


def get_hypernyms(domain):
    domain_synset = get_synset(domain)

    domain_hypernyms = domain_synset.hypernyms()

    hypernyms = []
    for hypernym in domain_hypernyms:
        hypernyms.append(hypernym.name().split(".")[0])

    return hypernyms


def get_def(word):
    return wn.synset(f'{word}.n.01').definition()


def get_synonym(word):
    synonym_list = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonym_list.append(lemma.name().split(".")[0])

    for synonym in synonym_list:
        if synonym != word:
            return synonym


def get_antonym(word):
    antonym_list = []
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            if lemma.antonyms():
                antonym_list.append(lemma.antonyms()[0].name())
    if len(antonym_list) >= 1:
        return antonym_list[0]
    else:
        return None


def remove_expression(words_list):  # keep only single words
    for word in words_list:
        for character in word:
            if character in string.punctuation:
                words_list.remove(word)
                break


def get_words_and_clues(domain):
    words_list = get_hyponyms(domain)
    remove_expression(words_list)
    words_list.sort(key=len, reverse=True)

    questions_list = []
    for word in words_list:

        if get_antonym(word) is not None:
            questions_list.append(f"Antonym for {get_antonym(word)}")
        elif get_synonym(word) is not None:
            questions_list.append(f"Synonym for {get_synonym(word)}")
        else:
            questions_list.append(get_def(word))

    for i in range(len(words_list)):
        words_list[i] = words_list[i].upper()

    return words_list, questions_list
