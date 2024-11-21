import networkx as nx
import random
import numpy as np
import math
import sys


def generateInstance(n: int, mx=100):
    # Generate KP instances, weights and values
    # n = number of elements, mx = ma weight and value
    values = np.random.choice(range(1, mx), size=n).tolist()
    weights = np.random.choice(range(1, mx), size=n).tolist()
    wMax = max(weights)

    return list(zip(values, weights)), np.random.randint(wMax, 2 * wMax)


# DP with weights as lines
# vw = value weight list and W = KP size
def dpW(vw, W: int):
    n = len(vw)
    A = np.zeros((W + 1, n + 1), int)
    B: list = [[[] for i in range(n + 1)] for i in range(W + 1)]

    # Initialize, it's already 0 but anyway
    for i in range(n + 1):
        A[0][i] = 0
    for i in range(W + 1):
        A[W][0] = 0

    # Actual DP
    for w in range(1, W + 1):
        for i in range(1, n + 1):
            if w < vw[i - 1][1]:
                A[w][i] = A[w][i - 1]
                B[w][i] = B[w][i - 1]
            else:
                if A[w][i - 1] > vw[i - 1][0] + A[w - vw[i - 1][1]][i - 1]:
                    A[w][i] = A[w][i - 1]
                    B[w][i] = B[w][i - 1]
                else:
                    A[w][i] = vw[i - 1][0] + A[w - vw[i - 1][1]][i - 1]
                    B[w][i] = B[w - vw[i - 1][1]][i - 1] + [i - 1]

    return int(A[W][n]), B[W][n]


def dpV(vw, W):
    n = len(vw)
    sv = sum([x[0] for x in vw])
    A = np.zeros((sv + 1, n + 1), float)
    B = [[[] for i in range(n + 1)] for i in range(sv + 1)]

    for i in range(n + 1):
        A[0][i] = 0
    for v in range(1, sv + 1):
        A[v][0] = float("inf")

    for v in range(1, sv + 1):
        for i in range(1, n + 1):
            if v < vw[i - 1][0]:
                if A[v][i - 1] < vw[i - 1][1]:
                    A[v][i] = A[v][i - 1]
                    B[v][i] = B[v][i - 1]
                else:
                    A[v][i] = vw[i - 1][1]
                    B[v][i] = [i - 1]
            else:
                if A[v][i - 1] < vw[i - 1][1] + A[v - vw[i - 1][0]][i - 1]:
                    A[v][i] = A[v][i - 1]
                    B[v][i] = B[v][i - 1]
                else:
                    A[v][i] = vw[i - 1][1] + A[v - vw[i - 1][0]][i - 1]
                    B[v][i] = B[v - vw[i - 1][0]][i - 1] + [i - 1]

    for v in range(sv, 0, -1):
        if A[v][n] <= W:
            return v, B[v][n]


# Check here
def kpFPTAS(vw, W, epsilon):
    n = len(vw)
    theta = max(epsilon * max([x[0] for x in vw]) / (2 * n), 1.0)
    vhat, X = dpV([(math.ceil(coppia[0] / theta), coppia[1]) for coppia in vw], W)
    return sum([vw[i][0] for i in X]), X


if len(sys.argv) > 1:
    SIZE = int(sys.argv[1])
else:
    SIZE = 20

if len(sys.argv) > 2:
    epsilon = float(sys.argv[2])
else:
    epsilon = 0.5

inst, kp = generateInstance(SIZE)
print(f"Objects are: {inst}")
print(f"KP max weight is: {kp}")

res1, b1 = dpW(inst, kp)
print(f"DP with weights:")
print(res1)
print(f"It took")
print(b1)


res2, b2 = dpV(inst, kp)
print(f"DP with values:")
print(res2)
print(f"It took")
print(b2)

# Exec FPTAS
res3, b3 = kpFPTAS(inst, kp, epsilon)
print(f"DP FPTAS:")
print(res3)
print(f"It took")
print(b3)
