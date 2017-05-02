## long staff shorts method broadie and glasseman
## baysian / particle filters

import option_pricer.option_class as oc
import numpy as np
from scipy.stats import norm

def binomial_price(payoff, option, euro = True):
    if euro == True:
        probs = oc.calc_prob(option)
        spots = oc.calc_spot(option)
        disc = np.exp(-(option.r - option.delta)*option.T)
        return disc * sum(probs * payoff(spots, option.strike))
    if euro == False:
        option_value = 0
        spot_tree = np.zeros([option.nodes, option.nodes])
        price_tree = np.zeros([option.nodes, option.nodes])
        payoff_tree = np.zeros([option.nodes, option.nodes])
        disc = np.exp(-(option.r - option.delta)*(option.T/option.periods))
        nodes_start = option.nodes

        while (option.nodes >= 1):
            nodes = option.nodes
            spots = oc.calc_spot(option)
            if len(spots) < len(spot_tree):
                spots = np.append(spots, np.zeros(len(spot_tree)-len(spots)))
            spot_tree[:,(nodes-1)] = spots
            payoff_tree[:, (nodes - 1)] = payoff(spots, option.strike)
            option.set_nodes(nodes - 1)

        option.set_nodes(nodes_start)
        pu = option.prob * disc
        pd = (1-option.prob) * disc

        price_tree[:, option.periods] = payoff_tree[:, option.periods]

        for i in range(option.periods -1, -1, -1):
            for j in range(option.periods -1, -1, -1):
                price_tree[j, i] = price_tree[j, i+1]*pu + price_tree[j+1, i+1]*pd
                if price_tree[j, i] < payoff(spot_tree[j, i], option.strike):
                    price_tree[j, i] = payoff(spot_tree[j, i], option.strike)

        option_value = price_tree[0,0]

        return option_value

def black_scholes(option, call = True):
    discount = np.exp(-option.r*option.T)
    growth = np.exp((option.r-option.delta)*option.T)
    dplus = (option.sigma*np.sqrt(option.T))**-1*(np.log(growth*option.S_0/option.strike)+1/2*option.sigma**2*option.T)
    dminus = (option.sigma*np.sqrt(option.T))**-1*(np.log(growth*option.S_0/option.strike)-1/2*option.sigma**2*option.T)

    if call == True:
        option_value = discount*(norm.cdf(dplus) * growth*option.S_0 - norm.cdf(dminus)* option.strike)
    if call == False:
        option_value = discount*(norm.cdf(-dminus)*option.strike - norm.cdf(-dplus) * growth*option.S_0)

    return option_value

def main():
    someoption=oc.Option(periods = 1000)
    someoption1 = oc.Option(periods = 1000)
    someoption2 = oc.Option()
    prc = binomial_price(oc.callpayoff,someoption, False)
    euro_prc = binomial_price(oc.callpayoff, someoption1, True)
    black_scholes_prc = black_scholes(someoption2)
    print(prc)
    print(euro_prc)
    print(black_scholes_prc)

if __name__ == '__main__':
    main()
