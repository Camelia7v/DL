from deep_translator import GoogleTranslator
# pip install deep_translator


def translate_text(text, source_language, target_language):
    return GoogleTranslator(source=source_language, target=target_language).translate(text)


def nr_of_matches(sentence1, sentence2):

    if type(sentence1) != list and type(sentence2) != list:
        sentence1 = sentence1.strip().split(" ")
        sentence2 = sentence2.strip().split(" ")

    correct = 0
    for word in sentence1:
        if word in sentence2:
            correct += 1

    return correct


def compute_precision(translated_sentence, translated_and_corrected_sentence):
    correct = nr_of_matches(translated_sentence, translated_and_corrected_sentence)

    if type(translated_sentence) == str:
        output_length = len(translated_sentence.strip().split(" "))
    else:
        output_length = len(translated_sentence)

    return correct / output_length


def compute_recall(translated_sentence, translated_and_corrected_sentence):

    correct = nr_of_matches(translated_sentence, translated_and_corrected_sentence)
    reference_length = len(translated_and_corrected_sentence.strip().split(" "))

    return correct / reference_length


def compute_F_measure(precision, recall):
    return 2 * precision * recall / (precision + recall)


def n_gram_generator(sentence, n):
    sentence = sentence.lower()

    # Break sentence in tokens, remove empty tokens
    tokens = [token for token in sentence.split(" ") if token != ""]

    # zip concatenates the tokens into n-grams
    ngrams = zip(*[tokens[i:] for i in range(n)])

    return [" ".join(ngram) for ngram in ngrams]


def bleu_score(machine_translated_sentence, original_sentence):

    machine_translated_sentence_grams = []
    for n in range(1, 5):
        machine_translated_sentence_grams.append(n_gram_generator(machine_translated_sentence, n))
    print(machine_translated_sentence_grams)

    original_sentence_grams = []
    for n in range(1, 5):
        original_sentence_grams.append(n_gram_generator(original_sentence, n))

    machine_translated_sentence = machine_translated_sentence.strip().split(" ")
    original_sentence = original_sentence.strip().split(" ")

    precisions = []
    for n in range(0, 4):
        precisions.append(compute_precision(machine_translated_sentence_grams[n], original_sentence_grams[n]))

    brevity_penalty = min(1, len(machine_translated_sentence)/len(original_sentence))

    multiplied_precisions = 1
    print("Precisions for the grams: ")
    for precision in precisions:
        print(precision)
        multiplied_precisions *= precision

    bleu_score = multiplied_precisions ** (1/4) * brevity_penalty

    return bleu_score


if __name__ == "__main__":

    sentence1_original = input("Enter a first sentence in Romanian (of at least 10 words): ")
    sentence2_original = input("Enter a second sentence in Romanian (of at least 10 words): ")

    sentence1_translated = translate_text(sentence1_original, 'ro', 'en')
    sentence2_translated = translate_text(sentence2_original, 'ro', 'en')

    print(sentence1_translated)
    user_answer = input("Is the above sentence well translated? If yes, type 'yes', "
                        "otherwise type in the correct translation for the sentence: ")
    if user_answer.lower() == "yes":
        sentence1_translated_and_corrected = sentence1_translated
    else:
        sentence1_translated_and_corrected = user_answer

    print(sentence2_translated)
    user_answer = input("Is the above sentence well translated? If yes, type 'yes', "
                        "otherwise type in the correct translation for the sentence: ")
    if user_answer.lower() == "yes":
        sentence2_translated_and_corrected = sentence2_translated
    else:
        sentence2_translated_and_corrected = user_answer

    precision1 = compute_precision(sentence1_translated, sentence1_translated_and_corrected)
    recall1 = compute_recall(sentence1_translated, sentence1_translated_and_corrected)
    f_measure1 = compute_F_measure(precision1, recall1)
    print("\n F-measure for the first sentence:", f_measure1)

    precision2 = compute_precision(sentence2_translated, sentence2_translated_and_corrected)
    recall2 = compute_recall(sentence2_translated, sentence2_translated_and_corrected)
    f_measure2 = compute_F_measure(precision2, recall2)
    print("F-measure for the second sentence:", f_measure2, "\n")

    bleu1 = bleu_score(sentence1_translated, sentence1_translated_and_corrected)
    print("Bleu score for the first sentence: ", bleu1, "\n")

    bleu2 = bleu_score(sentence2_translated, sentence2_translated_and_corrected)
    print("Bleu score for the second sentence: ", bleu2)

    """ Test precision, recall and F-measure"""
    # precision = compute_precision("Israeli officials responsibility of airport safety",
    #                               "Israeli officials are responsible for airport security")
    # print(precision)
    # recall = compute_recall("Israeli officials responsibility of airport safety",
    #                         "Israeli officials are responsible for airport security")
    # print(recall)
    # print(compute_F_measure(precision, recall))
