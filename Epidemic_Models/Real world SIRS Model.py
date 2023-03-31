import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Read graph from edges file
G = nx.read_edgelist("texas.mtx", nodetype=int)

# Ensure that nodes are numbered starting from 1
mapping = {node: node - 1 for node in G.nodes()}
G = nx.relabel_nodes(G, mapping)

# Set up simulation parameters
beta = 0.5 # infection rate
gamma = 0.083 # recovery rate
eeta = 0.2
t_max = 100 # number of time steps

# Initialize state arrays
n = len(G.nodes())
S = np.ones(n)
I = np.zeros(n)
R = np.zeros(n)
I[0] = 1 # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
I_history[:, 0] = I
R_history[:, 0] = R

# Run simulation
for t in range(1, t_max):
    print(t)
    # Infect susceptible neighbors
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < beta:
                        S[j] = 0
                        I[j] = 1

    # Recover infected individuals
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                I[i] = 0
                R[i] = 1
    # Recovered to Susceptable
    for i in range(n):
        if R[i] == 1:
            if np.random.rand() < eeta:
                R[i] = 0
                S[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    R_history[:, t] = R

# Plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.plot(np.sum(R_history, axis=0), label='Recovered')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.title("SIRS Model")
plt.show()
