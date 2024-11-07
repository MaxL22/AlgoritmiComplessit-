import networkx as nx
import random
import math
from matplotlib import pyplot as plt

# La clique sarà composta da punti random nel piano cartesiano, la distanza sarà distanza cartesiana


def genPoints(n=10, maxcoord=100):
    return [
        (random.randint(0, maxcoord), random.randint(0, maxcoord)) for i in range(n)
    ]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def plotpoints(points, col2segments: dict):
    maxx = max([p[0] for p in points])
    maxy = max([p[1] for p in points])
    plt.rcParams["figure.figsize"] = [maxx + 10, maxy + 10]
    plt.rcParams["figure.autolayout"] = True
    plt.xlim(-5, maxx + 5)
    plt.ylim(-5, maxy + 5)
    plt.grid()

    for p in points:
        plt.plot(
            p[0],
            p[1],
            marker="o",
            markersize=20,
            markeredgecolor="red",
            markerfacecolor="green",
        )

    for col, segments in col2segments.items():
        for segment in segments:
            p = points[segment[0]]
            q = points[segment[1]]
            plt.plot([p[0], q[0]], [p[1], q[1]], color=col, linewidth=5)
    plt.show()


# Dato un grafo fa clique
def points2clique(points):
    G = nx.Graph()
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=dist(points[i], points[j]))
    return G


def euPathToHamiltonian(ec):
    ec_path = [e[0] for e in ec]
    # hc_path = list(set(ec_path))
    hc_path = []
    for i in ec_path:
        if i not in hc_path:
            hc_path += [i]
    hc_path += [ec_path[0]]
    hc = [(hc_path[i], hc_path[i + 1]) for i in range(len(hc_path) - 1)]

    return hc


def cristophides(G: nx.Graph):
    T = nx.minimum_spanning_tree(G)
    D = [x for x in G.nodes() if T.degree[x] % 2 != 0]
    M = nx.min_weight_matching(G.subgraph(D))
    H = nx.MultiGraph()

    # Aggiunge tutti i lati dell'albero e del perfect matching
    for e in T.edges():
        H.add_edge(e[0], e[1])
    for e in M:
        H.add_edge(e[0], e[1])

    ec = list(nx.eulerian_circuit(H, 0))
    hc = euPathToHamiltonian(ec)

    return hc, list(T.edges()), M


# Aggiungi il plot di grafo iniziale e hc finale
V = genPoints()
hc, T, M = cristophides(points2clique(V))

print("In black the MST, in red the matching")
plotpoints(V, {"black": T, "red": M})

print("Now in blue the hamiltonian circuit")
plotpoints(V, {"blue": hc})
