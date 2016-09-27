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
import pdb
import settings
import toolkit
import matplotlib.pylab as plt
import sys


sys.dont_write_btyecode = True

head, content = toolkit.load_csv(settings.project_path+'db4school/diff_purpose', 'diff_purpose_precision')
content = map(lambda r: map(toolkit.str2num, r), content)

C2E = lambda x: x[3] == 'school_01' and x[4] == 'school_02'
C2C = lambda x: x[3] == 'school_01' and x[4] == 'school_01'
E2C = lambda x: x[3] == 'school_02' and x[4] == 'school_01'
E2E = lambda x: x[3] == 'school_02' and x[4] == 'school_02'

# regression
v = list()
for handler in ['org', 'lace1', 'lace2']:
    selected = filter(lambda x: x[2]==handler and x[5]=='linear regression', content)
    for scenario in [C2C, E2E, C2E, E2C]:
        selc = filter(scenario, selected)
        v.append(zip(*selc)[-1])

plt.clf()

fig = plt.figure(1)
fig.set_size_inches(6, 5)
ax = fig.add_subplot(111)
box = ax.boxplot(v)

ax.set_ylim(0, 4)
ax.set_title('Linear regression. RMSE. 20 repeats')
ax.axvspan(4.5, 8.5, alpha=0.3, color='gray')

ax.text(1, 3, 'No privatization', fontsize=10)
ax.text(5, 3, 'LACE1', fontsize=10)
ax.text(9, 3, 'LACE2', fontsize=10)
ax.text(6, 1, 'C=C150_4\nE=earnings\nCE=applied C-targeted model to predict E', fontsize=7)
plt.xticks(range(1,13), ['CC', 'EE', 'CE',' EC']*3)
fig.savefig('lr.png', bbox_inchees='tight')

# decision tree
v = list()
for handler in ['org', 'lace1', 'lace2']:
    selected = filter(lambda x: x[2]==handler and x[5]=='decision tree', content)
    for scenario in [C2C, E2E, C2E, E2C]:
        selc = filter(scenario, selected)
        v.append(zip(*selc)[-1])

plt.clf()

fig = plt.figure(1)
fig.set_size_inches(6, 5)
ax = fig.add_subplot(111)
box = ax.boxplot(v)

ax.set_ylim(0, 4)
ax.set_title('Decision tree. RMSE. 20 repeats')
ax.axvspan(4.5, 8.5, alpha=0.3, color='gray')

ax.text(1, 3, 'No privatization', fontsize=10)
ax.text(5, 3, 'LACE1', fontsize=10)
ax.text(9, 3, 'LACE2', fontsize=10)
ax.text(6, 1, 'C=C150_4\nE=earnings\nCE=applied C-targeted model to predict E', fontsize=7)
plt.xticks(range(1,13), ['CC', 'EE', 'CE', 'EC']*3)
fig.savefig('dt.png', bbox_inchees='tight')
