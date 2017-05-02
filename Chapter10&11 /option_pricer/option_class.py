import numpy as np
from scipy.stats import binom

class MarketData(object):

    def __init__(self, S_0 = 41.0, r=.08, sigma = .3, delta = 0):
        self.S_0 = S_0
        self.r = r
        self.sigma = sigma
        self.delta = delta

class Option(object):
    """
    Options are derivative securities

    Attributes:
        S_0 = initial spots
        r = Risk Free Rate
        sigma = Volatility
        strike = Strike Price
        T = Expiry length
        delta = dividend tail
        periods = Number of Compounds/Branches
        call = Type of option, True for Call, False for Put
    """

    def __init__(self, market_data = MarketData(), strike = 40.0, T = 1, periods = 2):
        self.S_0 = market_data.S_0
        self.r = market_data.r
        self.sigma = market_data.sigma
        self.delta = market_data.delta
        r = market_data.r
        delta = market_data.delta
        sigma = market_data.sigma
        self.strike = strike
        self.T = T
        self.periods = periods
        self.nodes = (periods + 1)
        self.upper = np.exp((r - delta)*T/periods + sigma*np.sqrt(T/periods))
        self.lower = np.exp((r - delta)*T/periods - sigma*np.sqrt(T/periods))
        self.prob = (np.exp(r * T/periods)-self.lower)/(self.upper - self.lower)
        self.h = float(T/periods)

    def set_nodes(self, nodes):
        self.nodes = nodes



def calc_prob(option):
    """ Calculates the Final Discrete Probability Distribution for an Option with N terminal nodes """
    nodes = option.nodes
    probs = np.zeros(nodes)
    if nodes > 2:
        for i in range(nodes):
            probs[i] = binom.pmf(k=i, n=option.periods, p = option.prob)
        probs = probs[::-1]
    else :
        probs = np.array([option.prob, 1 - option.prob])
    return probs

def calc_spot(option):
    """ Calculates the final terminal node spots for an Option with N terminal nodes """
    nodes = option.nodes
    current_spot = option.S_0
    if nodes > 2:
        spots = np.empty(nodes)
        for i in range(nodes):
            spots[i] = float(option.upper**(nodes - 1 - i)*option.lower**(i)*option.S_0)
    if nodes == 2:
        spots = np.array([float(option.upper*option.S_0), float(option.lower*option.S_0)])
    if nodes == 1:
        spots = np.array([current_spot])
    return spots


def callpayoff(spot,strike):
    return np.maximum(spot - strike, 0.0)
def putpayoff(spot, strike):
    return np.maximum(strike - spot, 0.0)
