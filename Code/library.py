## LIBRARIES ##
import datetime as dt
import matplotlib as plt
import numpy as np
import pandas as pd

## CUSTOM FUNCTIONS ##
def logit(x):
    """ Returns the logit of x. """
    logit_x = np.log(x/(1-x))
    return logit_x

def invlogit(x):
    """ Inverts the logit function. """
    invlogit_x = np.exp(x)/(1 + np.exp(x))
    return invlogit_x

def wtd_var(x, weights = None):
    """ Returns the weighted variance of x, weighted by 'weights' argument.
    Defaults to unweighted variance. """
    ## Convert to nd.arrays
    x = np.array(x)
    if weights == None:
        weights = np.array(weights)
    
    w_mean = np.average(x, weights = weights)
    dev_sq = (x - w_mean) ** 2
    if weights == None:
        return dev_sq.sum()/(dev_sq.size - 1)
    else:
        n = sum(weights != 0)
        w_var = sum(dev_sq) / ((dev_sq.size - 1) * sum(weights))
        return w_var