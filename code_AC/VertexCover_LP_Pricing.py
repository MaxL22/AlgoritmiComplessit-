"""
    Come implementato dal prof
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
from scipy.optimize import linprog

"""
    Given a graph G with attribute price on every edge, 
    return a dic with nodes of G as keys and sum of edge prices as values
"""
def totalPriceVertices(G: nx.Graph):
    result = {x: 0 for x in G.nodes()}
    for u,v,d in G.edges(data=True):
        result[u] += d['price']
        result[v] += d['price']
    return result
    
"""
    Given a graph G and a set of nodes X
    returns true if X is a Vertex cover
"""
def isVertexCover (G: nx.Graph, X):
    for u,v in G.edges():
        if u not in X and v not in X: 
            return False
    return True


"""
    Given graph G with ewights on node w (dictionary) and given a vertex cover X returns overall weight od X
"""
def vertexCoverCost(w, X):
    return sum(w[x] for x in X)

def PricingVertexCover (G, w):
    for u, v, d in G.edges(data=True):
        d['price'] = 0
    
    while True:
        tp = totalPriceVertices(G)
        delta_min = float('inf')
        delta_edge = None
        for u,v in G.edges():
            if tp[u] == w[u] or tp[v] == w[v]:
                continue
            delta = min(w[u] - tp[u], w[v]-tp[v])
            if delta < delta_min:
                delta_min = delta
                delta_edge = (u,v)
        if delta_edge is None:
            break
        G[delta_edge[0]][delta_edge[1]]['price'] += delta_min
        
    tp = totalPriceVertices(G)
    return set([x for x in G.nodes() if w[x] == tp[x]])

def roundingVertexCover (G: nx.Graph, w):
    nodes = list(G.nodes())
    c = [w[x] for x in nodes]
    """
        Matrice
        Ogni riga un lato
        Ogni colonna un nodo
        -1 se il lato è collegato a quel nodo
    """
    A_ub = [
        [-1 if x == u or x == v else 0 for x in nodes]
        for u,v in G.edges()
    ]
    b_ub = [-1 for x in G.edges()]
    
    # integrality 0 risolve sui reali, 1 su interi
    xstar = linprog(c, A_ub, b_ub, bounds=(0,1), integrality=0).x
    xhat = [0 if v<0.5 else 1 for v in xstar]

    return [nodes[i] for i in range(len(nodes)) if xhat[i]==1]

def exactVertexCover (G: nx.Graph, w):
    nodes = list(G.nodes())
    c = [w[x] for x in nodes]
    """
        Matrice
        Ogni riga un lato
        Ogni colonna un nodo
        -1 se il lato è collegato a quel nodo
    """
    A_ub = [
        [-1 if x == u or x == v else 0 for x in nodes]
        for u,v in G.edges()
    ]
    b_ub = [-1 for x in G.edges()]
    
    # integrality 0 risolve sui reali, 1 su interi
    xstar = linprog(c, A_ub, b_ub, bounds=(0,1), integrality=1).x
    print(xstar)

    return [nodes[i] for i in range(len(nodes)) if abs(xstar[i]-1)<1E-3]

# Grafo random
G = nx.erdos_renyi_graph(100, 0.2)
w = {x: random.randrange(1, 50) for x in G.nodes()}

# Draw the graph with node labels displaying their weights
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)
    
print(w)
# plt.show()

res = PricingVertexCover(G, w)
res2 = roundingVertexCover(G, w)
exact = exactVertexCover(G, w)

print()
print(res)
print(res2)
print(exact)
print(f"Is vertex cover (Pricing)? {isVertexCover(G, res)}")
print(f"Is vertex cover (Rounding)? {isVertexCover(G, res2)}")
print(f"Is vertex cover (Exact)? {isVertexCover(G, exact)}")
print(f"Cost Pricing: {vertexCoverCost(w, res)}")
print(f"Cost Rounding: {vertexCoverCost(w, res2)}")
print(f"Cost Exact: {vertexCoverCost(w, exact)}")

"""
    Check exact code
"""
