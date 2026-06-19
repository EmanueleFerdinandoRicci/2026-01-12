import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapD = {}
        self._graph = nx.Graph()
        self._constructors = []

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllNodes(self,y1,y2):
        self._constructors = DAO.getAllNodes(y1,y2)
        return self._constructors

    def creaGrafo(self,y1,y2):
        self._graph.clear()
        self._constructors = DAO.getAllNodes(y1, y2)
        for c in self._constructors:
            self._idMapD[c.constructorId] = c
        self._graph.add_nodes_from(self._constructors)

        allEdges = DAO.getAllEdges(y1, y2, self._idMapD)
        for e in allEdges:
            if self._graph.has_edge(e.constructor1, e.constructor2):
                peso = self._graph.get_edge_data(e.constructor1, e.constructor2, "weight")
                self._graph.remove_edge(e.constructor1, e.constructor2)
                self._graph.add_edge(e.constructor1, e.constructor2, weight= 1+peso["weight"])
            else:
                self._graph.add_edge(e.constructor1, e.constructor2, weight=1)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)