import string
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent

def generate_stopwords():
    with open(BASE_DIR / "stopwords.txt", encoding='utf-8', mode='r') as file:
        stop_words = [word.strip() for word in file]
    return stop_words

def remove_stopwords(sen, stop_words):

    new_sen = " ".join([i for i in sen if i not in stop_words and not i.isdigit()])

    return new_sen

def filter_sentences(sentence):
    """
    Removes the sentence if it doesn't end with punctuation or ends with a colon (:).
    Accepts only a single sentence (str).
    Returns the sentence if valid, else returns an empty string.
    """
    s = sentence.strip()
    if not s:
        return ""
    if s.endswith(":"):
        return ""
    if re.match(r".*[\.\!\?]$", s):
        return s
    return ""

def clean_sentence(func_sentence):
    """
    Cleans a single sentence after filtering.
    Returns the cleaned sentence or an empty string if filtered out.
    """
    filtered = filter_sentences(func_sentence)
    if not filtered:
        return ""
    stop_words = generate_stopwords()
    punct_symbols = (string.punctuation + '„“–')
    func_clean_sentence = filtered.replace("-", " ").lower()
    func_clean_sentence = func_clean_sentence.translate(str.maketrans('', '', punct_symbols))
    func_clean_sentence = remove_stopwords(func_clean_sentence.split(), stop_words)
    return func_clean_sentence



