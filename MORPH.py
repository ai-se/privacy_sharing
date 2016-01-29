from __future__ import division
import csv, random, math
import pdb


__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"


"""
MORPH is an instance mutator that "shake" the data while maintain the data attributes. GOAL: the MORPHed data
    can be learned by other data-mining techniques as well as the original data.

Version 1.0--Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def eulerianDist(x, y):
    """
    the Eulerian distance between x and y
    :param x: instance x. type--list or one number
    :param y: instance y. type--list or one number
    :return: the Eulerian distance between x and y
    """
    if not type(x) is list: x = [x]
    if not type(y) is list: y = [y]
    assert len(x) == len(y), "Instance x and y must share the same dimension"

    return math.sqrt(sum([(a-b)**2 for a, b in zip(x, y)]))


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


def _str2num(s):
    try:
        s = int(s)
    except ValueError:
        s = float(s)
    return s


def MORPH(database, writeout=False, alpha=0.15, beta=0.35):
    """
    MORPH is a instance mutator which can shake the instance within the class boundary
    :param database: original data. fetch from the "CliffOut" folder
    :param writeout: where to write the result as a csv file. Default writing out folder is "MorphOut"
    :param alpha: shake amplitude lower bound
    :param beta: shake amplitude upper bound
    :return: the morphed data
    """
    # load the database
    with open('Cliffout/' + database + '.csv', 'r') as db:
        reader = csv.reader(db)
        attributes = next(reader)  # including the last one--class tag
        dataset = []
        for line in reader:
            dataset.append(line)
    dataset = [map(_str2num, row) for row in dataset]  # str to numeric
    is_int = [type(i) is int for i in dataset[0]]  # save. for better representation of the output table
    classes = [row[-1] for row in dataset]  # fetch the classes
    dataset = [row[:-1] for row in dataset]  # separating the raw data and class

    '''dataset transposed mode begins...'''
    dataset = map(list, zip(*dataset))  # transpose.
    norm_funcs = []
    denorm_funcs = []

    # normalizing
    for attr_index, attr_elements in enumerate(dataset):  # for each attribute elements
        f1, f2 = attr_norm(attr_elements)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
        dataset[attr_index] = map(f1, attr_elements)

    '''dataset mode recover...'''
    dataset = map(list, zip(*dataset))  # transpose again.

    for row_index, row in enumerate(dataset):  # for each row
        heterogeneous_index = [i for i in range(len(classes)) if classes[i] != classes[row_index]]
        boundary_dist = min([eulerianDist(row, dataset[heg]) for heg in heterogeneous_index])
        boundary_dist /= math.sqrt(len(attributes)-1)
        for i in range(len(row)):
            dataset[row_index][i] += boundary_dist*random.uniform(alpha, beta)*random.choice([1, -1]) # shake

    '''dataset transposed mode begins...'''
    dataset = map(list, zip(*dataset))  # transpose.
    for attr_index, attr_elements in enumerate(dataset):  # for each attribute elements
        dataset[attr_index] = map(denorm_funcs[attr_index], attr_elements)  # scale to the original
        for i in range(len(dataset[attr_index])):
            if is_int[attr_index]:
                dataset[attr_index][i] = int(round(dataset[attr_index][i]))  # rounding when needed
    morphed = map(list, zip(*dataset))  # recover to the original mode and finish.
    '''!!MORPH done!!'''

    # writing out and output the results
    for row_index in range(len(morphed)):
        morphed[row_index].append(classes[row_index])
    morphed.insert(0, attributes)

    if writeout:
        with open('MorphOut/'+database+'.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(morphed)

    return morphed


def testing():
    # loc = [100,200,100,300]
    # norm_loc, denorm_loc = attr_norm(loc)
    # l1 = map(norm_loc,loc)
    # l2 = map(denorm_loc, l1)
    # print l1
    # print l2
    MORPH("ant-1.7", writeout=True)
    pdb.set_trace()


if __name__ == "__main__":
    testing()
