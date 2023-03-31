import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import networkx as nx
from matplotlib.animation import FuncAnimation

# According to some studies, the basic reproduction number (R0) for smallpox is estimated to be around 5-7,
# meaning that each infected person will on average infect 5-7 others. This translates to a high transmission rate, which can result in rapid spread of the disease.

# Based on historical data, the average duration of the infectious period for smallpox is about 10-14 days.
# This means that an infected person can transmit the virus to others for up to 2 weeks.

# The duration of immunity after recovery from smallpox is estimated to be around 30-40 years.
# However, the immunity can wane over time, which is why mu (the rate of immunity loss) is an important parameter in the SIR model.

# Using these values, we can estimate the values of beta, gamma, and mu for smallpox in the SIR model.
# For example, if we assume an R0 of 6, an infectious period of 12 days, and an immunity duration of 35 years, we can calculate:

# beta = R0 / infectious period = 6 / 12 = 0.5
# gamma = 1 / infectious period = 1 / 12 = 0.083
# mu = 1 / (365 * 35) = 0.000008
# These values are just estimates and may vary depending on the specific context and assumptions made.

# Define parameters
beta = 0.5 # infection rate
gamma = 0.083 # recovery rate
mu = 0.000008 # immunity loss rate
t_max = 100 # number of time steps

# Define the graph
# create an empty graph with 2000 nodes
G = nx.Graph()
G.add_nodes_from(range(769))

# # read edges from file and add to the graph
# with open('graph.txt', 'r') as f:
#     for line in f:
#         u, v = map(int, line.strip().split())
#         G.add_edge(u, v)
# n = G.number_of_nodes()

# Define the strogatz graph
n = 100 # number of nodes
k = 4 # number of nearest neighbors to connect
p = 0.1 # probability of rewiring
G = nx.newman_watts_strogatz_graph(n, k, p)

# Initialize state arrays
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

# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('Epidemic Spread on Newman Graph')
    pos = nx.spiral_layout(G)
    node_colors = np.where(R == 1, 'green', np.where(I == 1, 'red', 'blue'))
    nx.draw(G, pos, node_color=node_colors)
    plt.text(-1.3, 1.3, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, 1.2, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, 1.1, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-1.3, 1.0, f'Recovered Nodes: {int(np.sum(R))}')

# Define animation function
def update(t):
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

    # Lose immunity
    for i in range(n):
        if R[i] == 1:
            if np.random.rand() < mu:
                R[i] = 0
                S[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    R_history[:, t] = R

    # Plot current state
    plot_infection(t)

# Create animation
ani = FuncAnimation(plt.gcf(), update, frames=t_max, interval=50, repeat=False)

# Show the animation
plt.show()

# Plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.plot(np.sum(R_history, axis=0), label='Recovered')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()
