import pyagrum as gum
from globals import *
import pandas as pd
from  cpt_from_df import *
from ProbBound import *
from TriggerDecision import *
from Binner import *


def build_bnet(csv_file,
               danger_probs):
    """
    This method calculates the bnet (BayesNet) model for our Drought
    Anticipatory Action software. It uses the software pyagrum to do so.
    Some CPTs (TriggerDecision, ProbBound) are deterministic (learned from a
    deterministic function) whereas other CPTs are empirical probabilities (
    learned from a csv dataset)

    Parameters
    ----------
    csv_file: str
    danger_probs: list[float]
        danger probabilities

    Returns
    -------
    BayesNet

    """
    bn = gum.BayesNet('Drought Trigger Determination')
    rg_p = list(range(NUM_P_BINS))
    rg_e = list(range(-MAX_E, MAX_E + 1, 1))
    for i in range(NUM_X_FLAGS):
        bn.add(gum.IntegerVariable(f'X{i + 1}',
                                   f'X{i + 1}',
                                   [0, 1]))
    bn.add(gum.IntegerVariable('E',
                               'E',
                               rg_e))
    bn.add(gum.IntegerVariable('ProbBound',
                               'ProbBound',
                               rg_p))
    bn.add(gum.IntegerVariable('ProbImpactTail',
                               'ProbImpactTail',
                               rg_p))
    bn.add(gum.IntegerVariable('TriggerDecision',
                             'TriggerDecision',
                               [0, 1]))
    for name in LEAF_NODE_NAMES:
        bn.add(gum.IntegerVariable(name,
                                   name,
                                   rg_p))

    for i in range(NUM_X_FLAGS):
        bn.addArc(f"X{i + 1}", "ProbBound")
    bn.addArc("E", "ProbBound")
    print("ProbBound names=", bn.cpt("ProbBound").names)
    bn.addArc("ProbBound", "TriggerDecision")
    bn.addArc("ProbImpactTail", "TriggerDecision")
    print("TriggerDecision names=", bn.cpt("TriggerDecision").names)
    for name in LEAF_NODE_NAMES:
        bn.addArc("TriggerDecision", name)


    # root nodes
    for i in range(NUM_X_FLAGS):
        bn.cpt(f"X{i+1}").fillWith([0.5, 0.5])
    bn.cpt("ProbImpactTail").fillWith([1/NUM_P_BINS]*NUM_P_BINS)
    bn.cpt("E").fillWith([1 / NUM_E] * NUM_E)

    # non root nodes
    p3_cpt = ProbBound(danger_probs).get_cpt_array()
    bn.cpt("ProbBound")[:] = p3_cpt

    td_cpt=TriggerDecision().get_cpt_array()
    bn.cpt("TriggerDecision")[:]= td_cpt

    df = pd.read_csv(csv_file)
    br = Binner(NUM_P_BINS)
    for nd_name in LEAF_NODE_NAMES:
        df[nd_name] = df[nd_name].apply(br.get_xbin)
        learn_cpt_from_df(bn, df, nd_name)

    return bn


if __name__ == "__main__":

    def main():
        path = "data/leaf-nodes.csv"
        danger_probs = [.1, .5, .7]
        bn = build_bnet(path, danger_probs)

    main()