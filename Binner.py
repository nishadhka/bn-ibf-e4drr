import numpy as np


class Binner:

    def __init__(self, num_bins, xmin=0, xmax=1):
        self.num_bins = num_bins
        assert xmax > xmin
        self.xmin = xmin
        self.xmax = xmax
        self.delta_x = (xmax - xmin) / num_bins
        self.levels = list(np.arange(xmin,
                                     xmax + self.delta_x / 2,
                                     self.delta_x))
        # print("levels=", self.levels)

    def get_xbin(self, x):
        xbin = self.num_bins
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
        return [self.get_xbin(x) for x in xs]

    def get_x(self, xbin):
        return xbin * self.delta_x

    def get_xs(self, xbins):
        return [xbin * self.delta_x for xbin in xbins]


if __name__ == "__main__":
    def main():
        num_bins = 10
        xmin = 0
        xmax = 1
        binner = Binner(num_bins, xmin, xmax)
        xs = [0, .43, .5, .53, 1, 1.3]
        print("xs=", xs)
        xbins = binner.get_xbins(xs)
        print("xbins=", xbins)
        xs2 = binner.get_xs(xbins)
        print("xs2=", xs2)


    main()
