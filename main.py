import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import svd

# Make sure NLTK data is available
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


# ---------------------------------------------------------
# TEXT RANK IMPLEMENTATION
# ---------------------------------------------------------
def textrank_summary(text, n_sentences=3):
    sentences = sent_tokenize(text)

    # TF-IDF vectors for sentences
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(sentences)

    # Similarity matrix
    sim_matrix = cosine_similarity(tfidf)

    # PageRank parameters
    n = len(sentences)
    scores = np.ones(n) / n
    damping = 0.85

    # Power iteration
    for _ in range(50):
        new_scores = (1 - damping) + damping * sim_matrix.dot(scores)
        if np.allclose(new_scores, scores):
            break
        scores = new_scores

    # Pick top sentences
    top_idx = np.argsort(scores)[-n_sentences:]
    top_idx = sorted(top_idx)

    return " ".join(sentences[i] for i in top_idx)


# ---------------------------------------------------------
# LSA IMPLEMENTATION
# ---------------------------------------------------------
def lsa_summary(text, n_sentences=3, k_topics=3):
    sentences = sent_tokenize(text)

    # Sentence-term matrix
    vectorizer = TfidfVectorizer(stop_words="english")
    A = vectorizer.fit_transform(sentences).toarray()

    # SVD
    U, S, Vt = svd(A, full_matrices=False)

    # Keep top k topics
    U_k = U[:, :k_topics]
    S_k = S[:k_topics]

    # Sentence importance score
    scores = np.sqrt((U_k * S_k) ** 2).sum(axis=1)

    # Pick top sentences
    top_idx = np.argsort(scores)[-n_sentences:]
    top_idx = sorted(top_idx)

    return " ".join(sentences[i] for i in top_idx)


# ---------------------------------------------------------
# MAIN CONSOLE APP
# ---------------------------------------------------------
def main():
    print("\n=== SIMPLE TEXT SUMMARIZER (TextRank / LSA) ===\n")

    text = input("Paste your text here:\n\n")

    print("\nChoose summarization method:")
    print("1 - TextRank")
    print("2 - LSA")
    method = input("\nEnter 1 or 2: ")

    n = input("\nHow many sentences should the summary contain? (default = 3): ")
    n = int(n) if n.strip() else 3

    print("\n=== SUMMARY ===\n")

    if method == "1":
        print(textrank_summary(text, n))
    elif method == "2":
        print(lsa_summary(text, n))
    else:
        print("Invalid choice.")

    print("\n================\n")


if __name__ == "__main__":
    main()
