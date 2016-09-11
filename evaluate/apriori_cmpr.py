from __future__ import division
import pdb
import logging
import csv
import datetime
import itertools
from scipy.spatial.distance import cosine
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
project_path = [i for i in sys.path if i.endswith('privacy_sharing')][0]
from evaluate.Apriori.apriori import *
import data_tools

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"

"""
checking whether the two dataset has the same/similar frequent item set and association rules.
Using the APRIORI algorithm
"""


def dataset_iter(dataset):
    for data in dataset:
        yield frozenset(data)


def apriori_cmpr(model, org_folder, privatized_folder, min_support, min_confidence):
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
    dis_privatized_data = []
    # ranges_dict = dict()  # for backup

    for attr_name, col1, col2 in zip(attributes, zip(*all_org_data), zip(*all_privatized_data)):
        col1 = list(col1)
        col2 = list(col2)

        col = col1 + col2  # NOTE: put two dataset together
        ranges = data_tools.binrange(col)
        # ranges_dict[attr_name] = ranges

        tags = []
        for element in col1:
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
        dis_org_data.append(tags)

        tags = []
        for element in col2:
            for cursor, upper_bound in enumerate(ranges):
                if upper_bound >= element:
                    break
            tags.append(attr_name + ':' + str(cursor))
        dis_privatized_data.append(tags)

    dis_org_data = map(list, zip(*dis_org_data))
    dis_privatized_data = map(list, zip(*dis_privatized_data))

    # for attr_name, col in zip(attributes, zip(*all_privatized_data)):
    #     col = list(col)
    #     ranges = data_tools.binrange(col)
    #     # ranges = ranges_dict[attr_name]
    #
    #     tags = []
    #     for element in col:
    #         for cursor, upper_bound in enumerate(ranges):
    #             if upper_bound >= element:
    #                 break
    #
    #         # lower_bound = ranges[max(cursor-1, 0)]
    #         # mid = (upper_bound + lower_bound) / 2
    #         # if type(mid) is float:
    #         #     mid = round(mid, 2)
    #         #
    #         # tags.append(attr_name+':' + str(mid))
    #         tags.append(attr_name + ':' + str(cursor))
    #
    #     dis_privatized_data.append(tags)
    # dis_privatized_data = map(list, zip(*dis_privatized_data))
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

    return items_org, items_privatized, rules_org, rules_privatized, dis_org_data, dis_privatized_data


def item_set_similarity(item1, item2):
    """
    If two frequent item sets does not have the same attribute, return 0
    Otherwise, return the cosin distance of frequent item sets.
    :param item1: e.g. set(['ic:0', 'cbm:0', 'moa:0', 'noc:0'])
    :param item2:
    :return:
    """
    attr1 = dict()
    attr2 = dict()

    for item in item1:
        tmp = item.split(':')
        attr1[tmp[0]] = int(tmp[1])

    for item in item2:
        tmp = item.split(':')
        attr2[tmp[0]] = int(tmp[1])

    if set(attr1.keys()) != set(attr2.keys()):
        return "not same attributes"

    if attr1 == attr2:
        return 1

    # TODO need to normalize?!
    value_vector1 = []
    value_vector2 = []
    for key in attr1.keys():
        value_vector1.append(attr1[key])
        value_vector2.append(attr2[key])

    return 1 - cosine(value_vector1, value_vector2)  # TODO divide by zero error


def apriori_report(model, org_folder, privatized_folder, print_result=False,
                   conclusion_only=False, min_support=0.15, min_confidence=0.6):
    """

    :param model:
    :param org_folder:
    :param privatized_folder:
    :param print_result:
    :param conclusion_only:
    :param min_support:
    :param min_confidence:
    :return:
    """
    items_org, items_privatized, rules_org, rules_privatized, dis_org_data, dis_privatized_data = \
        apriori_cmpr(model, org_folder, privatized_folder, min_support, min_confidence)

    # EXPERIMENT
    status1 = []  # recording the status of rules from original dataset to the privatized dataset
    status2 = []  # recording the status of rules from privatized dataset to the original dataset
    for rule in rules_org:
        left = rule[0][0]
        right = rule[0][1]
        # confidence = float(rule[1])
        d = len([1 for i in dis_privatized_data if set(left) <= set(i)])
        if d < min_support:
            status1.append('min_support fail')
        else:
            conff = len([1 for i in dis_privatized_data if set(left+right) <= set(i)]) / d
            if conff >= min_confidence:
                status1.append('rule remains')
            else:
                status1.append('rule disappear')

    for rule in rules_privatized:
        left = rule[0][0]
        right = rule[0][1]
        # confidence = float(rule[1])
        d = len([1 for i in dis_org_data if set(left) <= set(i)])
        if d < min_support:
            status2.append('min_support fail')
        else:
            conff = len([1 for i in dis_org_data if set(left+right) <= set(i)]) / d
            if conff >= min_confidence:
                status2.append('rule remains')
            else:
                status2.append('rule disappear')

    # END OF THE EXPERIMENT

    out_file_name = project_path + '/Reports/association_report_' + \
        datetime.datetime.now().strftime('%y-%m-%d-%H-%M') + '.txt'

    out_file = open(out_file_name, 'a+')

    # writing the report
    out_file.write('******%s********\n' % model)
    if not conclusion_only:
        org_details = printResults(items_org, rules_org, print_result=print_result)
        out_file.write('\n------' + org_folder + '---' + model + '---\n')
        out_file.write(org_details)
        out_file.write('\n' + '*' * 20)

        privatize_details = printResults(items_privatized, rules_privatized, print_result=print_result)
        out_file.write('\n------' + privatized_folder + '---' + model + '---\n')
        out_file.write(privatize_details)
        out_file.write('\n' + '*' * 20)

    # conclusion report
    if len(status1) == 0:
        out_file.write("rules in org #: 0\n")
    else:
        out_file.write('rules in org #: %d\n' % len(rules_org))
        out_file.write('org -> %s: 1 -> %f\n' % (privatized_folder, (status1.count('rule remains')/len(status1))))
    if len(status2) == 0:
        out_file.write("rules in %s #: 0 \n" % privatized_folder)
    else:
        out_file.write('rules in %s #: %d\n' % (privatized_folder, len(rules_privatized)))
        out_file.write('%s -> org: 1 ->% f\n' % (privatized_folder, (status2.count('rule remains')/len(status2))))
    out_file.close()

    # pdb.set_trace()


def test():
    apriori_report('camel-1.6', 'DataSet', 'Lace1Out', min_support=0.4, min_confidence=0.8)

if __name__ == '__main__':
    test()
