import numpy as np
import option_pricer.option_class as oc
from scipy.stats import norm

def NaiveMonteCarloPricer(option, payoff, nreps = 10000):
    spots = np.empty(nreps)
    option_values = np.empty(nreps)
    z = np.random.normal(size = nreps)
    spots = option.S_0 * np.exp((option.r - option.delta - 1/2*option.sigma**2) + option.sigma*np.sqrt(option.T)*z)
    option_values = payoff(spots, option.strike)
    est_value = option_values.mean()
    est_value = np.exp(-(option.r - option.delta)*option.T) * est_value
    est_value_std = option_values.std()
    est_value_std_error = est_value_std/np.sqrt(nreps)
    return est_value, est_value_std_error
