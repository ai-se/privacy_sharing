from __future__ import division

import csv
import logging
import time
from os import sys, path

from scipy.spatial.distance import cosine

import toolkit
from tmp import settings

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from evaluate.Apriori.apriori import *

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


def apriori_cmpr(model, org_folder, ptz_folder):
    """
    Note:
    ignore the class attribute. just focus on the independent attributes
    :param model:
    :param org_folder:
    :param ptz_folder:
    :return:
    """
    # load the data sets
    org_attrs, org_data = toolkit.load_csv(org_folder, model)
    org_data = map(lambda r: map(toolkit.str2num, r), org_data)

    ptz_attrs, ptz_data = toolkit.load_csv(ptz_folder, model)
    ptz_data = map(lambda r: map(toolkit.str2num, r), ptz_data)
    ptz_data = toolkit.del_col_in_table(ptz_data, -1)

    # delete the useless columns
    attributes = settings.record_attrs
    org_dataT = map(list, zip(*org_data))
    org_dataT = [col for col, a1 in zip(org_dataT, org_attrs) if a1 in attributes]
    org_data = map(list, zip(*org_dataT))

    # discretize the data
    # translate the continuous attribute into 'attr+level'

    dis_org_data = []
    dis_ptz_data = []
    # ranges_dict = dict()  # for backup

    for attr_name, col1, col2 in zip(attributes, zip(*org_data), zip(*ptz_data)):
        col1 = list(col1)
        col2 = list(col2)

        col = col1 + col2  # NOTE: put two dataset together
        ranges = toolkit.binrange(col)
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
        dis_ptz_data.append(tags)

    dis_org_data = map(list, zip(*dis_org_data))
    dis_ptz_data = map(list, zip(*dis_ptz_data))

    logging.info("Database discretization done.")

    org_iter = dataset_iter(dis_org_data)
    ptz_iter = dataset_iter(dis_ptz_data)

    items_org, rules_org = runApriori(org_iter, settings.apriori_min_support, settings.apriori_min_confidence)
    items_ptz, rules_ptz = runApriori(ptz_iter, settings.apriori_min_support, settings.apriori_min_confidence)

    return items_org, items_ptz, rules_org, rules_ptz, dis_org_data, dis_ptz_data


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


def apriori_report(model, org_folder, we_report_folder):
    """

    :param model:
    :param org_folder:
    :param we_report_folder:
    :return:
    """
    we_report_folder = toolkit.make_it_list(we_report_folder)

    for ptz_folder in we_report_folder:
        items_org, items_ptz, rules_org, rules_ptz, dis_org_data, dis_ptz_data = \
            apriori_cmpr(model, org_folder, ptz_folder)

        ruleId = lambda r: hash(r[0][0][0]+'0'+r[0][1][0])

        rules_org_id = set(map(ruleId, rules_org))
        rules_ptz_id = set(map(ruleId, rules_ptz))

        lap = rules_org_id&rules_ptz_id

        if len(lap) == 0:
            pr = rr = 0  # the preserve and reveal rate
        else:
            pr = len(lap) / len(rules_org)
            rr = len(lap) / len(rules_ptz)

        with open(settings.project_path+ '/Reports/APRIORI_report.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([time.strftime("%m%d%y"), time.time(), model, ptz_folder,
                             len(items_org),
                             len(items_ptz),
                             len(rules_org),
                             len(rules_ptz),
                             round(pr, 3),
                             round(rr, 3)])


def test():
    apriori_report('camel-1.6', 'DataSet', 'Lace1Out')


if __name__ == '__main__':
    test()
