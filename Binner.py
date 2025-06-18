import numpy as np


class Binner:
    """

    Attributes
    ----------
    delta_x: float
    levels: list[float]
    num_bins: int
    xmax: float
    xmin: float

    """

    def __init__(self, num_bins, xmin=0, xmax=1):
        """

        Parameters
        ----------
        num_bins: int
        xmin: float
        xmax: float
        """
        self.num_bins = num_bins
        assert xmax > xmin
        self.xmin = xmin
        self.xmax = xmax
        self.delta_x = (xmax - xmin) / num_bins
        self.levels = list(np.arange(xmin,
                                     xmax,
                                     self.delta_x))
        # print("levels=", self.levels)

    def get_xbin(self, x):
        """

        Parameters
        ----------
        x: float

        Returns
        -------
        int

        """
        xbin = self.num_bins-1
        for i, level in enumerate(self.levels):
            # print("ngrr", x, level)
            if x <= level:
                if x < level - self.delta_x / 2:
                    xbin = i - 1
                else:
                    xbin = i
                break
        return xbin

    def get_xbins(self, xs):
        """

        Parameters
        ----------
        xs: list[float]

        Returns
        -------
        list[int]

        """
        return [self.get_xbin(x) for x in xs]

    def get_x(self, xbin):
        """

        Parameters
        ----------
        xbin: int

        Returns
        -------
        float

        """
        return xbin * self.delta_x

    def get_xs(self, xbins):
        """

        Parameters
        ----------
        xbins: list[int]

        Returns
        -------
        list[float]

        """
        return [xbin * self.delta_x for xbin in xbins]


if __name__ == "__main__":
    def main():
        num_bins = 10
        xmin = 0
        xmax = 1
        binner = Binner(num_bins, xmin, xmax)
        print("levels=", binner.levels)
        xs = [0, .43, .5, .53, 1, 1.3]
        print("xs=", xs)
        xbins = binner.get_xbins(xs)
        print("xbins=", xbins)
        xs2 = binner.get_xs(xbins)
        print("xs2=", xs2)


    main()
