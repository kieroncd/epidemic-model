import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint


fig = plt.figure(figsize=(10,6))
ax = plt.axes(xlim=(0,365), ylim=(0, 8000))
ax.set_xlabel('Days Since First Infection',fontsize=14)
ax.set_ylabel('Current Number Infected',fontsize=14)

line, = ax.plot([], [], lw=2)

time = np.arange(0, 365)
dur = np.arange(5, 51, 0.2)
dur = np.concatenate((dur, dur[::-1]))

def init():
    line.set_data([], [])
    return line,

def SIR(u, t, n=1000, p=0.1, num_contacts=1, infection_duration=14):
    i, r = u

    didt = p * (n - i - r) * i / (n-1) - i / infection_duration
    drdt = + i / infection_duration

    return [didt, drdt]


def compute_infections(infection_duration):
    return odeint(SIR, [1, 0], time, args=(1e4, 0.2, 1, infection_duration))[:, 0]


def animate(i):
    ax.collections.clear()
    inf = compute_infections(i)
    line.set_data(time, inf)
    plt.legend([f'Average Infection Duration: {i:.2f} days'], loc='upper right')
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=dur, interval=35)

plt.show()
