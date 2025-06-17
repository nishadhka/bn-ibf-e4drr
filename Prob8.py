from itertools import product
from Binner import *


class Prob8:

    def __init__(self, prev_costs, repl_costs, num_p_bins):
        assert len(prev_costs) == len(repl_costs)
        assert all([prev_costs[i] <= repl_costs[i] for i in len(repl_costs)])
        self.prev_costs = prev_costs
        self.repl_costs = repl_costs
        self.num_p_bins = num_p_bins
        self.br = Binner(self.num_p_bins, 0, 1)

    def get_prob8_bin(self, x_flags):

        assert len(x_flags) == len(self.repl_costs)

        cost_tot = 0
        loss_tot = 0
        for i in range(len(x_flags)):
            loss_tot += self.prev_costs[i] * x_flags[i]
            cost_tot += self.repl_costs[i]
        prob8 = cost_tot / loss_tot
        return self.br.get_xbin(prob8)

    def get_cpt(self):
        num_x = len(self.repl_costs)
        shape = (2 ** num_x, self.num_p_bins)
        ar = np.zeros(shape)
        row = 0
        for x_flags in product([0, 1] * num_x):
            for prob8_bin in self.num_p_bins:
                if prob8_bin == self.get_prob8_bin(x_flags):
                    ar[row, prob8_bin] = 1
                    break
            row += 1
        return ar
