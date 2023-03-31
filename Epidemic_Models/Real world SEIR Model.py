import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.2  # infection rate
sigma = 0.1  # rate of latent individuals becoming infectious
gamma = 0.05  # rate of infected individuals becoming recovered
t_max = 100  # number of time steps

# Read graph from edges file
G = nx.read_edgelist("google_plus.txt", nodetype=int, data=False)

# Ensure that nodes are numbered starting from 1
mapping = {node: node - 1 for node in G.nodes()}
G = nx.relabel_nodes(G, mapping)
n = G.number_of_nodes()

# Initialize state arrays
S = np.ones(n)
E = np.zeros(n)
I = np.zeros(n)
R = np.zeros(n)
I[0] = 1  # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
E_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
E_history[:, 0] = E
I_history[:, 0] = I
R_history[:, 0] = R


# Define animation function
for t in range(1,t_max):
    print(t)
    # Expose susceptible neighbors
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < beta:
                        S[j] = 0
                        E[j] = 1

    # Infect latent individuals
    for i in range(n):
        if E[i] == 1:
            if np.random.rand() < sigma:
                E[i] = 0
                I[i] = 1

    # Recover infected individuals
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                I[i] = 0
                R[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    E_history[:, t] = E
    I_history[:, t] = I
    R_history[:, t] = R

# plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(E_history, axis=0), label='Exposed')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.plot(np.sum(R_history, axis=0), label='Recovered')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.title("SEIR Model")
plt.show()