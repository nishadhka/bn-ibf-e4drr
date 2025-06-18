from itertools import product
from Binner import *
from globals import *


class ProbBound:

    def __init__(self, ins_costs, rep_costs):
        """

        Parameters
        ----------
        ins_costs: list[float]
            insurance costs
        rep_costs: list[float]
            replacement cost
        """
        assert len(ins_costs) == len(rep_costs)
        rg = range(len(rep_costs))
        assert all([ins_costs[i] <= rep_costs[i] for i in rg])
        self.ins_costs = ins_costs
        self.rep_costs = rep_costs
        self.br = Binner(NUM_P_BINS, 0, 1)

    def get_prob_bd_bin(self, x_flags):
        """

        Parameters
        ----------
        x_flags: list[bool]

        Returns
        -------
        float

        """

        assert len(x_flags) == len(self.rep_costs), \
            f"len {x_flags} != len {self.rep_costs}"

        rep_tot = 0
        ins_tot = 0
        for i in range(len(x_flags)):
            rep_tot += self.rep_costs[i]
            ins_tot += self.ins_costs[i] * x_flags[i]
        prob_bd = ins_tot / rep_tot
        return self.br.get_xbin(prob_bd)

    def get_cpt_array(self):
        """

        Returns
        -------
        np.array

        """
        num_x = len(self.rep_costs)
        shape = (2 ** num_x, NUM_P_BINS)
        ar = np.zeros(shape)
        row = 0
        for x_flags in product([0, 1], repeat=num_x):
            for prob_bd_bin in range(NUM_P_BINS):
                if prob_bd_bin == self.get_prob_bd_bin(x_flags):
                    ar[row, prob_bd_bin] = 1
                    break
            row += 1
        return ar


if __name__ == "__main__":
    def main():
        ins_costs = [3, 4, 3, 9, 1]
        rep_costs = [6, 12, 5, 17, 6]
        td = ProbBound(ins_costs, rep_costs)
        ar = td.get_cpt_array()
        print("array transpose = P(ProbBound|X_flags)")
        print(ar)


    main()
