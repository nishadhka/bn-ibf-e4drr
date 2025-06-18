import numpy as np
from itertools import product
from globals import NUM_P_BINS


class TriggerDecision:
    """

    Attributes
    ----------

    """

    def __init__(self):
        """

        Parameters
        ----------
        """

    def get_cpt_array(self):
        """

        Returns
        -------
        np.array

        """
        shape = (NUM_P_BINS, NUM_P_BINS, 2)
        ar = np.zeros(shape)
        row = 0
        rg = range(NUM_P_BINS)
        for tail_prob_bin, prob_bd_bin in product(rg, rg):
            # print("vbnw",tail_prob_bin, prob_bd_bin)
            for trigger in [0, 1]:
                if bool(trigger) == (tail_prob_bin > prob_bd_bin):
                    ar[tail_prob_bin, prob_bd_bin, trigger] = 1
            row += 1
        return ar


if __name__ == "__main__":
    def main():
        td = TriggerDecision()
        ar = td.get_cpt_array()
        print("array transpose = "
              "P(TriggerDecision|ProbBound, ProbImpactTail)")
        print(ar)

    main()
