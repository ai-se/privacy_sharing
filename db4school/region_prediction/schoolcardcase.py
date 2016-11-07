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
from LACE1 import LACE1
from LACE2 import LACE2
from sklearn.linear_model import LinearRegression
from sklearn import tree
from evaluate.predict import get_error_measure
import toolkit
import hashlib
import time
import settings
import csv
import random
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"

"""
The experiments for the schoolcard case studies
"""


REGIONS = [  # 0=NE, 1=NW, 2=S, 3=W
    ['CT', 'ME', 'MA', 'NH', 'RI', 'VT',
     'NJ', 'NY', 'PA'],  # NE
    ['IL', 'MI', 'OH', 'WI', 'IN',
     'KS', 'MN', 'NE', 'ND', 'SD', 'MO', 'IA'],  # MW
    ['DC', 'MD', 'DE', 'VA', 'WV', 'NC', 'SC', 'GA', 'FL', 'VI',
     'KY', 'TN', 'AL', 'MS',
     'AR', 'LA', 'OK', 'TX'],  # S
    ['MT', 'ID', 'WY', 'CO', 'NM', 'UT', 'AZ', 'NV',
     'WA', 'OR', 'CA', 'HI', 'AK'],   # W
]


def load_csv_within_region(folder, model, region):
    header, content = toolkit.load_csv(folder, model, has_header=True)
    assert 'STABBR' in header, 'please make sure region info in database'
    abbr_at = header.index('STABBR')

    content = [i for i in content if i[abbr_at] in REGIONS[region]]

    return header, content


def dolace1():
    dbs = ['school0', 'school1', 'school2', 'school3']
    for db in dbs:
        LACE1(db, 'db4school/train/', 'db4school/lace1')


def dolace2():
    dbs = ['school0', 'school1', 'school2', 'school3']
    for db in dbs:
        LACE2(db, 'db4school/train/', 'db4school/lace2')

# dolace1()
# dolace2()


def get_md5(folder, file_name):
    with open(settings.project_path+'/db4school/'+folder+'/'+file_name+ '.csv', 'r') as f:
        r = hashlib.md5(f.read()).hexdigest()
    return r


def data_set_split(model):
    """
    split the data as testing set and non-testing set (training set)
    NOTE: handing the dependent variable here.
    :param model: name of the model
    """
    # load the original data
    with open('db4school/raw/' + model + '.csv', 'r') as db:
        reader = csv.reader(db)
        head = next(reader)
        all_original_data = []
        for line in reader:
            all_original_data.append(line)

    # discrete the independent variable
    classes = [i[-1] for i in all_original_data]  # last column in the origin csv file
    classes = map(toolkit.str2num, classes)
    # if 0 in classes:
    #     # binary the classification
    #     classes = [int(bool(int(c))) for c in classes]
    # else:
    from toolkit import binrange
    slot = binrange(classes)
    tmp_c = list()
    for c in classes:
        cursor = 0
        for i in slot:
            if c > i:
                cursor += 1
            else:
                break
        tmp_c.append(cursor)
    classes = tmp_c

    for l, c in zip(all_original_data, classes):
        l[-1] = c
    # discrete done

    # split the data body
    random.shuffle(all_original_data)
    line = int(len(all_original_data) * (1 - settings.test_set_ratio))

    # write the train set
    with open('db4school/train/' + model + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([head])
        writer.writerows(all_original_data[0:line])

    # write the test set
    with open('db4school/test/' + model + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([head])
        writer.writerows(all_original_data[line:])


def get_predicting_data(trainfrom, testat):
    # pdb.set_trace()
    h, content = toolkit.load_csv('db4school', trainfrom, True)
    contentT = map(list, zip(*content))
    y_train = contentT[-1]
    content = list()
    for attr, col in zip(h, contentT):
        if attr in settings.record_attrs:
            content.append(col)
    x_train = map(list, zip(*content))

    h, content = toolkit.load_csv('db4school', testat, True)
    contentT = map(list, zip(*content))
    y_test = contentT[-1]
    content=list()
    for attr, col in zip(h, contentT):
        if attr in settings.record_attrs:
            content.append(col)
    x_test = map(list, zip(*content))

    x_test = map(lambda r:map(toolkit.str2num, r), x_test)
    x_train = map(lambda r:map(toolkit.str2num, r), x_train)
    y_test = map(toolkit.str2num, y_test)
    y_train = map(toolkit.str2num, y_train)

    return x_train, y_train, x_test, y_test

# data_set_split('school0')
# data_set_split('school1')
# data_set_split('school2')
# data_set_split('school3')


# MODULE1 -- cross predicting
lg_clf = LinearRegression()
dt_clf = tree.DecisionTreeRegressor()

for repeat in range(20):
    dolace1()
    dolace2()
    dbs = ['school0', 'school1', 'school2', 'school3']
    for db in dbs:
        for dbt in dbs:
            x_train, y_train, x_test, actual = get_predicting_data('lace1/'+db, 'test/'+dbt)
            # pdb.set_trace()
            lg_clf.fit(x_train, y_train)
            predict = lg_clf.predict(x_test).tolist()
            ee = get_error_measure(actual, predict)

            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE1',
                                    dbt,
                                    'linear regression',
                                    'RMSE',
                                    ee['RMSE'],
                                    ])
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE1',
                                    dbt,
                                    'linear regression',
                                    'MAE',
                                    ee['MAE'],
                                    ])

            x_train, y_train, x_test, actual = get_predicting_data('lace2/' + db, 'test/' + dbt)
            lg_clf.fit(x_train, y_train)
            predict = lg_clf.predict(x_test).tolist()
            ee = get_error_measure(actual, predict)
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE2',
                                    dbt,
                                    'linear regression',
                                    'MAE',
                                    ee['MAE'],
                                    ])
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE2',
                                    dbt,
                                    'linear regression',
                                    'RMSE',
                                    ee['RMSE'],
                                    ])

            x_train, y_train, x_test, actual = get_predicting_data('lace1/'+db, 'test/'+dbt)
            dt_clf.fit(x_train, y_train)
            predict = dt_clf.predict(x_test).tolist()
            ee = get_error_measure(actual, predict)
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE1',
                                    dbt,
                                    'decision tree',
                                    'RMSE',
                                    ee['RMSE'],
                                    ])
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE1',
                                    dbt,
                                    'decision tree',
                                    'MAE',
                                    ee['MAE'],
                                    ])

            x_train, y_train, x_test, actual = get_predicting_data('lace2/' + db, 'test/' + dbt)
            dt_clf.fit(x_train, y_train)
            predict = dt_clf.predict(x_test).tolist()
            ee = get_error_measure(actual, predict)
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE2',
                                    dbt,
                                    'decision tree',
                                    'MAE',
                                    ee['MAE'],
                                    ])
            toolkit.append_csv_row('db4school', 'precision_report',
                                   [time.strftime('%m%d%y'),
                                    time.time(),
                                    db,
                                    'LACE2',
                                    dbt,
                                    'decision tree',
                                    'RMSE',
                                    ee['RMSE'],
                                    ])

    print("Repeat %d done." % repeat)


