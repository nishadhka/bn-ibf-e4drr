import numpy as np
import pandas as pd


def learn_cpt_from_df(bn, df, name):
    """
    (modified, from pyagrum docs)

    Parameters
    ----------
    bn
    df
    name

    Returns
    -------

    """

    id = bn.idFromName(name)
    parents = list(reversed(bn.cpt(id).names))
    domains = [bn[name].domainSize()
               for name in parents]
    parents.pop()  # this removes last element

    if (len(parents) > 0):
        c = pd.crosstab(df[name], [df[parent] for parent in parents])
        s = c / c.sum().apply(np.float32)
    else:
        s = df[name].value_counts(normalize=True)

    bn.cpt(id)[:] = np.array((s).transpose()).reshape(*domains)


def learn_cpts_from_df(bn, df, nd_names=None):
    """

    Parameters
    ----------
    bn
    df
    nd_names

    Returns
    -------

    """
    if not nd_names:
        nd_names = bn.names
    for name in nd_names:
        if name in bn.names():
            learn_cpt_from_df(bn, df, name)
