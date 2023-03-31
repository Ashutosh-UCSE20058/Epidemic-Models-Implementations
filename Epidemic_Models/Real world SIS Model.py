import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# we are assuming a rumour spread model, as rumours have a higher infection rate,
# we take beta to be 0.5 and also considering how fast they can die out we take gamma to be 0.3

beta = 0.5  # infection rate
gamma = 0.3  # recovery rate

t_max = 100  # number of time steps

# Read graph from edges file
G = nx.read_edgelist("google_plus.txt", nodetype=int, data=False)

# Ensure that nodes are numbered starting from 1
mapping = {node: node - 1 for node in G.nodes()}
G = nx.relabel_nodes(G, mapping)

# Define the initial infected node
infected_node = 0

# Initialize state arrays
n = G.number_of_nodes()
S = np.ones(n)
I = np.zeros(n)

I[infected_node] = 1  # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
I_history[:, 0] = I



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

    # infected individuals becoming Susceptable again
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                I[i] = 0
                S[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I

# Plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')

plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.title("SIS")
plt.show()
