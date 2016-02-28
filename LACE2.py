from CLIFF import *
from MORPH import *
from LeaF import *

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE2 means CLIFF + LeaF + MORPH
This file is the control flow of LACE2.
Given the dataset, return the result of LACE2.
"""


def LACE2(model, original_data_folder, final_out_put_folder, cliff_percent, morph_alpha, morph_beta):
    """
    
    :param model:
    :param original_data_folder:
    :param final_out_put_folder:
    :param cliff_percent:
    :param morph_alpha:
    :param morph_beta:
    :return:
    """
    CLIFF(model, original_data_folder, cliff_percent, write_out_folder='CliffOut')  # run CLIFF algorithm
    MORPH(model, 'CliffOut', final_out_put_folder, morph_alpha, morph_beta)  # run morph algorithm
