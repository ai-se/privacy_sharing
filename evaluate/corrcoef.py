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
from os import sys, path
from numpy import corrcoef, absolute
from pylab import pcolor, show, colorbar, xticks, yticks, savefig
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv



sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from tools import toolkit


def get_corrcoef(config, org_file=None, res_file=None):
    if not org_file:
        org_file = config.corrcoef['org']
    if not res_file:
        res_file = config.corrcoef['res']

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

    org_sel = list()
    res_sel = list()

    for attr_name, col1, col2 in zip(attributes, zip(*org_data), zip(*res_data)):
        if attr_name not in config.corrcoef['interest_attrs']:
            continue

        col1 = list(col1)
        col1 = map(toolkit.str2num, col1)
        col2 = list(col2)
        col2 = map(toolkit.str2num, col2)

        org_sel.append(col1)
        res_sel.append(col2)

    R1 = corrcoef(org_sel)
    R1 = absolute(R1)

    R2 = corrcoef(res_sel)
    R2 = absolute(R2)

    def draw(data, name):
        plt.clf()
        tick = [i+0.5 for i in range(len(config.corrcoef['interest_attrs']))]
        labels = config.corrcoef['interest_attrs']
        xticks(tick, labels, rotation=60, fontsize=9)
        yticks(tick, labels, fontsize=9)
        pcolor(data)
        cbar = colorbar()
        cbar.ax.tick_params(labelsize=9)
        plt.tight_layout()
        savefig(name)

    draw(R1, 'org.eps')
    draw(R2, 'processed.eps')

    print('\n\n\nFigures drew. Check the files under current working directory.')


def demo():
    from configs import parkinson_config
    get_corrcoef(parkinson_config)


if __name__ == '__main__':
    demo()
