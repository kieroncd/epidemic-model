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
