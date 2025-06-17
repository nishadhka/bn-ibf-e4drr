import numpy as np
from itertools import product


class TriggerDecision:

    def __init__(self, num_p_bins):
        self.num_p_bins = num_p_bins

    def get_cpt(self):
        shape = (self.num_p_bins**2, 2)
        ar = np.zeros(shape)
        row = 0
        for tail_prob_bin, prob3_bin in\
            product(self.num_p_bins, self.num_p_bins):
            for trigger in [0, 1]:
                if tail_prob_bin > prob3_bin:
                    ar[row, trigger] = 1
                    break
            row += 1
        return ar