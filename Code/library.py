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

def pctile(n):
    def pctile_(x):
        return np.percentile(x, n)
    pctile_.__name__ = 'pctile_%s' % n
    return pctile_
