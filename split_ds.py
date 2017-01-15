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
import os
import sys
import csv
import random
project_dir = os.path.dirname(sys.modules['__main__'].__file__)


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

if __name__ == '__main__':
    split(sys.argv[1], float(sys.argv[2]))
