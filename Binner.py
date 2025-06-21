import numpy as np


class Binner:
    """
    The purpose of this class is to convert from a float to an integer or
    vice versa. The integer labels the location of the bin in which the
    float falls. The bins are contiguous and all have the same length
    `delta_x` except possibly the last one, which might be smaller. They
    start at the float `xmin` and end before the float `xmax`.

    Attributes
    ----------
    delta_x: float
    levels: list[float]
        list of points that mark beginning and end of bins
    num_bins: int
        number of bins
    xmax: float
    xmin: float

    """

    def __init__(self, num_bins, xmin=0, xmax=1):
        """
        Constructor

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
        This method converts from float x to int xbin.

        Parameters
        ----------
        x: float

        Returns
        -------
        int

        """
        assert self.xmin <= x <= self.xmax
        xbin = self.num_bins - 1
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
        This method converts from list[float] xs to list[int] xbins.

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
        This method converts from int xbin to float x.

        Parameters
        ----------
        xbin: int

        Returns
        -------
        float

        """
        assert 0 <= xbin < self.num_bins
        return xbin * self.delta_x

    def get_xs(self, xbins):
        """
        This method converts from list[int] xbins to list[float] xs.

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
        xs = [0, .43, .5, .53, 1]
        print("xs=", xs)
        xbins = binner.get_xbins(xs)
        print("xbins=", xbins)
        xs2 = binner.get_xs(xbins)
        print("xs2=", xs2)


    main()
