#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.


from __future__ import division
import csv
import logging
from bisect import bisect_left
from os import sys, path
from scipy.spatial.distance import cosine
import pdb

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from evaluate.Apriori.apriori import *
from tools import toolkit


"""
checking whether the two dataset has the same/similar frequent item set and association rules.
Using the APRIORI algorithm
"""


def dataset_iter(dataset):
    for data in dataset:
        yield frozenset(data)


def apriori_cmpr(org_file, res_file, config):
    """
    Note:
    ignore the class attribute. just focus on the independent attributes
    """
    # load the data sets
    org_data, res_data = list(), list()

    with open(org_file, 'r') as f:
        org_r = csv.reader(f)
        attributes = next(org_r)
        for row in org_r:
            org_data.append(row)

    with open(res_file, 'r') as f:
        res_r = csv.reader(f)
        next(res_r)
        for row in res_r:
            res_data.append(row)

    # discrete the data
    # translate the continuous attribute into 'attr+level'

    dis_org_data = []
    dis_ptz_data = []

    for attr_name, col1, col2 in zip(attributes, zip(*org_data), zip(*res_data)):
        if attr_name not in config.apriori['interest_attrs']:
            continue

        col1 = list(col1)
        col1 = map(toolkit.str2num, col1)
        col2 = list(col2)
        col2 = map(toolkit.str2num, col2)

        col = col1 + col2  # NOTE: put two dataset together

        ranges = toolkit.binrange(col)

        tags = []
        for element in col1:
            cursor = bisect_left(ranges, element)
            tags.append(attr_name + ':' + str(cursor))
        dis_org_data.append(tags)

        tags = []
        for element in col2:
            cursor = bisect_left(ranges, element)
            tags.append(attr_name + ':' + str(cursor))
        dis_ptz_data.append(tags)

    dis_org_data = map(list, zip(*dis_org_data))
    dis_ptz_data = map(list, zip(*dis_ptz_data))

    logging.info("Database discretization done.")

    org_iter = dataset_iter(dis_org_data)
    ptz_iter = dataset_iter(dis_ptz_data)

    items_org, rules_org = runApriori(org_iter, config.apriori['min_support'], config.apriori['min_confidence'])
    items_ptz, rules_ptz = runApriori(ptz_iter, config.apriori['min_support'], config.apriori['min_confidence'])

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

    value_vector1 = []
    value_vector2 = []
    for key in attr1.keys():
        value_vector1.append(attr1[key])
        value_vector2.append(attr2[key])

    return 1 - cosine(value_vector1, value_vector2)  # TODO divide by zero error


def association_rule_test(config, org_file=None, res_file=None):
    if not org_file:
        org_file = config.apriori['org']
    if not res_file:
        res_file = config.apriori['res']

    items_org, items_ptz, rules_org, rules_ptz, dis_org_data, dis_ptz_data = \
        apriori_cmpr(org_file, res_file, config)

    ruleId = lambda r: hash(r[0][0][0]+'0'+r[0][1][0])

    rules_org_id = set(map(ruleId, rules_org))
    rules_ptz_id = set(map(ruleId, rules_ptz))

    lap = rules_org_id & rules_ptz_id

    if len(lap) == 0:
        pr = rr = 0  # the preserve and reveal rate
    else:
        pr = len(lap) / len(rules_org)
        rr = len(lap) / len(rules_ptz)

    # print(len(items_org), len(items_ptz), len(rules_org), len(rules_ptz), round(pr, 3), round(rr, 3))
    return len(rules_org), len(rules_ptz), len(lap)


def demo():
    import configs.parkinson_config as config
    association_rule_test(config,
                          '/Users/jianfeng/git/super_lace/Dataset/parkinsons.csv',
                          '/Users/jianfeng/git/super_lace/.laceout/med0115.csv'
                          )


if __name__ == '__main__':
    demo()
