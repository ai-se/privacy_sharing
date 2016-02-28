from __future__ import division
import math


__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
set of tools for handling csv data
"""


def str2num(s):
    try:
        s = int(s)
    except ValueError:
        try:
            s = float(s)
        except ValueError:
            pass
    return s


def binrange(datalist, bin_number=10):
    """
    :param datalist:
    :param bin_number:
    :return: list of bin# e.g. {a,b,c,d,e} [a,b] (b,c] (c,d] [d,e]
    """
    l = sorted(datalist)
    bin_size = math.ceil(len(l)/bin_number)
    # print bin_size
    boundary = [l[0]]
    for i in range(0, len(l)):
        if (i+1) % bin_size == 0:
            boundary.append(l[i])
    if l[-1] not in boundary:
        boundary.append(l[-1])
    return boundary


def self_determine_bin_size(list_of_data):
    """
    Given the list, return the bin size automatically
    :param list:
    :return: bin size
    """
    return min(len(set(list_of_data)), 10)


def attr_norm(all_elements):
    """
    This is the normalization/de-normalization function generator for one kind of attribute
    :param all_elements: all the elements for one attribute
    :return: two functions. The first one can normalize the element; the second one is de-normalize the element

    e.g.
    loc = [100,200,100,300]
    norm_loc, denorm_loc = attr_norm(loc)
    l1 = map(norm_loc,loc)
    l2 = map(denorm_loc, l1)
    print l1 # [0.0, 0.5, 0.0, 1.0]
    print l2 # [100.0, 200.0, 100.0, 300.0]
    """
    if not type(all_elements) is list: all_elements = [all_elements]
    M = max(all_elements)
    m = min(all_elements)

    def norm(element):
        return (element-m)/(M-m) if M != m else 1

    def denorm(element):
        s = element*(M-m)+m if M != m else m
        return max(min(s, M), m)  # TODO has better solution for privacy preserving?

    return norm, denorm


def euclidean_dist(x, y):
    if type(x) is not list:
        x = [x]
    if type(y) is not list:
        y = [y]

    assert len(x) == len(y), "the dimension of two parameters must be the same"

    return sum([(i-j)**2 for i, j in zip(x, y)]) ** 0.5

# x = [0,0,0]
# y = [1,1,1]
# print euclidean_dist(x,y)
