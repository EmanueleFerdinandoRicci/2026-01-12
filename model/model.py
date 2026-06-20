import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapD = {}
        self._graph = nx.Graph()
        self._constructors = []
        self._optListCostruttori = []
        self._minDistGiorni = 0

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

    def getEdgeGrandi(self):
        edgeGrandi = list(self._graph.edges(data=True))
        edgeGrandi.sort(key=lambda e: e[2]["weight"], reverse=True)
        return edgeGrandi

    def getCompConnessa(self):
        comp_connesse = list(nx.connected_components(self._graph))
        num = len(comp_connesse)
        comp_max = max(comp_connesse, key=len)
        return num,comp_max

    def getCompConnessaOrd(self):
        comp_connesse = list(nx.connected_components(self._graph))
        if not comp_connesse:
            return 0, []

        num = len(comp_connesse)
        # Trova la componente connessa con più nodi
        comp_max = max(comp_connesse, key=len)
        # Crea una lista di tuple (nodo, grado_del_nodo)
        nodi_con_grado = [(n, self._graph.degree(n)) for n in comp_max]
        # Ordina la lista in base al grado (l'elemento in posizione 1 della tupla) in ordine decrescente
        nodi_con_grado.sort(key=lambda x: x[1], reverse=True)

        return num, nodi_con_grado

    def calcolaPunto2Ricorsivo(self, k, y1, y2):
        self._optListCostruttori = []
        self._minDistGiorni = 100 * 365  # Valore altissimo iniziale (100 anni)

        # 1. Assegno le date di nascita dei veterani ai costruttori nel grafo
        veterani_tuples = DAO.getVeterani(y1, y2, self._idMapD)
        for c in self._graph.nodes:
            c.oldest_driver_dob = None
        for costruttore, dob in veterani_tuples:
            if costruttore in self._graph.nodes:
                costruttore.oldest_driver_dob = dob

        # 2. Ottengo le componenti connesse e le filtro:
        # Mi interessano solo i costruttori all'interno che hanno un veterano
        components = []
        for comp in nx.connected_components(self._graph):
            nodi_validi = [nodo for nodo in comp if getattr(nodo, 'oldest_driver_dob', None) is not None]
            if nodi_validi:
                components.append(nodi_validi)

        if len(components) < k:
            # Non ho abbastanza componenti connesse da cui pescare, non posso trovare una sol
            return None, 0, None, None

        parziale = []
        self._ricorsione(components, k, parziale, indexComponente=0)

        if self._optListCostruttori:
            self._optListCostruttori.sort(key=lambda x: x.oldest_driver_dob)
            min_dob = self._optListCostruttori[0].oldest_driver_dob
            max_dob = self._optListCostruttori[-1].oldest_driver_dob
            return self._optListCostruttori, self._minDistGiorni, min_dob, max_dob
        else:
            return None, 0, None, None

    def _ricorsione(self, components, k, parziale, indexComponente):
        # condizione di ottimalità
        if len(parziale) == k:
            # ho una soluzione accettabile.
            dateDiNascita = [c.oldest_driver_dob for c in parziale]
            diffEta = (max(dateDiNascita) - min(dateDiNascita)).days

            if diffEta < self._minDistGiorni:
                self._optListCostruttori = copy.deepcopy(parziale)
                self._minDistGiorni = diffEta
            return

        # condizione di terminazione
        # 1) esco se l'indice che indica quale comp connessa sto considerando a questa iterazione è diventato maggiore o
        # uguale al numero di componenti connesse totali, perchè vuol dire che non ho altre componenti connesse da cui pescare
        # 2) l'altro motivo è se non ho abbastanza componenti rimanenti per arrivare a k costruttori in parziale
        if indexComponente >= len(components) or (len(components) - indexComponente) < (k - len(parziale)):
            return

        # se non sono uscito, allora posso aggiungere ancora costruttori. Per questa componente, di indice indexComponente,
        # provo a ingaggiare un costruttore oppure a non ingaggiare nessuno.

        # Caso 1: inserisco un costruttore appartenente a questa comp connessa. In questo branch provo tutti i costruttori che
        # fanno parte della componente connessa in esame.
        componente = components[indexComponente]
        for costruttore in componente:
            parziale.append(costruttore)
            self._ricorsione(components, k, parziale, indexComponente + 1)
            parziale.pop()

        # Caso 2: mi tengo un branch di esplorazione in cui io non ho preso proprio nessuno da questa componente.
        self._ricorsione(components, k, parziale, indexComponente + 1)

