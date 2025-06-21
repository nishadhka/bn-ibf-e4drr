import numpy as np
import pandas as pd

def learn_cpt_from_df(bn, df, nd_name):
    """
    (modified, from pyagrum docs)

    This method calculates an empirical CPT from a pandas dataframe `df`.
    The method calculates and stores the CPT for node `nd_name` inside a
    BayesNet `bn`.

    Parameters
    ----------
    bn: gum.BayesNet
    df: pd.DataFrame
    nd_name: str

    Returns
    -------
    None
    """

    id = bn.idFromName(nd_name)
    parents = list(reversed(bn.cpt(id).names))
    domains = [bn[name].domainSize()
               for name in parents]
    parents.pop()  # this removes last element

    if (len(parents) > 0):
        c = pd.crosstab(df[nd_name], [df[parent] for parent in parents])
        s = c / c.sum().apply(np.float32)
    else:
        s = df[nd_name].value_counts(normalize=True)

    bn.cpt(id)[:] = np.array((s).transpose()).reshape(*domains)


def learn_cpts_from_df(bn, df, nd_names=None):
    """
    This method just iterates the method learn_cpt_from_df() over a list of
    nodes

    Parameters
    ----------
    bn: gum.BayesNet
    df: pd.DataFrame
    nd_names: list[str]

    Returns
    -------
    None

    """
    if not nd_names:
        nd_names = bn.names
    for name in nd_names:
        if name in bn.names():
            learn_cpt_from_df(bn, df, name)
