# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # Copyright (C) 2016, Jianfeng Chen <jchen37@ncsu.edu>
# # vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# #  of this software and associated documentation files (the "Software"), to deal
# #  in the Software without restriction, including without limitation the rights
# #  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# #  copies of the Software, and to permit persons to whom the Software is
# #  furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in
# #  all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# #  THE SOFTWARE.
#
#
# from __future__ import division
# from matplotlib import colors
# import matplotlib.pyplot as plt
# import numpy as np
#
# """
# Summary issue https://github.com/ai-se/privacy_sharing/issues/13
# """
#
# region = ['NE', 'NW', 'S', 'W']
#
# Lace1_regression = [0, 0, 0, -1,
#                     -1, 0, 0, -2,
#                     -1, 0, 0, -1,
#                     1, 1, 1, 0]
#
# Lace1_decision_tree = [0, 0, 0, -1,
#                        0, 0, 0, -1,
#                        -1, 0, 0, -2,
#                        1, 1, 1, 0]
#
# Lace2_regression = [0, 1, 1, 0,
#                     0, 0, 0, -1,
#                     0, 0, 0, 1,
#                     1, 1, 1, 0]
#
# Lace2_decision_tree = [0, 0, 0, -1,
#                        -1, 0, 0, -2,
#                        -1, 0, 0, -2,
#                        1, 1, 1, 0]
#
# def map44(x):
#     return np.array([x[0:4], x[4:8], x[8:12], x[12:]])
#
#
# cmap = colors.ListedColormap(['red', 'pink', 'white', 'green', 'darkgreen'])
# bounds=[-2, -1, 0, 1, 2]
# norm = colors.BoundaryNorm(bounds, cmap.N)
# heatmap = plt.pcolor(map44(Lace1_regression), cmap=cmap, norm=norm)
#
# plt.colorbar(heatmap, ticks=[-2, -1, 0, 1, 2])
#
# plt.show()
