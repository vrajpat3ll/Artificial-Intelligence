class Graph:
    def __init__(self, nodes: int = 1):
        # Initialize the graph with infinite weights for all edges
        self.graph = [[float('inf') for i in range(nodes)]
                      for j in range(nodes)]

    def addEdge(self, u: int, v: int, w: int | float):
        # Add an edge from node u to node v (directed graph)
        self.graph[u - 1][v - 1] = w

    def addUndirectedEdge(self, u: int, v: int, w: int | float):
        # Add an edge between u and v (undirected graph)
        self.addEdge(u, v, w)
        self.addEdge(v, u, w)

    def getEdgeWeight(self, u: int, v: int):
        return self.graph[u - 1][v - 1]

    def __str__(self) -> str:
        return "\n".join(map(str, self.graph))
