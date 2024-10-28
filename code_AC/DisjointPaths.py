import networkx as nx
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
import math
import matplotlib.pyplot as plt

def greedyDisjointPath(G_original: nx.DiGraph, sourceTargetPairs, c=1):
    G = G_original.copy()
    # Set lengths and congestion
    # Restituisce iteratore, con data=True restituisce dizionario con label del nodo
    for u,v,d in G.edges(data = True):
        d['length'] = 1
        d['congestion'] = 0
        
    # Result sets
    I = [] # Indices of connected SourceTargetpairs
    P = [] # Corresponding paths
    # Calcola beta in modo da poter usare ogni arco c volte
    beta = math.pow(G.number_of_edges(), 1/(c+1))
    
    while True:
        min_length = float('inf')
        min_path = None
        min_connected_index = None
        
        # Per ogni coppia source-target
        for i in range(len(sourceTargetPairs)):
            # Se ha già un path lo salta
            if i in I: 
                continue
            
            # Altrimenti cerca il percorso minimo
            s = sourceTargetPairs[i][0]
            t = sourceTargetPairs[i][1]
            try:
                path = dijkstra_path(G, s, t, 'length')
            except: 
                pass
            else:
                # Se trova il path, ne calcola la lunghezza
                length = sum([G[path[i]][path[i+1]]['length'] for i in range(len(path) - 1)])
                # print(f"{path}, source={s}, target={t}, length={length}")
                # Se è il più breve trovato se lo segna
                if length < min_length:
                    min_length = length
                    min_path = path
                    min_connected_index = i
        # Qua ha trovato il percorso minimo
        # print(f"Minimum path: {min_path}, length={length}, index={min_connected_index}")
        # Se non lo ha trovato termina
        if min_path is None: 
            break
        
        print(f"Minimum path: {min_path}, length={min_length}, index={min_connected_index}")
        
        # Aggiorna la lista dei trovati ed il path
        I += [min_connected_index]
        P += [min_path]
        
        # Aggiorna il peso degli archi, eventualmente rimuovendoli
        for i in range(len(min_path)-1):
            u = min_path[i]
            v = min_path[i+1]
            G[u][v]['length'] *= beta
            G[u][v]['congestion'] += 1
            if G[u][v]['congestion'] == c: 
                G.remove_edge(u,v)
        #for u,v,d in G.edges(data=True):
        #    print(f"u={u} -> v={v} : d={d}")
    return I, P

def doubleFan(t = 10):
    G = nx.DiGraph()
    G.add_nodes_from(['s', 't', 'x', 'y'])
    G.add_nodes_from(['a' + str(x) for x in range(t)])
    G.add_nodes_from(['b' + str(x) for x in range(t)])
    G.add_edges_from([('s', 'a'+str(x)) for x in range(t)])
    G.add_edges_from([('a'+str(x), 'x') for x in range(t)])
    G.add_edges_from([('x', 'y')])
    G.add_edges_from([('y', 'b'+str(x)) for x in range(t)])
    G.add_edges_from([('b'+str(x), 't') for x in range(t)])
    return G
    
    
G = nx.DiGraph()

G = doubleFan(10)

# Per vedere il grafo
pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=15, font_color='black')
plt.title('NetworkX Graph Visualization')
plt.show()

stPairs = [('s','t')]*2
congestion = 2

I, P = greedyDisjointPath(G, stPairs, congestion)

print(I)
print(P)