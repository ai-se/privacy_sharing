from __future__ import division
import pdb
import csv
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
project_path = [i for i in sys.path if i.endswith('privacy_sharing')][0]
from evaluate.Apriori.apriori import *
import data_tools

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
checking whether the two dataset has the same/similar frequent item set and association rules.
Using the APRIORI algorithm
"""


def apriori_cmpr(model, org_folder, privatized_folder):
    """
    Note:
    ignore the class attribute. just focus on the independent attributes
    :param model:
    :param org_folder:
    :param privatized_folder:
    :return:
    """
    # load the data sets
    with open(project_path+'/'+org_folder+'/'+model+'.csv', 'r') as f:
        reader = csv.reader(f)
        org_attrs = next(reader)
        all_org_data = []
        for line in reader:
            all_org_data.append(line)
        all_org_data = [map(data_tools.str2num, row) for row in all_org_data]  # str to numeric

    with open(project_path+'/'+privatized_folder+'/'+model+'.csv', 'r') as f:
        reader = csv.reader(f)
        privatized_attrs = next(reader)
        all_privatized_data = []
        for line in reader:
            all_privatized_data.append(line)
        all_privatized_data = [map(data_tools.str2num, row) for row in all_privatized_data]  # str to numeric

    # delete the useless columns
    tmp_del_i1, tmp_del_i2 = [-1], [-1]  # initially, ignore the class attribute

    for attr_i, attr in enumerate(org_attrs):
        if attr not in privatized_attrs:
            tmp_del_i1.append(attr_i)

    for attr_i, attr in enumerate(privatized_attrs):
        if attr not in org_attrs:
            tmp_del_i2.append(attr_i)

    for attr_i, attr in enumerate(org_attrs):
        if attr not in privatized_attrs:
            del org_attrs[attr_i]

    for attr_i, attr in enumerate(privatized_attrs):
        if attr not in org_attrs:
            del privatized_attrs[attr_i]

    all_org_data = data_tools.del_col_in_table(all_org_data, tmp_del_i1)
    all_privatized_data = data_tools.del_col_in_table(all_privatized_data, tmp_del_i2)

    # discretize the data
    for col in zip(*all_org_data):
        col = list(col)
        bin_size = data_tools.self_determine_bin_size(col)
        pdb.set_trace()


def test():
    apriori_cmpr('ant-1.7', 'DataSet', 'Lace1Out')
    pdb.set_trace()

if __name__ == '__main__':
    test()