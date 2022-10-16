"""
TASK 3
Use a pre-trained neural language model to predict the next 2 words in a sequence of 4 words given as input.
"""

# pip install sentencepiece
# pip install transformers

import torch
import string
from transformers import BertTokenizer, BertForMaskedLM, logging
logging.set_verbosity_error()


# declare variables
no_words_to_be_predicted = globals()
input_text = globals()


# load model and tokenizer
def load_model():
    bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_model = BertForMaskedLM.from_pretrained('bert-base-uncased').eval()
    return bert_tokenizer, bert_model


# bert encode
def encode_bert(tokenizer, text_sentence, add_special_tokens=True):
    text_sentence = text_sentence.replace('<mask>', tokenizer.mask_token)
    # if <mask> is the last token, append a "." so that models don't predict punctuation.
    if tokenizer.mask_token == text_sentence.split()[-1]:
        text_sentence += ' .'
        input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])
        mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0]
    return input_ids, mask_idx


# bert decode
def decode_bert(tokenizer, pred_idx, top_clean):
    ignore_tokens = string.punctuation + '[PAD]'
    tokens = []
    for w in pred_idx:
        token = ''.join(tokenizer.decode(w).split())
        if token not in ignore_tokens:
            tokens.append(token.replace('##', ''))
    return '\n'.join(tokens[:top_clean])


def get_all_predictions(text_sentence, top_clean=5):
    input_ids, mask_idx = encode_bert(bert_tokenizer, text_sentence)
    with torch.no_grad():
        predict = bert_model(input_ids)[0]
    bert = decode_bert(bert_tokenizer, predict[0, mask_idx, :].topk(no_words_to_be_predicted).indices.tolist(),
                       top_clean)
    return {'bert': bert}


def get_prediction_end_of_sentence(input_text):
    input_text += ' <mask>'
    res = get_all_predictions(input_text, top_clean=int(no_words_to_be_predicted))
    return res


if __name__ == "__main__":

    print("----- Next Word Prediction with Pytorch using BERT -----")
    input_text = input("Enter a text: ")
    no_words_to_be_predicted = int(input("Enter the number of words to be predicted: "))

    bert_tokenizer, bert_model = load_model()
    bert_result = get_prediction_end_of_sentence(input_text)

    prediction = input_text
    for word in bert_result['bert'].split("\n"):
        prediction += " " + word
    print("Prediction: " + prediction)
