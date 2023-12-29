from modules.graph_sql import GraphSQL


class Graph:
    def __init__(self, graph_sql=None, edge_threshold=0):
        self.edges = {}
        self.n = 0
        self.edge_threshold = edge_threshold

        self.update_cache = set()

        if graph_sql is None:
            graph_sql = GraphSQL()

        self.graph_sql = graph_sql
        self.__load_sql(graph_sql)

    def __load_sql(self, graph_sql):
        n = graph_sql.node_count()
        self.n = n

        for i in range(1, 1 + n):
            self.edges[i] = []

        for e in graph_sql.edges():
            self.__add_edge(e.from_id, e.to_id, e.intensity)

        for i in range(1, 1 + n):
            self.edges[i].sort(reverse=True)

    def __add_edge(self, from_id, to_id, intensity):
        if intensity < self.edge_threshold:
            return

        self.edges[from_id].append((intensity, to_id))

    def add_edge(self, from_id, to_id, intensity):
        if intensity < self.edge_threshold:
            return

        self.__add_edge(from_id, to_id, intensity)
        self.__add_edge(to_id, from_id, intensity)

        self.graph_sql.add_edge(from_id, to_id, intensity)

        self.update_cache.add(from_id)
        self.update_cache.add(to_id)

    def get_edges(self, node_id):
        return self.edges[node_id]

    def sort_edges(self, node=-1):
        if node < 0:
            for i in self.update_cache():
                self.nodes[i].sort()

            self.update_cache.clear()

        else:
            self.edges[node].sort()

    def top_k_edges(self, node, k=3):
        edges = self.edges[node]
        return edges[: min(k, len(edges))]

    def add_node(self, **kwargs):
        if self.graph_sql.add_node(kwargs):
            self.n += 1

    def node(self, id):
        return self.graph_sql.node(id)

    def find_node(self, title):
        return self.graph_sql.find_node(title)


if __name__ == "__main__":
    g = Graph(edge_threshold=0.7)
    # g.add_edge(2, 3, 0.9)
    print(g.top_k_edges(node=2, k=10))
