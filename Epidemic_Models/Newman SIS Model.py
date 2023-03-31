import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse
import networkx as nx
from matplotlib.animation import FuncAnimation

#we are assuming a rumour spread model, as rumours have a higher infection rate, 
#we take beta to be 0.5 and also considering how fast they can die out we take gamma to be 0.3

beta = 0.5 # infection rate
gamma = 0.3 # recovery rate

t_max = 100 # number of time steps


G = nx.Graph()
G.add_nodes_from(range(769))


# Define the strogatz graph
n = 100 # number of nodes
k = 4 # number of nearest neighbors to connect
p = 0.3 # probability of rewiring
G = nx.newman_watts_strogatz_graph(n, k, p)

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
