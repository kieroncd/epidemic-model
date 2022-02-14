import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.integrate import odeint
from models import sir_waning


def compute_infections(args):
    return odeint(sir_waning, [1, 0, n-1], time, args=args)[:, 0]


def update(val):
    line.set_ydata(compute_infections((n,
                                      infection_chance.val,
                                      num_contacts.val,
                                      infection_time.val,
                                      waning_time.val)))
    ax.set_title(f'R0 = {infection_chance.val * num_contacts.val * infection_time.val:.1f}')


end_date = 730
time = np.arange(0, end_date)
n = 1e7
fig = plt.figure(figsize=(10,6))
ax = plt.axes(xlim=(0,end_date), ylim=(0, n))

plt.subplots_adjust(bottom=0.4)
ax.set_xlabel('Days Since First Infection',fontsize=14)
ax.set_ylabel('Current Number Infected',fontsize=14)
line, = ax.plot([], [], lw=2)


line.set_data(time,[compute_infections((n, 0.1, 1, 14, 90))])
ax.set_title(f'R0 = {0.1 * 1 * 14:.1f}')
axp0 = plt.axes([0.15, 0.1, 0.65, 0.03])
axnc = plt.axes([0.15, 0.15, 0.65, 0.03])
axit = plt.axes([0.15, 0.20, 0.65, 0.03])
axwt = plt.axes([0.15, 0.25, 0.65, 0.03])

infection_chance = pylab.Slider(axp0, 'infection chance', 0.01, 0.2, valinit=0.1, valstep=0.01)
num_contacts = pylab.Slider(axnc, 'num contacts', 0.1, 10, valinit=1, valstep=0.1)
infection_time = pylab.Slider(axit, 'infection time', 1, 50, valinit=14, valstep=1)
waning_time = pylab.Slider(axwt, 'waning time', 10, 180, valinit=90, valstep=1)

infection_chance.on_changed(update)
num_contacts.on_changed(update)
infection_time.on_changed(update)
waning_time.on_changed(update)

plt.show()
