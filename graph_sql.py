from database import Edge, Node
from database import session as db_session


class GraphNode:

    def __init__(self, id):
        self.id = id


    def get_content(self):
        row = db_session.query(Node).where(Node.id == self.id).first()
        return row.primary_content, row.secondary_content


    def get_edges(self, threshold=0):
        rows = db_session.query(Edge).where(Edge.from_id == self.id, Edge.intensity > threshold)
        return [(edge.to_id, edge.intensity) for edge in rows]


    def edges(self, **args):
        return self.get_edges(args)


class GraphSQL:

    def get_node(self, id):
        return GraphNode(id)


    def node(self, id):
        return self.get_node(id)


    def add_node(self, **kwargs):
        if self.__node_exists(kwargs['title']):
            return

        node = Node(**kwargs)
        db_session.add(node)
        db_session.commit()

        return True


    def node_count(self):
        return len(db_session.query(Node).all())


    def find_node(self, title):
        return db_session.query(Node).where(Node.title == title).first()


    def add_edge(self, node1, node2, intensity=1):
        if self.__edge_exists(node1, node2):
            return

        edge = Edge(from_id=node1, to_id=node2, intensity=intensity)
        db_session.add(edge)
        edge = Edge(from_id=node2, to_id=node1, intensity=intensity)
        db_session.add(edge)
        db_session.commit()


    def get_edge(self, from_id, to_id):
        row = db_session.query(Edge).where(Edge.from_id == from_id, Edge.to_id == to_id).first()
        return row


    def edge(self, **kwargs):
        return self.get_edge(kwargs)


    def edges(self):
        rows = db_session.query(Edge).all()
        return rows


    def __edge_exists(self, from_id, to_id):
        return self.get_edge(from_id, to_id) != None


    def __node_exists(self, title):
        row = db_session.query(None).where(Node.title == title).first()
        return row


if __name__ == '__main__':
    g = GraphSQL()
    g.add_node(title='One more node')
