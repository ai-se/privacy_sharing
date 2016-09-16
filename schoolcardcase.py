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
import settings
import toolkit
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
#
# for i in range(4):
#     h, ct = load_csv_within_region('DataSet', 'school', i)
#     toolkit.write_csv('db4school', 'school%d'%i, ct, h)
#
#
