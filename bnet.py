import pyagrum as gum
from globals import *
import pandas as pd
from  cpt_from_df import *
from ProbBound import *
from TriggerDecision import *


def build_bnet(csv_file,
               ins_costs,
               rep_costs):
    """

    Parameters
    ----------
    csv_file: str
    ins_costs: list[float]
    rep_costs: list[float]

    Returns
    -------
    BayesNet

    """
    bn = gum.BayesNet('Drought Trigger Determination')
    for i in range(NUM_X_FLAGS):
        bn.add(gum.IntegerVariable(f'X{i + 1}',
                                   f'X{i + 1}',
                                   range(2)))
    bn.add(gum.IntegerVariable('ProbBound',
                               'ProbBound',
                               range(NUM_P_BINS)))
    bn.add(gum.IntegerVariable('ProbImpactTail',
                               'ProbImpactTail',
                               range(NUM_P_BINS)))
    bn.add(gum.IntegerVariable('TriggerDecision',
                               'TriggerDecision',
                               range(2)))
    bn.add(gum.IntegerVariable('FAR',
                               'FAR',
                               range(NUM_P_BINS)))
    bn.add(gum.IntegerVariable('HR',
                               'HR',
                               range(NUM_HR_BINS)))
    bn.add(gum.IntegerVariable('AUROC',
                               'AUROC',
                               range(NUM_AUROC_BINS)))
    for i in range(NUM_X_FLAGS):
        bn.addArc(f"X{i + 1}", "ProbBound")
    bn.addArc("ProbBound", "TriggerDecision")
    bn.addArc("ProbImpactTail", "TriggerDecision")
    bn.addArc("TriggerDecision", "FAR")
    bn.addArc("TriggerDecision", "HR")
    bn.addArc("TriggerDecision", "AUROC")

    # root nodes
    for i in range(NUM_X_FLAGS):
        bn.cpt(f"X{i+1}").fillWith([0.5, 0.5])
    bn.cpt("ProbImpactTail").fillWith([1/NUM_P_BINS]*NUM_P_BINS)

    # non root nodes
    p3_cpt = ProbBound(ins_costs, rep_costs).get_cpt_array()
    bn.cpt("ProbBound")[:] = p3_cpt

    td_cpt=TriggerDecision().get_cpt_array()
    bn.cpt("TriggerDecision")[:]= td_cpt

    df = pd.read_csv(csv_file)
    learn_cpts_from_df(bn, df, ["FAR", "HR", "AUROC"])

    return bn


