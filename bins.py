from __future__ import division
from copy import deepcopy
from collections import namedtuple
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "WTFPL"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
Discrete technique. Binning the one array into equal size bin.
Rewrite from Dr. Tim Menzies. https://github.com/timm/luamine/blob/master/v1.0-3/bins.lua
"""


class ListStat(object):
    def __init__(self):
        self.mu = 0
        self.n = 0
        self.m2 = 0

    def __repr__(self):
        return "mu = %f, n = %d, m2 = %f" % (self.mu, self.n, self.m2)


def num1(z, stat):
    """
    update the list_stat if z is added to the list
    :param z: number
    :param stat: ListStat value
    :return: ListStat value
    """
    stat.n += 1
    delta = z - stat.mu
    stat.mu += delta / stat.n
    stat.m2 += delta * (z - stat.mu)

    if abs(stat.m2) < 1e-4:
        stat.m2 = 0

    return stat


def unnum(z, stat):  # opposite to num1
    if stat.n == 1:
        stat.n, stat.mu, stat.m2 = 0, 0, 0
        return stat

    stat.n -= 1
    delta = z - stat.mu
    stat.mu -= delta / stat.n
    stat.m2 -= delta * (z - stat.mu)

    if abs(stat.m2) < 1e-4:
        stat.m2 = 0

    return stat


def num0(l=[]):
    """
    create the list_stat value basing on the l
    :param l: a list
    :return: ListStat value
    """
    stat = ListStat()
    for element in l:
        stat = num1(element, stat)
    return stat


def sd(stat):  # get standard deviation from ListStat
    return (stat.m2 / (stat.n - 1)) ** 0.5 if stat.n > 1 else 0


BinInfo = namedtuple("BinInfo", "enough cohen maxBins minBin small verbose trivial")
Range = namedtuple("Range", "lo also n up")
ranges = []


def bins1(i, nums, all, lvl):
    if i.verbose:
        print "|.."*lvl, str(nums)

    cut = -1
    n = len(nums)
    start, stop = nums[0], nums[-1]

    if stop - start >= i.small:
        lhs, rhs = num0(), deepcopy(all)
        score, score1 = sd(rhs), None
        old = None
        for j, new in enumerate(nums):
            num1(new, lhs)
            unnum(new, rhs)
            score1 = (lhs.n * sd(lhs) + rhs.n * sd(rhs)) / n
            if new != old and lhs.n >= i.enough and rhs.n >= i.enough and \
                    new - start >= i.small and score1 * i.trivial < score:
                cut, score, lo, hi = j, score1, deepcopy(lhs), deepcopy(rhs)
            old = new

        if cut != -1:
            bins1(i, nums[:cut+1], lo, lvl+1)
            bins1(i, nums[cut+1:], hi, lvl+1)
        else:  # we've found a leaf range
            global ranges
            ranges.append(Range(lo=start, also=None, n=len(nums), up=stop))


def bins(t, enough=None, cohen=0.2, maxBins=16, minBin=4, small=None, verbose=False, trivial=1.05):
    nums = sorted(t)
    all = num0(t)
    enough = enough or max(minBin, all.n/maxBins)
    small = small or sd(all) * cohen
    i = BinInfo(enough, cohen, maxBins, minBin, small, verbose, trivial)
    bins1(i, nums, all, 1)
    return ranges


# def test():
#     import random
#     nums = [1, 24, 17, 21, 17, 18, 11, 25, 18, 5, 19, 17, 7, 11, 26, 11, 21, 6, 13, 3]
#     print sorted(nums)
#     ranges = bins(nums, maxBins=4, verbose=False)
#     for r in ranges:
#         print r
#
#
# if __name__ == '__main__':
#     import sys, traceback
#     try:
#         test()
#     except:
#         type, value, tb = sys.exc_info()
#         traceback.print_exc()
#         pdb.post_mortem(tb)
