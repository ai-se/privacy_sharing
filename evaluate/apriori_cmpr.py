from __future__ import division
import pdb
import logging
import csv
import datetime
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


def dataset_iter(dataset):
    for data in dataset:
        yield frozenset(data)


def apriori_cmpr(model, org_folder, privatized_folder, min_support=0.15, min_confidence=0.6):
    """
    Note:
    ignore the class attribute. just focus on the independent attributes
    :param model:
    :param org_folder:
    :param privatized_folder:
    :param min_support:
    :param min_confidence:
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
    attributes = [attr for attr in org_attrs if attr in privatized_attrs]  # intersection of two data set attributes
    del attributes[-1]  # do not consider the classification attributes

    tmp_del_i1, tmp_del_i2 = [], []

    for attr_i, attr in enumerate(org_attrs):
        if attr not in attributes:
            tmp_del_i1.append(attr_i)

    for attr_i, attr in enumerate(privatized_attrs):
        if attr not in attributes:
            tmp_del_i2.append(attr_i)

    all_org_data = data_tools.del_col_in_table(all_org_data, tmp_del_i1)
    all_privatized_data = data_tools.del_col_in_table(all_privatized_data, tmp_del_i2)

    # discretize the data
    # translate the continuous attribute into 'attr+level'

    dis_org_data = []
    # ranges_dict = dict()  # for backup

    for attr_name, col in zip(attributes, zip(*all_org_data)):
        col = list(col)
        bin_size = data_tools.self_determine_bin_size(col)
        ranges = data_tools.binrange(col, bin_size)
        # ranges_dict[attr_name] = ranges

        tags = []
        for element in col:
            for cursor, upper_bound in enumerate(ranges):
                if upper_bound >= element: break

            # lower_bound = ranges[max(cursor-1, 0)]
            # mid = (upper_bound + lower_bound) / 2
            # if type(mid) is float:
            #     mid = round(mid, 2)
            #
            # tags.append(attr_name+':' + str(mid))
            tags.append(attr_name + ':' + str(cursor))

        dis_org_data.append(tags)
    dis_org_data = map(list, zip(*dis_org_data))

    dis_privatized_data = []
    for attr_name, col in zip(attributes, zip(*all_privatized_data)):
        col = list(col)
        bin_size = data_tools.self_determine_bin_size(col)
        ranges = data_tools.binrange(col, bin_size)
        # ranges = ranges_dict[attr_name]

        tags = []
        for element in col:
            for cursor, upper_bound in enumerate(ranges):
                if upper_bound >= element:
                    break

            # lower_bound = ranges[max(cursor-1, 0)]
            # mid = (upper_bound + lower_bound) / 2
            # if type(mid) is float:
            #     mid = round(mid, 2)
            #
            # tags.append(attr_name+':' + str(mid))
            tags.append(attr_name + ':' + str(cursor))

        dis_privatized_data.append(tags)
    dis_privatized_data = map(list, zip(*dis_privatized_data))

    logging.info("Database discretization done.")

    # writing out the dis dataset
    # with open('tmp_org.csv', 'wb') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(dis_org_data)
    #
    # with open('tmp_pri.csv', 'wb') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(dis_privatized_data)

    org_iter = dataset_iter(dis_org_data)
    privatized_iter = dataset_iter(dis_privatized_data)

    items_org, rules_org = runApriori(org_iter, min_support, min_confidence)
    items_privatized, rules_privatized = runApriori(privatized_iter, min_support, min_confidence)

    return items_org, items_privatized, rules_org, rules_privatized


def apriori_report(model, org_folder, privatized_folder, min_support=0.15, min_confidence=0.6):
    items_org, items_privatized, rules_org, rules_privatized = \
        apriori_cmpr(model, org_folder, privatized_folder, min_support, min_confidence)

    out_file_name = project_path + '/Reports/association_report_' + \
        datetime.datetime.now().strftime('%y-%m-%d-%H') + '.txt'

    out_file = open(out_file_name, 'wb')

    # frequent item set similarity
    itemsets_org = [set(items[0]) for items in items_org]
    itemsets_privatized = [set(items[0]) for items in items_privatized]

    for i in itemsets_org:
        if i in itemsets_privatized:
            print i

    pdb.set_trace()
    # writing the report

    org_details = printResults(items_org, rules_org, print_result=False)
    out_file.write('\n------' + org_folder + '---' + model + '---\n')
    out_file.write(org_details)
    out_file.write('\n' + '*' * 20)

    privatize_details = printResults(items_privatized, rules_privatized, print_result=False)
    out_file.write('\n------' + privatized_folder + '---' + model + '---\n')
    out_file.write(privatize_details)
    out_file.write('\n' + '*' * 20)

    out_file.close()

    pdb.set_trace()


def test():
    apriori_report('ant-1.7', 'DataSet', 'Lace1Out', 0.3, 0.6)

if __name__ == '__main__':
    test()
