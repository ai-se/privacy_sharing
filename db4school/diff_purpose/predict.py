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
from evaluate.predict import get_moprhed_train as get_pured_dataset
from sklearn.metrics import mean_squared_error
import settings
import csv
import time
import toolkit
import pdb
import sys

sys.dont_write_btyecode = True


def onerun():
    """
    predicting test.
    diff purpose
    """
    settings.record_attrs = ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'CDR3']

    LACE1('school_01', settings.project_path + 'db4school/diff_purpose/train',
          settings.project_path + 'db4school/diff_purpose/lace1out')

    LACE2('school_01', settings.project_path + 'db4school/diff_purpose/train',
          settings.project_path + 'db4school/diff_purpose/lace2out')

    LACE1('school_02', settings.project_path + 'db4school/diff_purpose/train',
          settings.project_path + 'db4school/diff_purpose/lace1out')

    LACE2('school_02', settings.project_path + 'db4school/diff_purpose/train',
          settings.project_path + 'db4school/diff_purpose/lace2out')

    lg = LinearRegression()
    dt = tree.DecisionTreeRegressor()

    org_source = settings.project_path + 'db4school/diff_purpose/train/', 'org'
    lace1_source = settings.project_path + 'db4school/diff_purpose/lace1out', 'lace1'
    lace2_source = settings.project_path + 'db4school/diff_purpose/lace2out', 'lace2'

    test_set = settings.project_path + 'db4school/diff_purpose/test'

    f = csv.writer(open(settings.project_path + 'db4school/diff_purpose/diff_purpose_precision.csv', 'a+'))

    for alg, alg_name in [org_source, lace1_source, lace2_source]:
        for src_dataset in ['school_01', 'school_02']:
            for test_dataset in ['school_01', 'school_02']:
                trainx, trainy = get_pured_dataset(alg, src_dataset)
                lg.fit(trainx, trainy)
                dt.fit(trainx, trainy)

                testx, actual = get_pured_dataset(test_set, test_dataset)

                predict = lg.predict(testx).tolist()
                err = mean_squared_error(actual, predict) ** 0.5
                f.writerow([
                    time.strftime('%m%d%y'),
                    time.time(),
                    alg_name,
                    src_dataset,
                    test_dataset,
                    'linear regression',
                    'RMSE',
                    err
                ])

                predict = dt.predict(testx).tolist()
                err = mean_squared_error(actual, predict) ** 0.5
                f.writerow([
                    time.strftime('%m%d%y'),
                    time.time(),
                    alg_name,
                    src_dataset,
                    test_dataset,
                    'decision tree',
                    'RMSE',
                    err
                ])


if __name__ == '__main__':
    for i in range(20):
        onerun()
        print('run %d done.' % i)
