from database import get_nodes
from fast_search import FastSearch


def get_model():
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


def get_node_contents():
    nodes = get_nodes()
    contents = (
        f"$title$ {n.title} $primary_content$ {n.primary_content} $secondary_content$ {n.secondary_content}"
        for n in nodes
    )
    return contents


def start_indexing(contents):
    contents = [x for x in contents]
    return FastSearch(contents)


class SearchEngine:
    def __init__(self, lazy_start=False, content_gen=get_node_contents):
        if lazy_start:
            self.fast_search = FastSearch([])
        else:
            self.fast_search = start_indexing(content_gen)

    def start_indexing(self):
        self.fast_search = start_indexing()

    def query(self, query):
        return 1 + self.fast_search.query(query)

    def related_docs(self, doc_id):
        best, scores = self.fast_search.related_docs(doc_id - 1)
        return best + 1, scores
