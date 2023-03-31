
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.2 # infection rate
sigma = 0.1 # rate of latent individuals becoming infectious
gamma = 0.05 # rate of infected individuals becoming recovered
t_max = 100 # number of time steps

# Define the graph
n = 100 # number of nodes
k = 5 # number of nearest neighbors to connect
p = 0.1 # probability of rewiring
G = nx.watts_strogatz_graph(n, k, p)

# Initialize state arrays
S = np.ones(n)
E = np.zeros(n)
I = np.zeros(n)
R = np.zeros(n)
I[0] = 1 # initial infected node

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

pos = nx.spiral_layout(G)

# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('SEIR Epidemic Spread on Newman Graph')
    
    nx.draw(G, pos, node_color=['green' if i == 0 else 'orange' if i == 1 else 'red' if i == 2 else 'blue' for i in np.argmax(np.vstack([S,E,I,R]), axis=0)])
    plt.text(-0.9, 1.2, f'Time Step: {t}/{t_max}')
    plt.text(-0.9, 1.1, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-0.9, 1.0, f'Exposed Nodes: {int(np.sum(E))}')
    plt.text(-0.9, 0.9, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-0.9, 0.8, f'Recovered Nodes: {int(np.sum(R))}')

# Define animation function
def update(t):
    global S, E, I, R

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

    # Plot current state
    plot_infection(t)

# Create animation
ani = FuncAnimation(plt.gcf(), update, frames=t_max, interval = 50, repeat = False)

# Showing te animation
plt.show()

# plot results
plt.plot(np.sum(S_history, axis=0), label = 'Susceptible')
plt.plot(np.sum(E_history, axis=0), label = 'Exposed')
plt.plot(np.sum(I_history, axis=0), label = 'Infected')
plt.plot(np.sum(R_history, axis=0), label = 'Recovered')
plt.legend()
plt.title("SEIR Model in Watts Strogatz Graph")
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()