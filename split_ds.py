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
import sys
import csv
import random
from configs.parkinson_config import project_dir


def split(name, test_ratio):
    f = open(project_dir + '/Dataset/' + name + '.csv', 'r')
    f_tr = open(project_dir + '/Trainset/' + name + '.csv', 'w')
    f_te = open(project_dir + '/Testset/' + name + '.csv', 'w')

    reader = csv.reader(f)
    writeTrain = csv.writer(f_tr)
    writeTest = csv.writer(f_te)

    h = next(reader)
    writeTrain.writerow(h)
    writeTest.writerow(h)

    for row in reader:
        if random.random() < test_ratio:
            writeTest.writerow(row)
        else:
            writeTrain.writerow(row)


def split5(name):
    f = open(project_dir + '/Trainset/' + name + '.csv', 'r')
    f_1 = open(project_dir + '/Trainset/' + name + '.1.csv', 'w')
    f_2 = open(project_dir + '/Trainset/' + name + '.2.csv', 'w')
    f_3 = open(project_dir + '/Trainset/' + name + '.3.csv', 'w')
    f_4 = open(project_dir + '/Trainset/' + name + '.4.csv', 'w')
    f_5 = open(project_dir + '/Trainset/' + name + '.5.csv', 'w')

    reader = csv.reader(f)
    writers = [csv.writer(f_1), csv.writer(f_2), csv.writer(f_3), csv.writer(f_4), csv.writer(f_5)]

    h = next(reader)
    for w in writers:
        w.writerow(h)
    n = [200, 400, 600, 800, 2000]
    from bisect import bisect_left
    for i, row in enumerate(reader):
        if random.random() > 0.3: continue
        x = bisect_left(n, i)
        writers[x].writerow(row)

if __name__ == '__main__':
    split(sys.argv[1], float(sys.argv[2]))
    # split5(sys.argv[1])
