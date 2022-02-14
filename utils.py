import numpy as np


def seasonality(time, strength, shift):
    return 1 + strength* np.cos(2 * np.pi / 365 * (time - shift))
