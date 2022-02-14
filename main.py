import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint


end_date = 730
time = np.arange(0, end_date)
n = 1e7
base_infection_chance = 0.1
base_num_contacts = 1
base_waning_time = 90

fig = plt.figure(figsize=(10,6))
ax = plt.axes(xlim=(0,end_date), ylim=(0, n))
ax.set_xlabel('Days Since First Infection',fontsize=14)
ax.set_ylabel('Current Number Infected',fontsize=14)
line, = ax.plot([], [], lw=2)


def sir(u, t, n=1000, p=0.1, num_contacts=1, infection_duration=14):
    '''
    Basic SIR model

    Parameters
    ----------
    n : int, optional
        number of people in the population. The default is 1000.
    p : float, optional
        transmissibility; how likely a contact of a susceptible with an infected
        will result in an infection. The default is 0.1.
    num_contacts : float, optional
        average number of contacts per individual. The default is 1.
    infection_duration : int, optional
        average length of time an individual is infectious. The default is 14.

    Returns
    -------
    list
        list of first order ODEs describing the infected, recovered and
        susceptible populations.

    '''
    i, r, s = u

    didt = p * (n - i - r) * i * num_contacts / (n-1) - i / infection_duration
    drdt = + i / infection_duration
    dsdt = - didt - drdt

    return [didt, drdt, dsdt]


def sir_waning(u, t, n=1000, p=0.1, num_contacts=1, infection_duration=14,
               waning_time=90):
    '''
    Basic SIR model with waning immunity

    Parameters
    ----------
    n : int, optional
        number of people in the population. The default is 1000.
    p : float, optional
        transmissibility; how likely a contact of a susceptible with an infected
        will result in an infection. The default is 0.1.
    num_contacts : float, optional
        average number of contacts per individual. The default is 1.
    infection_duration : int, optional
        average length of time an individual is infectious. The default is 14.
    waning_time : int, optional
        average length of time before a recovered individual becomes
        susceptible. The default is 90.

    Returns
    -------
    list
        list of first order ODEs describing the infected, recovered and
        susceptible populations.

    '''
    i, r, s = u

    didt = p * (n - i - r) * i * num_contacts / (n-1) - i / infection_duration
    drdt = + i / infection_duration - r / waning_time
    dsdt = - didt - drdt

    return [didt, drdt, dsdt]


def compute_infections(args):
    return odeint(sir_waning, [1, 0, n-1], time, args=args)[:, 0]


def animate(i):
    ax.collections.clear()
    inf = compute_infections((n, base_infection_chance, base_num_contacts, i, base_waning_time))
    line.set_data(time, inf)
    ax.set_title(f'R0 = {base_infection_chance*base_num_contacts*i:.2f}')
    plt.legend([f'Average Infection Duration: {i:.2f} days'], loc='upper right')
    return line,


if __name__ == '__main__':
    durations = np.arange(1, 91, 1)
    durations = np.concatenate((durations, durations[::-1]))
    anim = animation.FuncAnimation(fig, animate, frames=durations, interval=55)
    plt.show()
