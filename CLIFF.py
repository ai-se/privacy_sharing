from __future__ import division
import csv
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
CLIFF algorithm
Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def binrange(datalist, bin_number=10):
    """
    :param datalist:
    :param bin_number:
    :return: list of bin# e.g. {a,b,c,d,e} [a,b) [b,c) [c,d) [d,e]
    """
    l = sorted(datalist)
    bin_size = round(len(l)/bin_number)
    # print bin_size
    boundary = [l[0]]
    for i in range(1, len(l)):
        if i % bin_size == 0:
            boundary.append(l[i])
    boundary.append(l[-1])
    return boundary


def power():
    return 1


def testing():
    dataset = "./Dataset/"  # setting up the data set folder

    """
    load the csv file by attributes
    scripts from http://stackoverflow.com/questions/16503560/read-specific-columns-from-csv-file-with-python-csv
    """
    from collections import defaultdict
    columns = defaultdict(list)  # each value in each column is appended to a list
    with open(dataset + 'ant-1.3.csv') as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into the appropriate list based on column name k

    print columns['avg_cc']


if __name__ == '__main__':
    testing()
