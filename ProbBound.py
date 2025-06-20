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

    def get_prob_bd_bin(self, e, *x_flags):
        """

        Parameters
        ----------
        x_flags: list[int]
        e: int

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
        prob_bd_bin = self.br.get_xbin(prob_bd) + e
        if prob_bd_bin < 0:
            prob_bd_bin = 0
        if prob_bd_bin >= NUM_P_BINS:
            prob_bd_bin = NUM_P_BINS - 1
        return prob_bd_bin

    def get_cpt_array(self):
        """

        Returns
        -------
        np.array

        """
        shape = [NUM_P_BINS]
        shape += [2] * NUM_X_FLAGS
        shape += [NUM_E]
        shape.reverse()
        # print("xxcf, shape", shape)
        ar = np.zeros(shape)
        rg_p = list(range(NUM_P_BINS))
        rg_e = list(range(-MAX_E, MAX_E + 1, 1))
        for x_flags in product([0, 1], repeat=NUM_X_FLAGS):
            for e in rg_e:
                prob_bd_bin = self.get_prob_bd_bin(e, *x_flags)
                for prob in rg_p:
                    # kk = [prob, *x_flags, e]
                    # print("all indices", kk)
                    if prob == prob_bd_bin:
                        jj = [prob, *x_flags, e]
                        # print("llkm, special", jj)
                        ar[tuple(reversed(jj))] = 1
                        break
        return ar


if __name__ == "__main__":
    def main():
        ins_costs = [3, 4, 3]
        rep_costs = [6, 12, 5]
        td = ProbBound(ins_costs, rep_costs)
        ar = td.get_cpt_array()
        print("array with index order reversed = P(ProbBound|X_flags, e)")
        print("array shape=", ar.shape)
        print(ar)


    main()