import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.0011 # infection rate
t_max = 100 # number of time steps

# Define the graph
n = 100 # number of nodes
k = 10 # number of nearest neighbors to connect
p = 0.1 # probability of rewiring
G = nx.newman_watts_strogatz_graph(n, k, p)

# p = 0.01
# G = nx.gnp_random_graph(n,p)

# Initialize state arrays
S = np.ones(n)
I = np.zeros(n)
I[0] = 1 # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
I_history[:, 0] = I

# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('Epidemic Spread on Newman Graph')
    pos = nx.spiral_layout(G)
    nx.draw(G, pos, node_color=['red' if i == 1 else 'blue' for i in I])
    plt.text(-1.3, 1.3, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, 1.2, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, 1.1, f'Susceptible Nodes: {int(np.sum(S))}')

# Define animation function
def update(t):
    global I, S

    # Infect susceptible neighbors
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < beta:
                        S[j] = 0
                        I[j] = 1

    # Store current states in history arrays
    I_history[:, t] = I
    S_history[:, t] = S

    # Plot current state
    plot_infection(t)

# Create animation
ani = FuncAnimation(plt.gcf(), update, frames=t_max, interval=50, repeat=False)

# Show the animation
plt.show()

# Plot results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()
