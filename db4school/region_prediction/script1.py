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
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as plt
import pdb
import settings
import toolkit


"""
study case schoolcard script 1::
cross region prediction statistics
DRAWING the db4school/precision_report.csv
DRAWING prediction_report.csv
"""

# module_1
def module1():
    header, content = toolkit.load_csv(settings.project_path+"/db4school", "region_prediction/precision_report_copy")

    content = map(lambda r: map(toolkit.str2num, r), content)

    source_db = lambda x: x[2]
    test_for = lambda x: x[4]

    cases = ['school0', 'school1', 'school2', 'school3']

    lg_rmse = lambda x: x[5]=='linear regression' and x[6]=='RMSE'
    # lg_mae = lambda x: x[5]=='linear regression' and x[6]=='MAE'
    dt_rmse = lambda x: x[5]=='decision tree' and x[6]=='RMSE'
    # dt_mae = lambda x: x[5]=='decision tree' and x[6]=='MAE'

    for case in cases:
        plt.clf()
        fig = plt.figure(1)
        fig.set_size_inches(7,5)
        match_cases = filter(lambda x: source_db(x) == case, content)
        lace1_cases = filter(lambda x: 'LACE1' in x, match_cases)
        lace2_cases = filter(lambda x: 'LACE2' in x, match_cases)
        v = list()

        for testat in cases:
            # lace1
            selected = filter(lambda x: test_for(x) == testat, lace1_cases)

            lg = filter(lg_rmse, selected)
            dt = filter(dt_rmse, selected)

            v.append(zip(*lg)[-1])
            v.append(zip(*dt)[-1])

            # lace2
            selected = filter(lambda x: test_for(x) == testat, lace2_cases)
            lg = filter(lg_rmse, selected)
            dt = filter(dt_rmse, selected)

            v.append(zip(*lg)[-1])
            v.append(zip(*dt)[-1])

        # transformed to fit the charts
        v = [v[0],v[4],v[8],v[12],
             v[1],v[5],v[9],v[13],
             v[2],v[6],v[10],v[14],
             v[3],v[7],v[11],v[15]]

        ax = fig.add_subplot(111)
        box = ax.boxplot(v)
        import numpy
        for i in v: print(numpy.median(i))
        print('~~~')
        ax.axvspan(0, 4.5, alpha=0.3, color='gray')
        ax.axvspan(8.5, 12.5, alpha=0.3, color='gray')

        ax.text(1, 60000, 'LACE1\nregression', fontsize=10)
        ax.text(5, 60000, 'LACE1\ndecision tree', fontsize=10)
        ax.text(9, 60000, 'LACE2\nregression', fontsize=10)
        ax.text(13, 60000, 'LACE2\ndecision tree', fontsize=10)

        plt.setp(box['boxes'][cases.index(case)], color='red')
        plt.setp(box['boxes'][cases.index(case)+4], color='red')
        plt.setp(box['boxes'][cases.index(case)+8], color='red')
        plt.setp(box['boxes'][cases.index(case)+12], color='red')
        # pdb.set_trace()
        plt.xticks(range(1, 17), ['NE', 'NW', 'S', 'W']*4)
        ax.set_ylim([0, 150000])
        ax.set_title('RMSE for prediction from region data.')
        fig.savefig(case+'.png', bbox_inches='tight')


def module2():
    print('this is the second module in this file.')
    head, content = toolkit.load_csv(settings.project_path+'/Reports', 'PREDICTION_report_copy')
    content = map(lambda r: map(toolkit.str2num, r), content)

    lg_rmse = lambda x: x[4]=='linear regression' and x[5]=='RMSE'
    dt_rmse = lambda x: x[4]=='decision tree' and x[5]=='RMSE'

    lace1 = lambda x: x[3]=='Lace1Out'
    lace2 = lambda x: x[3]=='Lace2Out'
    org   = lambda x: x[3]=='NoHandle'

    v = list()
    for clf in [lg_rmse, dt_rmse]:
        for alg in [org, lace1, lace2]:
            selected = filter(clf and alg, content)
            v.append(zip(*selected)[-1])

    plt.clf()
    fig = plt.figure(1)
    fig.set_size_inches(7, 5)
    ax = fig.add_subplot(111)
    box = ax.boxplot(v)

    plt.xticks(range(1, 7), ['org', 'lace1', 'lace2']*2)

    ax.axvspan(0, 3.5, alpha=0.3, color='gray')

    ax.text(1, 60000, 'Linear regression', fontsize=10)
    ax.text(4, 60000, 'Decision tree', fontsize=10)

    ax.set_ylim([0, 150000])
    ax.set_title('RMSE for predicting at the whole shoolcard set')
    fig.savefig('school.png', bbox_inches='tight')


print(settings.MORPH_alpha)

if __name__ == '__main__':
    module1()
    module2()

