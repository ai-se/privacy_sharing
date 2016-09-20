from CLIFF import *
from MORPH import *
import settings

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE1 means CLIFF + MORPH
This file is the control flow of LACE1.
Given the dataset, return the result of LACE1.
"""


def LACE1(model, original_data_folder, lace1_out_put_folder):
    """

    :param model:
    :param original_data_folder:
    :param lace1_out_put_folder:
    :return:
    """
    CLIFF(model, original_data_folder, write_out_folder=settings.project_path+"CliffOut")
    MORPH(model, settings.project_path+'CliffOut', lace1_out_put_folder)  # run morph algorithm
