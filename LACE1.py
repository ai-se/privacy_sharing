from CLIFF import *
from MORPH import *

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE1 means CLIFF + MORPH
This file is the control flow of LACE1.
Given the dataset, return the result of LACE1.
"""


def LACE1(model, original_data_folder, final_out_put_folder, cliff_percent, morph_alpha, morph_beta, record_attr):
    """

    :param model:
    :param original_data_folder:
    :param final_out_put_folder:
    :param cliff_percent:
    :param morph_alpha:
    :param morph_beta:
    :param record_attr:
    :return:
    """
    CLIFF(model,
          original_data_folder,
          cliff_percent,
          write_out_folder='CliffOut',
          record_attrs=record_attr)  # run CLIFF algorithm
    MORPH(model, 'CliffOut', final_out_put_folder, morph_alpha, morph_beta)  # run morph algorithm
