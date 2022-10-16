"""
TASK 1 and TASK 2
1. Implement a generalized n-gram language model for the Romanian language, using a smoothing technique at your choice.
2. Compute the probability of a new sentence, given at input, using the n-gram model you developed.
"""

from bs4 import BeautifulSoup
import requests
from nltk.tokenize import word_tokenize
import nltk
# nltk.download('punkt')


def create_corpus(page_link):
    # get URL
    page = requests.get(page_link)

    # scrape webpage
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)

    # write text into a file
    f = open("corpus.txt", "wb")
    for item in soup.find_all('p'):
        f.write(item.get_text().encode("UTF-8"))
    f.close()


def extract_words():
    text = open("corpus.txt", "r", encoding="utf-8").read()
    words_list = word_tokenize(text)

    words = list()
    for item in words_list:
        if item.startswith("„") and len(item) > 2:
            words.append(item[1:])
        elif item not in ",.:;!?()„”-'[]–’/—--''..—■``■—...":
            words.append(item)

    print("All the words from the corpus: ", len(words), "\n")

    unique_words = set(words)
    print("All the UNIQUE words from the corpus: ", len(unique_words))

    return words, unique_words


def get_language_model(words, unique_words, n):
    V = len(unique_words)

    if n == 2:
        list_of_bigrams = []
        bigram_counts = {}
        unigram_counts = {}

        for i in range(len(words) - 1):
            if i < len(words) - 1 and words[i + 1].islower():
                list_of_bigrams.append((words[i], words[i + 1]))

                if (words[i], words[i + 1]) in bigram_counts:
                    bigram_counts[(words[i], words[i + 1])] += 1
                else:
                    bigram_counts[(words[i], words[i + 1])] = 1

            if words[i] in unigram_counts:
                unigram_counts[words[i]] += 1
            else:
                unigram_counts[words[i]] = 1

        print("\n All the possible Bigrams are: ")
        print(list_of_bigrams)

        print("\n Bigrams along with their frequency: ")
        print(bigram_counts)

        print("\n Unigrams along with their frequency: ")
        print(unigram_counts)

        list_of_probabilities = {}
        for bigram in list_of_bigrams:
            word1 = bigram[0]
            list_of_probabilities[bigram] = (bigram_counts.get(bigram) + 1) / (unigram_counts.get(word1) + V)

        print("\n Bigrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_bigrams, bigram_counts, unigram_counts

    elif n == 3:
        list_of_trigrams = []
        trigram_counts = {}
        bigram_counts = {}

        for i in range(len(words) - 1):
            if i < len(words) - 2 and words[i + 1].islower() and words[i + 2].islower():
                list_of_trigrams.append((words[i], words[i + 1], words[i + 2]))

                if (words[i], words[i + 1], words[i + 2]) in trigram_counts:
                    trigram_counts[(words[i], words[i + 1], words[i + 2])] += 1
                else:
                    trigram_counts[(words[i], words[i + 1], words[i + 2])] = 1

            if (words[i], words[i + 1]) in bigram_counts:
                bigram_counts[(words[i], words[i + 1])] += 1
            else:
                bigram_counts[(words[i], words[i + 1])] = 1

        print("\n All the possible Trigrams are: ")
        print(list_of_trigrams)

        print("\n Trigrams along with their frequency: ")
        print(trigram_counts)

        print("\n Bigrams along with their frequency: ")
        print(bigram_counts)

        list_of_probabilities = {}
        for trigram in list_of_trigrams:
            word1 = trigram[0]
            word2 = trigram[1]
            list_of_probabilities[trigram] = (trigram_counts.get(trigram) + 1) / (bigram_counts.get((word1, word2)) + V)

        print("\n Trigrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_trigrams, trigram_counts, bigram_counts

    elif n == 4:
        list_of_quadrugrams = []
        quadrugrams_counts = {}
        trigram_counts = {}

        for i in range(len(words) - 1):
            if i < len(words) - 3 and words[i + 1].islower() and words[i + 2].islower() and words[i + 3].islower():
                list_of_quadrugrams.append((words[i], words[i + 1], words[i + 2], words[i + 3]))

                if (words[i], words[i + 1], words[i + 2], words[i + 3]) in quadrugrams_counts:
                    quadrugrams_counts[(words[i], words[i + 1], words[i + 2], words[i + 3])] += 1
                else:
                    quadrugrams_counts[(words[i], words[i + 1], words[i + 2], words[i + 3])] = 1

                if (words[i], words[i + 1], words[i + 2]) in trigram_counts:
                    trigram_counts[(words[i], words[i + 1], words[i + 2])] += 1
                else:
                    trigram_counts[(words[i], words[i + 1], words[i + 2])] = 1

        print("\n All the possible Quadrugrams are: ")
        print(list_of_quadrugrams)

        print("\n Quadrugrams along with their frequency: ")
        print(quadrugrams_counts)

        print("\n Trigrams along with their frequency: ")
        print(trigram_counts)

        list_of_probabilities = {}
        for quadrugram in list_of_quadrugrams:
            word1 = quadrugram[0]
            word2 = quadrugram[1]
            word3 = quadrugram[2]
            list_of_probabilities[quadrugram] = \
                (quadrugrams_counts.get(quadrugram) + 1) / (trigram_counts.get((word1, word2, word3)) + V)

        print("\n Quadrugrams along with their probability: ")
        print(list_of_probabilities)

        return list_of_probabilities, list_of_quadrugrams, quadrugrams_counts, trigram_counts


def get_probability_for_a_new_text(n, input_text, unique_words, words, list_of_probabilities,
                                   list_of_tuples, tuples_counts, tuples_minus_1_counts):
    V = len(unique_words)
    input_words = word_tokenize(input_text)
    tuples = []

    if n == 2:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 1:
                tuples.append((input_words[i], input_words[i + 1]))
        print("\n The bigrams in given sentence are: ")
        print(tuples)
    elif n == 3:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 2:
                tuples.append((input_words[i], input_words[i + 1], input_words[i + 2]))
        print("\n The trigrams in given sentence are: ")
        print(tuples)
    elif n == 4:
        for i in range(len(input_words) - 1):
            if i < len(input_words) - 3:
                tuples.append((input_words[i], input_words[i + 1], input_words[i + 2], input_words[i + 3]))
        print("\n The quadrugrams in given sentence are: ")
        print(tuples)

    count = 0
    for item in input_words:
        if item not in words:
            count += 1

    print("\n The probabilities for the tuples are: ")
    sentence_probability = 1
    if count == 0:
        for i in range(len(tuples)):
            print('0: ', list_of_probabilities[tuples[i]])
            sentence_probability *= list_of_probabilities[tuples[i]]
    else:
        for i in range(len(tuples)):
            if tuples[i] in list_of_tuples:
                probability = (tuples_counts[tuples[i]] + 1) / (
                            tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V)
                print('1: ', probability)
                sentence_probability *= probability
            elif tuples[i][:len(tuples[i]) - 1] in tuples_minus_1_counts:
                print('2: ', 1 / (tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V))
                sentence_probability *= 1 / (tuples_minus_1_counts[tuples[i][:len(tuples[i]) - 1]] + V)
            else:
                print('3: ', 1 / V)
                sentence_probability *= 1 / V

    print('\n' + f'The probability of sentence "{input_text}" is ' + str(sentence_probability))


if __name__ == "__main__":
    webpage_link = "https://ro.wikipedia.org/wiki/Cel_mai_iubit_dintre_pământeni_(roman)"

    # input_text = "They buy a big house"
    input_text = "Cel mai iubit dintre pământeni"
    # input_text = "Titlul romanului poate fi citit ca semn al pledoariei disperate pe care autorul o face"

    # input_text = input("Enter a sentence (in Romanian): ")
    n = int(input("Enter a value for n (it can be 2, 3 or 4): "))

    create_corpus(webpage_link)
    words, unique_words = extract_words()
    list_of_probabilities, list_of_tuples, tuples_counts, tuples_minus_1_counts = \
        get_language_model(words, unique_words, n)
    get_probability_for_a_new_text(n, input_text, unique_words, words, list_of_probabilities,
                                   list_of_tuples, tuples_counts, tuples_minus_1_counts)
