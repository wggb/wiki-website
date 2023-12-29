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


def start_indexing(contents, lazy_input=True):
    if lazy_input:
        contents = [x for x in contents()]
    return FastSearch(contents)


class SearchEngine:
    def __init__(self, lazy_start=False, content_gen=get_node_contents):
        self.indexing_args = content_gen

        self.fast_search = FastSearch([])
        if not lazy_start:
            self.start_indexing()

    def start_indexing(self):
        self.fast_search = start_indexing(self.indexing_args)

    def query(self, query):
        return 1 + self.fast_search.query(query)

    def related_docs(self, doc_id):
        best, scores = self.fast_search.related_docs(doc_id - 1)
        return best + 1, scores

    def signal_new_doc(self):
        self.new_doc_count += 1

        if (
            self.new_doc_count < 0.1 * self.total_doc_count or self.new_doc_count > 100
        ) and self.new_doc_count > 3:
            self.start_indexing()
            self.new_doc_count = 0
            self.total_doc_count = self.fast_search.size
