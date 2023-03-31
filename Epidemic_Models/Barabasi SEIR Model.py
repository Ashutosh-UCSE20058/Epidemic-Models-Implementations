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
beta = 0.5 # contact rate
delta = 0.02 # infection rate
gamma = 0.083 # recovery rate

t_max = 100 # number of time steps



# Define the strogatz graph
n = 100 # number of nodes
m = 5 # number of edges
G = nx.barabasi_albert_graph(n,m)

# Initialize state arrays
S = np.ones(n)
E = np.zeros(n)
I = np.zeros(n)
R = np.zeros(n)
I[0] = 1 # initial infected node


# Initialize history arrays
S_history = np.zeros((n, t_max))
I_history = np.zeros((n, t_max))
R_history = np.zeros((n, t_max))
E_history = np.zeros((n, t_max))

# Store initial states
S_history[:, 0] = S
E_history[:, 0] = E
I_history[:, 0] = I
R_history[:, 0] = R

pos = nx.random_layout(G)
# Define plot function
def plot_infection(t):
    plt.clf()
    plt.title('Epidemic Spread on Barabasi Albert Graph')    
    node_colors = np.where(R == 1, 'green', np.where(I == 1, 'red', np.where(E == 1, 'orange','blue')))
    nx.draw(G, pos, node_color=node_colors)
    plt.text(-1.3, -1.3, f'Time Step: {t}/{t_max}')
    plt.text(-1.3, -1.2, f'Infected Nodes: {int(np.sum(I))}')
    plt.text(-1.3, -1.1, f'Susceptible Nodes: {int(np.sum(S))}')
    plt.text(-1.3, -1.1, f'Exposed Nodes: {int(np.sum(E))}')
    plt.text(-1.3, -1.0, f'Recovered Nodes: {int(np.sum(R))}')
    

# Define animation function
def update(t):
    global S, I, R, E
    # Susceptible to exposed
    for i in range(n):
        if I[i] == 1:
            neighbors = list(G.neighbors(i))
            lamda = sum(I)*beta/n #expose probabilty
            for j in neighbors:
                if S[j] == 1:
                    if np.random.rand() < lamda:
                        S[j] = 0
                        E[j] = 1

    # Exposed to infected 
    for i in range(n):
        if E[i] == 1:
            if np.random.rand() < delta:
                E[i] = 0
                I[i] = 1

    # infected to recovered
    for i in range(n):
        if I[i] == 1:
            if np.random.rand() < gamma:
                I[i] = 0
                R[i] = 1

    # Store current states in history arrays
    S_history[:, t] = S
    I_history[:, t] = I
    R_history[:, t] = R
    E_history[:, t] = E

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
