from itertools import product
from Binner import *
from globals import *


class ProbBound:
    """

    Attributes
    ----------
    br: Binner
    ins_costs: list[float]
    rep_costs: list[float]

    """

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
        x_flags: list[int]

        Returns
        -------
        float

        """

        assert len(x_flags) == len(self.rep_costs), \
            f"len {x_flags} != len {self.rep_costs}"

        prob_bd = 0
        for i in range(len(x_flags)):
            assert self.rep_costs[i] > 0
            prob_bd += (self.ins_costs[i]/self.rep_costs[i]) * x_flags[i]
        x_sum = np.sum(x_flags)
        if x_sum > 0:
            prob_bd /= x_sum
        else:
            prob_bd = 0
        return self.br.get_xbin(prob_bd)

    def get_cpt_array(self):
        """

        Returns
        -------
        np.array

        """
        shape = [2]* NUM_X_FLAGS
        shape.append(NUM_P_BINS)
        # print("xxcf", shape)
        ar = np.zeros(shape)
        row = 0
        for x_flags in product([0, 1], repeat=NUM_X_FLAGS):
            for prob_bd_bin in range(NUM_P_BINS):
                if prob_bd_bin == self.get_prob_bd_bin(list(x_flags)):
                    ar[*x_flags, prob_bd_bin] = 1
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
