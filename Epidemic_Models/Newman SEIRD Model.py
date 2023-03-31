import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
from matplotlib.animation import FuncAnimation


# Define parameters
beta = 0.7  # contact rate
alpha = 0.5  # exposed to infected rate
gamma = 0.01 # recovery rate
mu = 0.1 # death rate
t_max = 100  # number of time steps


# Define the Barabasi-Albert graph
n = 100 # number of nodes
k = 5 # number of nearest neighbors to connect
p = 0.1 # probability of rewiring
G = nx.newman_watts_strogatz_graph(n,k,p)

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

pos = nx.spring_layout(G)
# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('SEIRD Epidemic Spread on Barabasi-Albert Graph')
    node_colors = np.where(D == 1, 'black', np.where(R == 1, 'green', np.where(I == 1, 'red', np.where(E == 1, 'orange', 'blue'))))
    nx.draw(G, pos, node_color=node_colors)
    plt.text(-1.3, -0.5, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, -0.6, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, -0.7, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-1.3, -0.8, f'Exposed Nodes: {int(np.sum(E))}')
    plt.text(-1.3, -0.9, f'Recovered Nodes: {int(np.sum(R))}')
    plt.text(-1.3, -1.0, f'Dead Nodes: {int(np.sum(D))}')


# Define animation function
def update(t):
    global S, E, I, R, D
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
plt.plot(np.sum(D_history, axis=0), label='Deaseased')
plt.legend()
plt.title("SEIRD Model in Newman Graph")
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()
