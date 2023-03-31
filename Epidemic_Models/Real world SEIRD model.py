import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.5  # contact rate
alpha = 0.2  # exposed to infected rate
gamma = 0.1  # recovery rate
mu = 0.01  # death rate
t_max = 100  # number of time steps

# Read graph from edges file
G = nx.read_edgelist("texas.mtx", nodetype=int, data=False)

# Ensure that nodes are numbered starting from 1
mapping = {node: node - 1 for node in G.nodes()}
G = nx.relabel_nodes(G, mapping)
n = G.number_of_nodes()

# Initialize state arrays
S = np.ones(n)
E = np.zeros(n)
I = np.zeros(n)
R = np.zeros(n)
D = np.zeros(n)
I[0] = 1  # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
E_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))
D_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
E_history[:, 0] = E
I_history[:, 0] = I
R_history[:, 0] = R
D_history[:, 0] = D


# Define animation function
for t in range(1,t_max):
    print(t)
    # Susceptible to exposed
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            lambda_ = sum(I) * beta / n  # exposure probability
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < lambda_:
                        S[j] = 0
                        E[j] = 1

    # Exposed to infected
    for i in range(n):
        if E[i] == 1:
            if np.random.rand() < alpha:
                E[i] = 0
                I[i] = 1

    # Infected to recovered or dead
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                if np.random.rand() < mu:
                    I[i] = 0
                    D[i] = 1
                else:
                    I[i] = 0
                    R[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    R_history[:, t] = R
    D_history[:, t] = D



# Plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.plot(np.sum(R_history, axis=0), label='Recovered')
plt.plot(np.sum(D_history, axis=0), label='Deaseased')
plt.plot("SEIRD Model in Barabasi Graph")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.title("SEIRD")
plt.show()
