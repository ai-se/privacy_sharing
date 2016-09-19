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
"""
Get the IPR box-plot for school card study case
"""

head, content = toolkit.load_csv(settings.project_path+'Reports', 'IPR_report')

content = map(lambda r: map(toolkit.str2num, r), content)

lace1 = lambda r: r[5]=='Lace1Out'
lace2 = lambda r: r[5]=='Lace2Out'

v1 = filter(lace1, content)
v2 = filter(lace2, content)

v1 = zip(*v1)[-1]
v2 = zip(*v2)[-1]

plt.clf()
fig = plt.figure(1)
fig.set_size_inches(7,5)
ax = fig.add_subplot(111)
box = ax.boxplot([v1,v2])

plt.xticks([1,2], ['LACE1', 'LACE2'])
ax.set_yticks(range(0, 101)[::10])

ax.set_title('IPR report, 20 repeats. Higher the better')
fig.savefig('ipr.png', bbox_inches='tight')

print('ipr.png wrote!')
