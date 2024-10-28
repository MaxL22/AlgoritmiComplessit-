import networkx as nx

'''
G: grafo non orientato
M: matching sul grafo

FindAugmenting (G,M):
X <- vertici esposti in M
for all x in X
	BFS(x) con alternanza di lati non in M e in M
'''

# BFS su lati alternati
def altBFS(x: int, G: nx.Graph, M: list, X: set):
    q = [x]
    known = []
    path = {}
    lfm = False

    # Deve ricordarsi il percorso e terminare al primo nodo esposto
    while q:
        # Aggiungi alla coda solo i nodi giusti
        for j in G[q[0]]:
            if j not in known:
                if not lfm and (j, x) not in M:
                    q.append(j)
                elif (j, x) in M:
                    q.append(j)
        
        lfm = not lfm
        known.append(q[0])
        path[q[len(q)-1]] = q[0]
        
        # Se nodo esposto termina
        if q[len(q)-1] in X:
            return path
        
        q.remove(q[0])
        # 'Till here it works I think
    
    return None 

# Trasforma il dict di nodi in lati
def getEdges(path: set):
    e = []
    for i in path: 
        e.append((path[i], i))     
    
    return e

# Switcha i lati del matching
def switch(M: list, e: list):
    for (i, j) in e:
        a,b = i,j
        if a > b: 
            a,b = b,a
        if (a, b) in M:
            M.remove((a,b))
        else:
            M.append((a,b))
    return M

# Crea un grafo vuoto
G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1, 4), (1, 5), (2, 5), (2, 6), (3, 4)])

# Crea un matching vuoto
M = []
# Lista di nodi esposti
X = {i for i in G}

# Stampa il grafo
print("Grafo:", G.edges())

c = 0

# Finché ci sono nodi esposti
while X:
    # nodi esposti da provare si intende
    if c==len(X):
        # Ho finito i nodi, quelli che rimangono non si possono trovare
        break
    
    x = list(X)[c]
    
    # BFS che alterna, ritorna il path
    a = altBFS(x, G, M, X)
    
    # Non ho trovato un path, provo con il prossimo nodo esposto
    if not a:
        print("No augmenting path from " + str(x))
        c+=1
        continue
    
    # Switch dei lati nel matching e path
    e = getEdges(a)
    M = switch(M, e)
    
    c = 0
    
    # Rimetto a posto la lista di nodi esposti
    for (i,j) in e: 
        if i in X:
            X.remove(i)
        if j in X:
            X.remove(j)
    
is_valid_matching = nx.algorithms.matching.is_matching(G, M)
print("Is it a valid Matching?", is_valid_matching)

print("Maximal match: " + str(M))