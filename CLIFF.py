from __future__ import division
import copy
import logging
import random
import settings
import pdb
import toolkit
from toolkit import log_v

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"

"""
CLIFF algorithm
Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def power(L, C, Erange):
    """
    :param L: a list of values for one attribute in the data set
    :param C: the class corresponded to L list
    :param Erange: a st of sub-range for a given attribute. specifically, it's the boundary returned from binrange()
    :return: the power of each item in this attribute
    """
    assert len(L) == len(C), "The L and C must be corresponded to each other"
    E = copy.deepcopy(Erange)
    E[0] -= 1

    power_table = dict()
    for c in set(C):  # for each type of class
        first = [index for index, eachc in enumerate(C) if eachc == c]
        rest = [index for index, eachc in enumerate(C) if eachc != c]
        p_first = len(first) / len(L)
        p_rest = len(rest) / len(L)

        powerc = []
        for u, v in zip(E[0:-1], E[1:]):  # checking the range (u,v]
            like_first = sum([1 for i in first if u < L[i] <= v])/len(first) * p_first
            like_rest = sum([1 for i in rest if u < L[i] <= v])/len(rest) * p_rest
            try:
                powerc.append((like_first ** 2 / (like_first + like_rest)))
            except ZeroDivisionError:
                powerc.append(0)
        power_table[c] = powerc

    # filling the result by power_table
    power = []
    for l, c in zip(L, C):
        for e_cursor in range(len(E)):
            if E[e_cursor] >= l: break
        power.append(round(power_table[c][e_cursor-1], 2))

    return power


def cliff_core(data):
    """
    data has no header, only containing the record attributes
    :return the cliffed data (part of the input data)
    """

    if len(data) < 50:
        logging.debug("no enough data to cliff. return the whole dataset")
        return data

    percentage = settings.CLIFF_percentage
    percentage /= 100 if percentage > 1 else 1

    classes = map(toolkit.str2num, zip(*data)[-1])
    data_power = list()  # will be 2D list (list of list)
    for col in zip(*data):
        col = map(toolkit.str2num, col)
        E = toolkit.binrange(col)
        data_power.append(power(col, classes, E))

    data_power = map(list, zip(*data_power))  # transposing the data power
    row_sum = [sum(row) for row in data_power]

    zips = zip(data, classes, row_sum)

    output = list()
    for cls in set(classes):
        matched = filter(lambda z: z[1] == cls, zips)
        random.shuffle(matched)
        matched = sorted(matched, key=lambda z:z[2], reverse=True)

        if len(matched) < 5:
            output.extend([m[0] for m in matched])  # all saved
            continue

        for i in range(int(len(matched)*percentage)):
            output.append(matched[i][0])

    return output


def CLIFF(model,
          db_folder,
          write_out_folder=None):
    """
    Core function for CLIFF algorithm
    prune the data set according to the power
    attributes are discretized

    :param model: should be a csv file containing the original database
    :param db_folder: the folder name of db
    :param write_out_folder: where to write out the generated data base into "write_out_folder/model.csv"
    :return: the CLIFFED database
    """
    ori_attrs, alldata = toolkit.load_csv(db_folder, model)  # load the database
    record_attrs = settings.record_attrs

    alldataT = map(list, zip(*alldata))
    valued_dataT = list()
    for attr, col in zip(ori_attrs, alldataT):
        if attr in record_attrs:
            valued_dataT.append(col)
    valued_dataT.append(alldataT[-1])  # cant miss the classification

    alldata = map(list, zip(*valued_dataT))
    alldata = map(lambda row:map(toolkit.str2num, row), alldata)  # numbering the 2d table

    after_cliff = cliff_core(alldata)
    after_cliff.insert(0, record_attrs+[ori_attrs[-1]])  # add the header

    if write_out_folder:
        toolkit.write_csv(write_out_folder, model, after_cliff)

    return after_cliff


def testing():
    CLIFF("ant-1.7",
          "./Dataset",
          "./CliffOut",
          )

if __name__ == '__main__':
    testing()
