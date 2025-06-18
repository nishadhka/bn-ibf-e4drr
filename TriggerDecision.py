import numpy as np
from itertools import product


class TriggerDecision:

    def __init__(self, num_p_bins):
        """

        Parameters
        ----------
        num_p_bins: int
        """
        self.num_p_bins = num_p_bins

    def get_cpt_array(self):
        """

        Returns
        -------
        np.array

        """
        shape = (self.num_p_bins ** 2, 2)
        ar = np.zeros(shape)
        row = 0
        rg = range(self.num_p_bins)
        for tail_prob_bin, prob3_bin in product(rg, rg):
            # print("vbnw",tail_prob_bin, prob3_bin)
            for trigger in [0, 1]:
                if bool(trigger) == (tail_prob_bin > prob3_bin):
                    ar[row, trigger] = 1
            row += 1
        return ar


if __name__ == "__main__":
    def main():
        td = TriggerDecision(num_p_bins=3)
        ar = td.get_cpt_array()
        print("array transpose = "
              "P(TriggerDecision|ProbBound, ProbImpactTail)")
        print(ar)

    main()
