import pyagrum as gum
from globals import *


def build_bnet(csv_file):
    bn = gum.BayesNet('Drought Trigger Determination')
    bn.add(gum.IntegerVariable('X_FLAGS',
                               'X_FLAGS',
                               2**NUM_X_FLAGS))
    bn.add(gum.IntegerVariable('Prob8',
                               'Prob8',
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
                               NUM_HR_BINS))
    bn.addArc("X_FLAGS", "Prob8")
    bn.addArc("Prob8", "TriggerDecision")
    bn.addArc("ProbImpactTail", "TriggerDecision")
    bn.addArc("TriggerDecision", "FAR")
    bn.addArc("TriggerDecision", "HR")
    bn.addArc("TriggerDecision", "AUROC")
    


