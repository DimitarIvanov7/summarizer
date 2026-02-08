import classla
import string

# import networkx as nx
import itertools
from pathlib import Path

classla.download('bg')
nlp = classla.Pipeline('bg', processors='tokenize')
lemma = classla.Pipeline('bg', processors='tokenize,pos,lemma')
summary_size = 2

BASE_DIR = Path(__file__).resolve().parent

def generate_stopwords():
    with open(BASE_DIR / "stopwords.json", encoding='utf-8', mode='r') as file:
        stop_words = [word.strip('\n') for word in file]
    return stop_words


# function to remove stopwords
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


def sentence_difference(first_sent, second_sent):

    counter = 0

    first_sent_list = first_sent.split()
    second_sent_list = second_sent.split()

    if len(first_sent_list) >= len(second_sent_list):
        longer_sent = first_sent_list
        shorter_sent = second_sent_list
    else:
        longer_sent = second_sent_list
        shorter_sent = first_sent_list

    for word_first in longer_sent:
        if word_first not in shorter_sent:
            counter += 1

    return counter / len(longer_sent)


def build_graph(nodes_combination):

    nodes = [n[0] for n in nodes_combination]
    gr = nx.Graph()  # initialize an undirected graph
    gr.add_nodes_from(nodes)
    node_pairs = list(itertools.combinations(nodes_combination, 2))

    # add edges to the graph (weighted by Levenshtein distance)
    for pair in node_pairs:
        first_string = pair[0]
        second_string = pair[1]
        lev_distance = sentence_difference(first_string[1], second_string[1])

        gr.add_edge(first_string[0], second_string[0], weight=lev_distance)

    return gr


def get_lemmas(sentences):

    # Generate couples containing the original sentence and the lemmatized one
    words = [[lem, lemma(clean_sentence(lem))] for lem in sentences if clean_sentence(lem)]
    words = [[word[0], word[1].sentences[0].to_dict()] for word in words]
    words = [[word[0], ' '.join([k['lemma'] for k in word[1][0]])] for word in words]

    return words


def rank_sentences(lem_sentences):
    current_weight = 0

    weights_dict = dict()

    for sent in lem_sentences:
        for sent_other in lem_sentences:
            current_weight += sentence_difference(sent[1], sent_other[1])

        weights_dict[sent[0]] = current_weight
        current_weight = 0

    return weights_dict


def summarize(articles, text_rank=True):
    filename = "results.txt"

    summary_of_articles = ""

    for article in articles:

        doc = nlp(article)

        sentences = [s.text for s in doc.sentences]

        lem_sentences = get_lemmas(sentences)

        if text_rank:

            graph = build_graph(lem_sentences)

            calculated_page_rank = nx.pagerank(graph, weight='weight')

            sorted_sentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

        else:

            filename = "results_other.txt"

            experimental_dict = rank_sentences(lem_sentences)

            sorted_sentences = sorted(experimental_dict)

        summary = ' '.join(sorted_sentences[:summary_size])

        summary_of_articles += summary + '\n'

    # save the summery to a file
    with open(filename, encoding='utf-8', mode="w") as f:
        f.write(summary_of_articles)

    return filename
