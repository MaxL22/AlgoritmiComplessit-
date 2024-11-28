import numpy as np
import random
from scipy.optimize import linprog
import math


def generateInstance(m, n=10, maxW=100):
    res = []
    for i in range(m):
        s = set(random.sample(range(n), random.randint(1, n // m)))
        res += [(s, random.randint(1, maxW))]

    return res


# I instance, list of pairs (s,w) where s is a set of point and w its cost
def setCover(I, k):
    m = len(I)
    universe = list(set.union(*[s for s, w in I]))
    n = len(universe)
    # Setup PL
    c = np.array([w for s, w in I])
    A_ub = np.zeros((n, m))
    b_ub = np.zeros(n)

    for i in range(n):
        p = universe[i]
        for j in range(m):
            s, w = I[j]
            if p in s:
                A_ub[i][j] = -1
        b_ub[i] = -1

    lphat = linprog(c, A_ub, b_ub, bounds=(0, 1))
    lp = linprog(c, A_ub, b_ub, bounds=(0, 1), integrality=1)
    xhat = lphat.x
    xexact = lp.x

    attempts = math.ceil(k + math.log(n))

    res = set([])
    for i in range(m):
        for t in range(attempts):
            if random.random() <= xhat[i]:
                res |= set([i])
                break

    resexact = set([i for i in range(m) if xexact[i] == 1])
    return res, resexact


while True:
    I = generateInstance(150, n=1000)
    res, resexact = setCover(I, 3)
    if res != resexact and sum([I[x][1] for x in res]) != sum(
        [I[x][1] for x in resexact]
    ):
        break

universe = set.union(*[s for s, w in I])

if set.union(*[I[x][0] for x in res]) == universe:
    print("Sol approssimata ammissibile")
if set.union(*[I[x][0] for x in resexact]) == universe:
    print("Sol esatta ammissibile")

print(f"Valore sol esatta: {sum([I[x][1] for x in resexact])}")
print(f"Valore sol appr: {sum([I[x][1] for x in res])}")
