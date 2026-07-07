class WorkflowDAG:


    def __init__(self):

        self.nodes = {}
        self.edges = []



    def add_node(self, node):

        self.nodes[node] = []

        return True



    def connect(self, start, end):

        self.edges.append(
            (
                start,
                end
            )
        )


        return True