from __future__ import division
import csv, copy, re
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
    :return: list of bin# e.g. {a,b,c,d,e} [a,b] (b,c] (c,d] [d,e]
    """
    l = sorted(datalist)
    bin_size = int(len(l)/bin_number)
    #print bin_size
    boundary = [l[0]]
    for i in range(0, len(l)):
        if (i+1) % bin_size == 0:
            boundary.append(l[i])
    if l[-1] not in boundary: boundary.append(l[-1])
    return boundary


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


def CLIFF(database, percentage, writeout=False, record_attrs=['all_attributes'], bin_sizes=['self determine']):
    """
    Core function for CLIFF algorithm
    prune the data set according to the power
    attributes are discretized

    :param database: should be a csv file containing the original database
    :param percentage: the percentage of data to be return
    :param writeout: whether to write out the generated data base into "CliffOut/***_p.csv"
    :param record_attrs: specify the recording attributes. if not set, all numeric attributes will be considered
    :param bin_sizes: the bin_sizes for each record_attrs.
    :return: the CLIFFED database
    """
    percentage /= 100 if percentage > 1 else 1

    assert len(record_attrs) == len(bin_sizes), \
        "bin_size should be matched with the record_attrs. CANNOT set only one of them"

    # load the database
    with open('Dataset/'+database+'.csv', 'r') as db:
        reader = csv.reader(db)
        original_attributes = next(reader)
        alldata = []
        for line in reader:
            alldata.append(line)

    # determine which original_attributes to the record, as well as the perfect bin size
    if 'all_attributes' in record_attrs:
        record_attrs=[]
        for attr in range(len(original_attributes)-1):  # the last attr is the CLASS
            col = [original_data_row[attr] for original_data_row in alldata]  # get the col in this attribute
            if len(set(col)) == 1: continue  # all rows are the same in this attr. Not informative. Ignore it
            try:
                float(col[0])  # numeric? testing
                record_attrs.append(original_attributes[attr])
            except ValueError:
                continue
    else:
        for ra in record_attrs:
            assert ra in original_attributes, "record_attrs must be in the database"

    # determine the best bin size
    if 'self determine' in bin_sizes:
        bin_sizes = []
        for attr in record_attrs:
            temp = original_attributes.index(attr)
            col = [original_data_row[temp] for original_data_row in alldata]
            bin_sizes.append(min(len(set(col)), 10))
    else:
        assert len(bin_sizes) == len(record_attrs), "bin_siezes and record_attrs must have the same size when setting"

    # binary the classification
    # TODO binary?!
    classes = [i[len(original_attributes)-1] for i in alldata]  # last column in the origin csv file
    classes = [int(bool(int(c))) for c in classes]

    # get the power for each attribute
    # store them in a final table
    all_data_power = []
    for attr_index, attr in enumerate(record_attrs):
        temp = original_attributes.index(attr)
        col = [i[temp] for i in alldata]
        try: col = map(int, col)
        except ValueError: col = map(float, col)
        E = binrange(col, bin_sizes[attr_index])
        all_data_power.append(power(col, classes, E))

    all_data_power = map(list, zip(*all_data_power))  # transpose.

    cliffout = []
    cliffout.append(record_attrs+original_attributes[-1:])  # header

    # select the largest sum of power in each row from each class
    # TODO make sure the understanding here is correct
    row_sum = [sum(row) for row_index, row in enumerate(all_data_power)]

    for cls in set(classes):
        row_sum_sub = [sum(row) for row_index, row in enumerate(all_data_power) if classes[row_index] == cls]
        minimum = sorted(row_sum_sub, reverse=True)[int(len(row_sum_sub) * percentage)]

        # create the cliffout
        for row_index in range(len(alldata)):
            if classes[row_index] != cls: continue
            if row_sum[row_index] < minimum: continue  # prune due to low power
            temp_row = []
            for attr_index, attr in enumerate(original_attributes[:-1]):
                if attr in record_attrs:
                    try: x = int(alldata[row_index][attr_index])
                    except ValueError: x = float(alldata[row_index][attr_index])
                    temp_row.append(x)
            temp_row.append(cls)
            cliffout.append(temp_row)

    # write the cliffout
    if writeout:
        with open('CliffOut/'+database+'_'+str(percentage)+'.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(cliffout)

    return cliffout


def testing():
    # dataset = "./Dataset/"  # setting up the data set folder
    #
    # """
    # load the csv file by attributes
    # scripts from http://stackoverflow.com/questions/16503560/read-specific-columns-from-csv-file-with-python-csv
    # """
    # from collections import defaultdict
    # columns = defaultdict(list)  # each value in each column is appended to a list
    # with open(dataset + 'ant-1.3.csv') as f:
    #     reader = csv.DictReader(f)  # read rows into a dictionary format
    #     for row in reader:  # read a row as {column1: value1, column2: value2,...}
    #         for (k, v) in row.items():  # go over each column name and value
    #             columns[k].append(v)  # append the value into the appropriate list based on column name k
    #
    # # bug = map(int, columns['bug'])
    # # rfc = map(int, columns['rfc'])
    # # E = binrange(rfc)
    # #
    # # #wmc = [11,14,3,12,6,5,4,14]
    # # dit = [4,1,2,3,3,1,2,1]
    # # c = [0,1,0,0,0,0,0,1]
    # # E = binrange(dit,1)
    # # pwer = power(dit,c,E)
    #
    # ce = [12,4,1,12,4,1,3,20]
    # c = [0,1,0,0,0,0,0,1]
    # E = binrange(ce, 2)
    # pwer = power(ce,c,E)
    # pdb.set_trace()

    CLIFF('ant-1.7', 20, writeout=True)

if __name__ == '__main__':
    testing()
