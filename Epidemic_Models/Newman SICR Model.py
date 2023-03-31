
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define parameters
beta = 0.02 # infection rate
gamma = 0.05 # Carrier rate
alpha = 0.02 # recovery rate from carrier
t_max = 100 # number of time steps

# Define the graph
n = 100 # number of nodes
k = 10 # number of nearest neighbors to connect
p = 0.1 # probability of rewiring
G = nx.newman_watts_strogatz_graph(n, k, p)

# Initialize state arrays
S = np.ones(n)
I = np.zeros(n)
C = np.zeros(n)
R = np.zeros(n)
I[0] = 1 # initial infected node

# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
C_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
I_history[:, 0] = I
C_history[:, 0] = C
R_history[:, 0] = R

pos = nx.spiral_layout(G)

# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('Epidemic Spread on Newman Graph (SICR Model)')
   
    nx.draw(G, pos, node_color=['blue' if i == 0 else 'red' if i == 1 else 'orange' if i == 2 else 'green' for i in np.argmax(np.vstack([S,I,C,R]), axis=0)])
    plt.text(-1.3, 1.3, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, 1.2, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, 1.1, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-1.3, 1.0, f'Carrier Nodes: {int(np.sum(C))}')
    plt.text(-1.3, 0.9, f'Recovered Nodes: {int(np.sum(R))}')

# Define animation function
def update(t):
    global S, I, C, R

    # Infect susceptible neighbors
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < beta:
                        S[j] = 0
                        I[j] = 1

    # Move some infected individuals to carrier state
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                I[i] = 0
                C[i] = 1

    # carrier to recovered
    for i in range(n):
        if C[i] == 1:
            if np.random.rand() < alpha:
                C[i] = 0
                R[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    C_history[:, t] = C
    R_history[:, t] = R

    # Plot current state
    plot_infection(t)

# Create animation
ani = FuncAnimation(plt.gcf(), update, frames=t_max, interval=50, repeat=False)

# Show the animation
plt.show()

# Plot Results
plt.plot(np.sum(S_history, axis=0), label='Susceptible')
plt.plot(np.sum(I_history, axis=0), label='Infected')
plt.plot(np.sum(C_history, axis=0), label='Carriers')
plt.plot(np.sum(R_history, axis=0), label='Recovered')
plt.legend()
plt.title("SICD Model in Newman Graph")
plt.xlabel('Time')
plt.ylabel('Number of Individuals')
plt.show()

