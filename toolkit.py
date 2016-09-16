from __future__ import division
import bins
import csv

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


def str2num(s):
    try:
        s = int(s)
    except ValueError:
        try:
            s = float(s)
        except ValueError:
            pass
    return s


def median(l):
    """
    return the median of the list l.
    l WILL NOT be changed.
    :param l:
    :return:
    """
    return sorted(l)[int(len(l)/2)]


def binrange(data_list, enough=None, cohen=0.2, maxBins=16, minBin=4, trivial=1.05):
    """

    :param data_list:
    :param enough:
    :param cohen:
    :param maxBins:
    :param minBin:
    :param trivial:
    :return: ist of bin# e.g. {a,b,c,d,e} [a,b] (b,c] (c,d] [d,e]
    """
    ranges = bins.bins(t=data_list, enough=enough, cohen=cohen,
                       maxBins=maxBins, minBin=minBin,trivial=trivial)
    res = [ranges[0].lo]
    for r in ranges:
        res.append(r.up)
    return res


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
        if m <= s <= M:
            return s
        elif m < s:
            s = 2 * m - s
        else:
            s = 2 * M - s
        return max(min(s, M), m)

    return norm, denorm


def euclidean_dist(x, y):
    """
    the Eulerian distance between x and y
    :param x: instance x. type--list or one number
    :param y: instance y. type--list or one number
    :return: the Eulerian distance between x and y
    """
    if type(x) is not list:
        x = [x]
    if type(y) is not list:
        y = [y]

    assert len(x) == len(y), "the dimension of two parameters must be the same"

    return sum([(i-j)**2 for i, j in zip(x, y)]) ** 0.5


def normalize_cols_for_table(table):
    """
    normalize a list of list--table
    data are grouped by cols
    :param table:
    :return:
    """
    result = []
    for col in zip(*table):
        f1, f2 = attr_norm(list(col))
        result.append(map(f1, col))
    return map(list, zip(*result))


def del_col_in_table(list_of_list, col_index):
    """
    delete one column or multiple columns in the table (list of list)
    :param list_of_list: data table
    :param col_index: index of the col. can be single number or a list. can be negative
    :return: new alloc pruned table
    """

    if type(col_index) is not list:
        col_index = [col_index]
    for i in range(len(col_index)):
        if col_index[i] < 0:
            col_index[i] += len(list_of_list[0])

    list_of_list = map(list, zip(*list_of_list))
    return_table = []
    for index, col in enumerate(list_of_list):
        if index not in col_index:
            return_table.append(col)
    return map(list, zip(*return_table))


def load_csv(folder, file_name, has_header=True):
    """
    loading the csv file at folder/file_name.csv
    :param folder:
    :param file_name:
    :param has_header:
    :return: (header if possible) + (content)
    """
    if '/' not in folder:
        folder += '/'
    with open(folder + file_name+'.csv', 'r') as db:
        reader = csv.reader(db)
        if has_header:
            header = next(reader)
        content = []
        for line in reader:
            content.append(line)
    if has_header:
        return header, content
    else:
        return content


def write_csv(folder, file_name, content, header=None):
    with open(folder + '/' + file_name + '.csv', 'w') as f:
        writer = csv.writer(f)
        if header is not None:
            writer.writerow(header)
        writer.writerows(content)


def log_v(variable, value):
    if type(value) is str:
        print(variable + ": " + value)
    else:
        print(variable + ": " + str(value))


def make_it_list(single_object_or_a_list):
    if type(single_object_or_a_list) is not list:
        single_object_or_a_list = [single_object_or_a_list]
    return single_object_or_a_list
