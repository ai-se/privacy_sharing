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

# parameters
CLIFF_percentage = 0.3
Lace2_holder_number = 5
MORPH_alpha = 0.15
MORPH_beta = 0.35

ds_file = project_dir + '/Trainset/parkinsons.csv'
independent_attrs = ['age',
                     'Jitter(%)', 'Jitter(Abs)', 'Jitter:RAP', 'Jitter:PPQ5', 'Jitter:DDP',
                     'Shimmer', 'Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5', 'Shimmer:APQ11', 'Shimmer:DDA',
                     'NHR', 'HNR',
                     'RPDE', 'DFA', 'PPE']

objective_attr = 'motor_UPDRS'

writeto = project_dir + '/.laceout'
writeFileName = 'med' + time.strftime("%m%d")

# research question configs
ipr = {
    'org': project_dir + '/Dataset/parkinsons.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'sen_attr': ['age', 'Jitter:RAP'],
    'ipr_query_size': 2,
    'ipr_num_of_queries': 100,
}

apriori = {
    'org': project_dir + '/Trainset/parkinsons.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'interest_attrs': independent_attrs,
    'min_support': 0.3,
    'min_confidence': 0.5,
}

corrcoef = {
    'org': project_dir + '/Trainset/parkinsons.csv',
    'res': writeto + '/' + writeFileName + '.csv',
    'interest_attrs': independent_attrs,
}


predict = {
    # 'train_file': writeto + '/' + writeFileName + '.csv',
    'train_file': project_dir + '/Trainset/parkinsons.csv',
    'test_file': project_dir + '/Testset/parkinsons.csv',
    'predict_obj': objective_attr,

}

