import string
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def generate_stopwords():
    with open(BASE_DIR / "stopwords.txt", encoding='utf-8', mode='r') as file:
        stop_words = [word.strip() for word in file]
    return stop_words

def remove_stopwords(sen, stop_words):

    new_sen = " ".join([i for i in sen if i not in stop_words and not i.isdigit()])

    return new_sen


def clean_sentence(func_sentence):

    stop_words = generate_stopwords()

    # add long dash
    punct_symbols = (string.punctuation + '„“–')

    # replace short dash and lower case
    func_clean_sentence = func_sentence.replace("-", " ").lower()

    # Removes punctuation symbols
    func_clean_sentence = func_clean_sentence.translate(str.maketrans('', '', punct_symbols))

    # remove special symbols, punctuation, digits and stop words from sentences and lower case
    func_clean_sentence = remove_stopwords(func_clean_sentence.split(), stop_words)

    return func_clean_sentence
