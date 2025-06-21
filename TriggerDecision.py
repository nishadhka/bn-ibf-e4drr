import numpy as np
from itertools import product
from globals import NUM_P_BINS


class TriggerDecision:
    """
    Let A = TriggerDecision, pa(TriggerDecision) = ProbBound, ProbImpactTail

    The purpose of this class is to find the CPT (Conditional Probability
    Table) for the node A. The node will have the same name as this class.
    The CPT will be given as a numpy array. The innermost index of the array
    corresponds to node A, and the other tensor indices will correspond to
    the parent nodes pa(A) of A.

    In the case of A, the CPT is deterministic. This means

    P(A|pa(A)) = delta(A, f(pa(A)))

    where delta(x, y) is the Kronecker delta function, and f(pa(A)) is some
    function of pa(A).

    Attributes
    ----------

    """

    def __init__(self):
        """
        Constructor

        Parameters
        ----------

        """

    def get_cpt_array(self):
        """
        This method returns the CPT of node TriggerDecision as a numpy
        array. The CPT is deterministic.

        Returns
        -------
        np.array

        """
        shape = (NUM_P_BINS, NUM_P_BINS, 2)
        ar = np.zeros(shape)
        rg = range(NUM_P_BINS)
        for prob_tail_bin, prob_bd_bin in product(rg, rg):
            # print("vbnw",prob_tail_bin, prob_bd_bin)
            for trigger in [0, 1]:
                if bool(trigger) == (prob_tail_bin > prob_bd_bin):
                    jj = [trigger, prob_bd_bin, prob_tail_bin]
                    ar[tuple(reversed(jj))] = 1
        return ar


if __name__ == "__main__":
    def main():
        td = TriggerDecision()
        ar = td.get_cpt_array()
        print("array with index order reversed = "
              "P(TriggerDecision|ProbBound, ProbImpactTail)")
        print(ar)

    main()
