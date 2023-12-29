import numpy as np


def tfidf_sim_matrix(docs):
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(
        min_df=1, ngram_range=(1, 1), max_df=0.3, token_pattern="\w*[a-z]+\w*"
    )
    vectorizer.fit(docs)

    encoder = lambda x: vectorizer.transform(x)

    D = encoder(docs)
    sim_matrix = D @ D.T

    return sim_matrix.toarray(), encoder, D


def setence_bert_sim_matrix(docs):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

    encoder = lambda x: model.encode(x)

    D = encoder(docs)
    sim_matrix = D @ D.T

    return sim_matrix, encoder, D


def get_top_k(sim_matrix, k=3, return_scores=True):
    top_k = k
    best = np.argpartition(sim_matrix, -top_k - 1, axis=1)[:, -top_k - 1 :]
    scores = np.zeros_like(best, dtype=np.float32)

    r = np.arange(sim_matrix.shape[0])[:, None]

    if return_scores:
        scores = sim_matrix[r, best]

    sorted_indices = np.argsort(scores, axis=1)[:, ::-1]

    best = best[r, sorted_indices][:, 1:]
    scores = scores[r, sorted_indices][:, 1:]

    return best, scores


class FastSearch:
    class Methods:
        SBERT = "SBERT"
        TFIDF = "TF-IDF"

    def __init__(self, docs):
        self.methods = {
            "TF-IDF": tfidf_sim_matrix(docs),
            "SBERT": setence_bert_sim_matrix(docs),
        }

    def query(self, query, method=Methods.SBERT, k=3):
        _, enc, D = self.methods[method]
        Q = enc(query)
        m = Q @ D.T

        # indices that we want sorted
        i = np.arange(1, k + 1) * -1
        doc_ids = np.argpartition(m, i)[-k - 1 :][::-1]

        return doc_ids

    def related_docs(self, doc_id, method=Methods.SBERT, k=3):
        sim, _, _ = self.methods[method]
        best, scores = get_top_k(sim[doc_id : doc_id + 1, :])
        return best, scores
