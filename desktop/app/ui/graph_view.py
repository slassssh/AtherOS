class GraphView:


    def __init__(self):

        self.nodes = []
        self.edges = []



    def add_node(self, node):

        self.nodes.append(
            node
        )

        return True



    def connect(self, source, target):

        self.edges.append(
            (
                source,
                target
            )
        )

        return True