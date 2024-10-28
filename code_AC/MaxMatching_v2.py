'''
    Non fatto da me ma da qualcuno che sa effettivamente programmare
'''

import networkx as nx
import matplotlib.pyplot as plt
import random

def BFS_aug(G : nx.Graph, M : set, n):

	c = {n : "G"}
	d = {n : 0};
	p = {n : None};

	F = [n]
	while F:
		x = F.pop(0)
		c[x] = "B"

		for y in G.neighbors(n):
			if(y not in c):
				p[y] = x
				d[y] = d[x]+1;
				c[x] = "G"

				if(d[x] % 2 == 0 and (x,y) not in M):
					F.append(y)
				elif(d[x] % 2 == 1 and (x,y) in M):
					F.append(y)

				if(not any(y in t for t in M)):
					return p, y;

	return None

def switch(G : nx.Graph, M : set, p : dict, y):
	flg = 0
	while p[y] != None:
		if(flg):
			M.remove((p[y],y))
		else:
			M.add((p[y], y))

		flg = not flg;
		y = p[y];

def findAugmenting(G : nx.Graph, M : set):
	for x in G.nodes:
		if(not any(x in t for t in M)):
			p = BFS_aug(G, M, x);

			if(p != None):
				return p
	return None

def MaxMatch(G : nx.Graph):
	M = set();
	while True:
		t = findAugmenting(G, M)

		#print(M, t);

		if(t == None):
			return M
		else:
			switch(G, M, t[0], t[1])

	return M

if __name__ == "__main__":
	B = nx.Graph()

	U = {f'U({i})' for i in range(1, 70)}
	D = {f'D({i})' for i in range(1, 70)}

	B.add_nodes_from(U, bipartite=0)
	B.add_nodes_from(D, bipartite=1)

	edges = [(random.choice(list(U)), random.choice(list(D))) for _ in range(500)]
	B.add_edges_from(edges)

	plt.figure(figsize=(12, 10))

	pos = nx.bipartite_layout(B, U)

	nx.draw_networkx_nodes(B, pos, nodelist=U, node_color='red', node_size=20, label='Uomini')
	nx.draw_networkx_nodes(B, pos, nodelist=D, node_color='blue', node_size=20, label='Donne')

	nx.draw_networkx_edges(B, pos, edge_color='gray')

	plt.title('Grafo Bipartito')
	plt.show()

	M = MaxMatch(B);

	print("-------------------");

	print(M);

	print("-------------------");

	print(len(M));
