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
from toolkit import binrange
import pdb
import toolkit
import settings
import random
import sys

sys.dont_write_btyecode = True

attrs = ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'CDR3']


head, content = toolkit.load_csv(settings.project_path+'DataSet/', 'school')
content = map(lambda r: map(toolkit.str2num, r), content)

random.shuffle(content)

train = content[:(int(len(content)*(1-settings.test_set_ratio)))]
test  = content[(int(len(content)*(1-settings.test_set_ratio))):]


def dis(classes):
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
    return classes


"""
create the training set1 and set2
"""
trainT = map(list, zip(*train))
raw = list()
for attr, col in zip(head, trainT):
    if attr not in attrs: continue
    raw.append(col)

raw = map(list, zip(*raw))

# discrete
dependent1 = trainT[head.index('C150_4')]
dependent2 = trainT[head.index('mn_earn_wne_p7')]

dependent1 = dis(dependent1)
dependent2 = dis(dependent2)

toolkit.write_csv(settings.project_path+'/db4school/diff_purpose/train', 'school_01',
                  [i + [j] for i, j in zip(raw, dependent1)],
                  attrs+['C150_4'])

toolkit.write_csv(settings.project_path+'/db4school/diff_purpose/train', 'school_02',
                  [i + [j] for i, j in zip(raw, dependent2)],
                  attrs+['mn_earn_wne_p7'])

print('Training set 1 and 2 created.')

"""
create the test set1 and set2
"""
testT = map(list, zip(*test))
raw = list()
for attr, col in zip(head, testT):
    if attr not in attrs: continue
    raw.append(col)

raw = map(list, zip(*raw))

# discrete
dependent1 = testT[head.index('C150_4')]
dependent2 = testT[head.index('mn_earn_wne_p7')]

dependent1 = dis(dependent1)
dependent2 = dis(dependent2)

toolkit.write_csv(settings.project_path+'/db4school/diff_purpose/test', 'school_01',
                  [i + [j] for i, j in zip(raw, dependent1)],
                  attrs+['C150_4'])

toolkit.write_csv(settings.project_path+'/db4school/diff_purpose/test', 'school_02',
                  [i + [j] for i, j in zip(raw, dependent2)],
                  attrs+['mn_earn_wne_p7'])

print('Test set 1 and 2 created.')

