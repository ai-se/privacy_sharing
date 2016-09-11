from __future__ import division
import csv
import copy
import logging
import random
import settings
import pdb
import data_tools

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


def CLIFF(database_or_data,
          db_folder=None,
          write_out_folder=None):
    """
    Core function for CLIFF algorithm
    prune the data set according to the power
    attributes are discretized

    :param database_or_data: should be a csv file containing the original database, or the list containing the data
    :param db_folder: the folder name of db
    :param write_out_folder: where to write out the generated data base into "write_out_folder/***_p.csv"
    :return: the CLIFFED database
    """
    percentage = settings.CLIFF_percentage
    percentage /= 100 if percentage > 1 else 1

    if type(database_or_data) is str:
        # load the database
        with open(db_folder + '/' + database_or_data+'.csv', 'r') as db:
            reader = csv.reader(db)
            ori_attrs = next(reader)
            alldata = []
            for line in reader:
                alldata.append(line)
    else:
        alldata = database_or_data

    record_attrs = settings.record_attrs

    classes = [i[-1] for i in alldata]  # last column in the origin csv file
    classes = map(data_tools.str2num, classes)

    # get the power for each attribute
    # store them in a final table
    all_data_power = []
    for attr_index, attr in enumerate(record_attrs):
        temp = ori_attrs.index(attr)
        col = [i[temp] for i in alldata]
        try: col = map(int, col)
        except ValueError: col = map(float, col)
        E = data_tools.binrange(col)
        all_data_power.append(power(col, classes, E))

    all_data_power = map(list, zip(*all_data_power))  # transpose.

    cliff_out = list()
    cliff_out.append(record_attrs+ori_attrs[-1:])  # header

    # select the largest sum of power in each row from each class
    row_sum = [sum(row) for row_index, row in enumerate(all_data_power)]

    for cls in set(classes):
        row_sum_sub = [sum(row) for row_index, row in enumerate(all_data_power) if classes[row_index] == cls]
        minimum = sorted(row_sum_sub, reverse=True)[int(len(row_sum_sub) * percentage)]

        # create the cliff_out
        for row_index in range(len(alldata)):
            if classes[row_index] != cls: continue
            if row_sum[row_index] < minimum: continue  # prune due to low power
            temp_row = []
            for attr_index, attr in enumerate(ori_attrs[:-1]):
                if attr in record_attrs:
                    try: x = int(alldata[row_index][attr_index])
                    except ValueError: x = float(alldata[row_index][attr_index])
                    temp_row.append(x)
            temp_row.append(cls)
            cliff_out.append(temp_row)

    # write the cliff_out
    if write_out_folder:
        with open(write_out_folder + '/'+database + '.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(cliff_out)

    return cliff_out


def testing():
    CLIFF("school",
          "./Dataset",
          "./CliffOut",
          )

if __name__ == '__main__':
    testing()
