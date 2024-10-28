"""
    Fatto da me
"""

import networkx as nx
import random
import matplotlib.pyplot as plt

def pricingVertexCover (G_original: nx.Graph):
    G = G_original.copy()
    
    # Peso degli archi a zero
    for u, v in G.edges():
        G.edges[u, v]['weight'] = 0
    
    while True:
        min_diff = float('inf')
        min_edge = None
        
        # Trova il minimo
        for u,v in G.edges():
            diff = min(diffStretto(G, u), diffStretto(G, v))
            
            if diff is not 0:
                if diff < min_diff:
                    min_diff = diff
                    min_edge = (u,v)
        
        if min_edge == None:
            break
        
        G.edges[min_edge]['weight'] += min_diff
        print(G.edges[min_edge], min_diff)
    
    # Torna la lista di nodi non stretti
    return [i for i in G.nodes() if isStr(G,i)]
    

def isVertexCover (G: nx.Graph, X):
    for u,v in G.edges():
        if u not in X and v not in X: 
            return False
    return True

def vertexCoverCost(G: nx.Graph):
    return sum(G.nodes[i]['weight'] for i in G.nodes())

def isStr(G, node):
    return (sum(data['weight'] for _, _, data in G.edges(node, data=True))) >= G.nodes[node]['weight']
    
def diffStretto(G, node):
    return G.nodes[node]['weight'] - (sum(data['weight'] for _, _, data in G.edges(node, data=True)))

# Create a random graph
num_nodes = 15

G = nx.gnp_random_graph(num_nodes, 0.3)  # 0.5 is the probability for edge creation

# Add random weights to each node
for i in G.nodes():
    G.nodes[i]['weight'] = random.randint(1, 40)

# Print node weights
for node in G.nodes(data=True):
    print(f"Node {node[0]} has weight {node[1]['weight']}")

nodesList = pricingVertexCover(G)
print(f"I nodi stretti sono: {nodesList}")
print(f"Si tratta di un vertex cover? {isVertexCover(G, nodesList)}")
print(f"Il costo è: {vertexCoverCost(G)}")

# Draw the graph with node labels displaying their weights
pos = nx.spring_layout(G)
node_weights = nx.get_node_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)

# Draw the weights near the nodes
for node, (x, y) in pos.items():
    plt.text(x, y + 0.1, s=node_weights[node], bbox=dict( alpha=1), horizontalalignment='center')

# Draw the edge weights
# edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Display the graph
plt.show()
