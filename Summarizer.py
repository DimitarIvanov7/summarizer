import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import svd
import stanza

stanza.download("bg")
nlp_bg = stanza.Pipeline("bg", processors="tokenize", use_gpu=False)

def stanza_sent_tokenize(text):
    doc = nlp_bg(text)
    return [sentence.text for sentence in doc.sentences]

def textrank_summary_bg(text, clean_fn, n_sentences=3):
    sentences = stanza_sent_tokenize(text)  # works ok for BG most of the time

    if len(sentences) <= n_sentences:
        return " ".join(sentences)

    cleaned = [clean_fn(s) for s in sentences]
    vectorizer = TfidfVectorizer()  # no english stopwords
    tfidf = vectorizer.fit_transform(cleaned)

    sim_matrix = cosine_similarity(tfidf)
    np.fill_diagonal(sim_matrix, 0.0)  # optional: ignore self-similarity

    n = len(sentences)
    scores = np.ones(n) / n
    damping = 0.85

    for _ in range(50):
        new_scores = (1 - damping) / n + damping * sim_matrix.dot(scores)
        if np.allclose(new_scores, scores, atol=1e-6):
            break
        scores = new_scores

    top_idx = np.argsort(scores)[-n_sentences:]
    top_idx = sorted(top_idx)
    return " ".join(sentences[i] for i in top_idx)


def lsa_summary_bg(text, clean_fn, n_sentences=3, k_topics=3):
    sentences = stanza_sent_tokenize(text)

    if len(sentences) <= n_sentences:
        return " ".join(sentences)

    cleaned = [clean_fn(s) for s in sentences]
    vectorizer = TfidfVectorizer()
    A = vectorizer.fit_transform(cleaned).toarray()

    U, S, Vt = svd(A, full_matrices=False)

    k = min(k_topics, U.shape[1])
    U_k = U[:, :k]
    S_k = S[:k]

    scores = np.sqrt((U_k * S_k) ** 2).sum(axis=1)

    top_idx = np.argsort(scores)[-n_sentences:]
    top_idx = sorted(top_idx)
    return " ".join(sentences[i] for i in top_idx)
