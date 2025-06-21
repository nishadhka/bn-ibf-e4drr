from itertools import product
from Binner import *
from globals import *


class ProbBound:
    """
    Let A = ProbBound, pa(ProbBound) = X1, X2, X3, ..., E

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
    br: Binner
    ins_costs: list[float]
        insurance costs
    rep_costs: list[float]
        replacement costs

    """

    def __init__(self, ins_costs, rep_costs):
        """
        Constructor

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
        This method calculates the probability bound (in bin units). This
        bound equals a deterministic function f(ins_costs, rep_costs,
        x_flags) plus the noise e


        Parameters
        ----------
        x_flags: list[int]
            This is a list of binary integers (0 or 1)
        e: int
            error (i.e., noise), expressed in bin units, not float units

        Returns
        -------
        float

        """
        assert all([flag==0 or flag==1 for flag in x_flags])
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
        This method returns the CPT of node TriggerDecision as a numpy
        array. The CPT is a deterministic and is calculated using the method
        get_prob_bd_bin()


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