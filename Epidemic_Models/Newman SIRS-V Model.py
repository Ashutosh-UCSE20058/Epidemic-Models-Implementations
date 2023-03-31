import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.03  # infection rate
gamma = 0.02  # recovery rate
v = 0.005  # vaccination rate
mu = 0.005  # waning immunity rate
t_max = 100  # number of time steps

# # Define the strogatz graph
# n = 100 # number of nodes
# k = 4 # number of nearest neighbors to connect
# p = 0.1 # probability of rewiring
# G = nx.newman_watts_strogatz_graph(n, k, p)


# Initialize state arrays
S = np.ones(n)
I = np.zeros(n)
R = np.zeros(n)
V = np.zeros(n)

I[0] = 1  # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))
V_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
I_history[:, 0] = I
R_history[:, 0] = R
V_history[:, 0] = V

# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('Epidemic Spread on Barabasi Albert Graph')
    pos = nx.spiral_layout(G)
    node_colors = np.where(R == 1, 'green', np.where(I == 1, 'red', np.where(V == 1, 'pink','blue')))
    nx.draw(G, pos, node_color=node_colors)
    plt.text(-1.3, 1.3, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, 1.2, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, 1.1, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-1.3, 1.0, f'Recovered Nodes: {int(np.sum(R))}')
    plt.text(-1.3, 0.9, f'Vaccinated Nodes: {int(np.sum(V))}')

# Define animation function
def update(t):
    global S, I, R, V

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

    # Vaccinate susceptible individuals
    for i in range(n):
        if S[i] == 1:
            if np.random.rand() < v:
                S[i] = 0
                V[i] = 1

    
    # Waning immunity in recovered individuals
    for i in range(n):
        if R[i] == 1:
            if np.random.rand() < mu:
                R[i] = 0
                S[i] = 1

    

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    R_history[:, t] = R
    V_history[:, t] = V

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
plt.plot(np.sum(V_history, axis=0), label='Vaccinated')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()
