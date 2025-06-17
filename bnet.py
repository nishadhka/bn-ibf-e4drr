import pyagrum as gum
from globals import *
import pandas as pd
from  cpt_from_df import *
from Prob3 import *
from TriggerDecision import *


def build_bnet(csv_file,
               prev_costs,
               repl_costs):
    bn = gum.BayesNet('Drought Trigger Determination')
    for i in range(NUM_X_FLAGS):
        bn.add(gum.IntegerVariable(f'X{i +}',
                                   f'X{i + 1}',
                                   2))
    bn.add(gum.IntegerVariable('Prob3',
                               'Prob3',
                               NUM_P_BINS))
    bn.add(gum.IntegerVariable('ProbImpactTail',
                               'ProbImpactTail',
                               NUM_P_BINS))
    bn.add(gum.IntegerVariable('TriggerDecision',
                               'TriggerDecision',
                               2))
    bn.add(gum.IntegerVariable('FAR',
                               'FAR',
                               NUM_FAR_BINS))
    bn.add(gum.IntegerVariable('HR',
                               'HR',
                               NUM_HR_BINS))
    bn.add(gum.IntegerVariable('AUROC',
                               'AUROC',
                               NUM_AUROC_BINS))
    for i in range(NUM_X_FLAGS):
        bn.addArc(f"X{i + 1}", "Prob3")
    bn.addArc("Prob3", "TriggerDecision")
    bn.addArc("ProbImpactTail", "TriggerDecision")
    bn.addArc("TriggerDecision", "FAR")
    bn.addArc("TriggerDecision", "HR")
    bn.addArc("TriggerDecision", "AUROC")

    # root nodes
    for i in range(NUM_X_FLAGS):
        bn.cpt(f"X{i+1}").fillWith([0.5, 0.5])
    bn.cpt("ProbImpactTail").fillWith([1/NUM_P_BINS]*NUM_P_BINS)

    # non root nodes
    p3_cpt = Prob3(prev_costs, repl_costs, NUM_P_BINS).get_cpt()
    bn.cpt("Prob3").fillWith(p3_cpt)

    td_cpt=TriggerDecision(NUM_P_BINS)
    bn.cpt("TriggerDecision").fillWith(td_cpt)

    df = pd.read_csv(csv_file)
    learn_cpt_from_df(bn, df, ["FAR", "HR", "AUROC")


