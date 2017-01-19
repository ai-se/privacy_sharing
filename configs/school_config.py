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
import time

# ==============
# ATTENTION: THIS FILE MUST BE LOCATIONS IN THE ONE LEVEL SUB-FOLDER OF CURRENT PROJECT
# ==============
project_dir = os.path.dirname(os.path.abspath(__file__+'/..'))

NO_NEED_TO_LACE = True

# parameters
CLIFF_percentage = 0.5
Lace2_holder_number = 1
MORPH_alpha = 0.15
MORPH_beta = 0.35

ds_file = project_dir + '/Trainset/school.csv'
independent_attrs = [
                    'ADM_RATE',
                    'SAT_AVG',
                    'TUITFTE',
                    # 'RET_FT4',
                    'PCTFLOAN',
                    'PCTPELL',
                    'DEBT_MDN',
                    'C150_4',
                    'CDR3',
                    'mn_earn_wne_p7'
                    ]

objective_attr = 'RET_FT4'

writeto = project_dir + '/.laceout'
writeFileName = 'edu' + time.strftime("%m%d")

# research question configs
ipr = {
    'org': project_dir + '/Dataset/school.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'sen_attr': ['ADM_RATE', 'PCTFLOAN', 'C150_4'],
    'ipr_query_size': 2,
    'ipr_num_of_queries': 100,
}

apriori = {
    'org': project_dir + '/Trainset/school.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'interest_attrs': independent_attrs,
    'min_support': 0.1,
    'min_confidence': 0.1,
}

corrcoef = {
    'org': project_dir + '/Trainset/school.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'interest_attrs': independent_attrs,
}


predict = {
    'train_file': writeto + '/' + writeFileName + '.csv',
    'test_file': project_dir + '/Testset/school.csv',
    'predict_obj': independent_attrs
}
