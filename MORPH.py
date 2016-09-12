from __future__ import division
import copy
import csv
import random
import math
import pdb
import copy
import toolkit
import settings

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


"""
MORPH is an instance mutator that "shake" the data while maintain the data attributes. GOAL: the MORPHed data
    can be learned by other data-mining techniques as well as the original data.

Version 1.0--Reference: Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


def MORPH(database, db_folder='not_from_csv_file', write_out_folder=None,
          db_has_normalized=False, effect_scope=[0, -1]):
    """
    MORPH is a instance mutator which can shake the instance within the class boundary
    :param database: original data.
    :param db_folder: from where database fetch. by default, the database is a list of list
    :param write_out_folder: specify the  writing out folder. None means no writing
    :param db_has_normalized: whether the database has been normalized
    :param effect_scope: specify the scope in the database to be morphed. Any data beyond the scope will remain the same
    :return: the morphed data
    """
    alpha = settings.MORPH_alpha
    beta = settings.MORPH_beta

    # load the database
    if db_folder != 'not_from_csv_file':
        with open(db_folder + '/' + database + '.csv', 'r') as db:
            reader = csv.reader(db)
            attributes = next(reader)  # including the last one--class tag
            dataset = []
            for line in reader:
                dataset.append(line)
        dataset = [map(toolkit.str2num, row) for row in dataset]  # str to numeric
    else:
        dataset = database
        attributes = ['foo'] * len(dataset[0])

    # backup the no-need-to-morphed data
    if effect_scope[1] < 0:
        effect_scope[1] += len(dataset)+1
    backup_data_set = copy.deepcopy(dataset[effect_scope[0]:effect_scope[1]])

    if db_has_normalized:
        #  adding two instance (all zeros and all ones) so that the normalization and de-normalization process
        #  do not damage the original data
        dataset.append([0]*len(dataset[0]))
        dataset.append([1]*len(dataset[0]))

    is_int = [type(i) is int for i in dataset[0]]  # save. for better representation of the output table
    classes = [row[-1] for row in dataset]  # fetch the classes
    dataset = [row[:-1] for row in dataset]  # separating the raw data and class

    '''dataset transposed mode begins...'''
    dataset = map(list, zip(*dataset))  # transpose.
    norm_funcs = []
    denorm_funcs = []

    # normalizing

    for attr_index, attr_elements in enumerate(dataset):  # for each attribute elements
        f1, f2 = toolkit.attr_norm(attr_elements)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
        dataset[attr_index] = map(f1, attr_elements)

    '''dataset mode recover...'''
    dataset = map(list, zip(*dataset))  # transpose again.

    for row_index, row in enumerate(dataset):  # for each row
        heterogeneous_index = [i for i in range(len(classes)) if classes[i] != classes[row_index]]
        boundary_dist = min([toolkit.euclidean_dist(row, dataset[heg]) for heg in heterogeneous_index])
        boundary_dist /= math.sqrt(len(attributes)-1)
        for i in range(len(row)):
            dataset[row_index][i] += boundary_dist*random.uniform(alpha, beta)*random.choice([1, -1])  # shake

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
    if db_folder != 'not_from_csv_file':
        morphed.insert(0, attributes)

    if write_out_folder:
        with open(write_out_folder + '/'+database+'.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(morphed)

    if db_has_normalized:
        morphed = morphed[:-2]

    # recover the unmorphed data
    for backup, row_index in zip(backup_data_set, range(effect_scope[0], effect_scope[1])):
        morphed[row_index] = backup

    return morphed


def testing():
    MORPH("school", 'CliffOut', write_out_folder='Lace1Out')

if __name__ == "__main__":
    testing()
