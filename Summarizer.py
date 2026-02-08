import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import svd
import stanza

try:
    nlp_bg = stanza.Pipeline("bg", processors="tokenize", use_gpu=False)
except:
    stanza.download("bg")
    nlp_bg = stanza.Pipeline("bg", processors="tokenize", use_gpu=False)

def stanza_sent_tokenize(text):
    doc = nlp_bg(text)
    return [sentence.text for sentence in doc.sentences]

def textrank_summary_bg(text, clean_fn, n_sentences=3, damping=0.85, max_iter=100, tol=1e-6):
    sentences = stanza_sent_tokenize(text)
    N = len(sentences)

    if N <= n_sentences:
        return " ".join(sentences)

    # Clean sentences only for vectorization
    cleaned = [clean_fn(s) for s in sentences]

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(cleaned)

    # Similarity graph
    W = cosine_similarity(X)
    np.fill_diagonal(W, 0.0)

    # Row-normalize → transition matrix
    row_sums = W.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    P = W / row_sums

    # PageRank
    scores = np.ones(N) / N
    teleport = np.ones(N) / N

    for _ in range(max_iter):
        new_scores = (1 - damping) * teleport + damping * P.T.dot(scores)
        if np.linalg.norm(new_scores - scores, 1) < tol:
            break
        scores = new_scores

    # Select top sentences
    top_idx = np.argsort(scores)[-n_sentences:]
    top_idx.sort()

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
