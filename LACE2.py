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
    # load the database and handle them
    with open(original_data_folder+'/'+model+'.csv', 'r') as db:
        reader = csv.reader(db)
        original_attributes = next(reader)
        all_data = []
        for line in reader:
            line = map(csv_data_tools.str2num, line)
            all_data.append(line)

    # TODO user-given record attributes
    record_attrs = []
    tmp_all_data = []
    for attr_index, attr in enumerate(original_attributes):
        if type(all_data[0][attr_index]) is str:
            continue
        col = zip(*all_data)[attr_index]
        if len(set(col)) > 1:
            record_attrs.append(attr)
            tmp_all_data.append(col)

    original_attributes = record_attrs
    tmp_all_data = map(list, zip(*tmp_all_data))
    all_data = copy.deepcopy(tmp_all_data)
    logging.debug("loading the whole database and col selection done.")

    # get the important Leaf Distance
    fetch_num = min(len(all_data), 100)



LACE2('ant-1.3', 'TrainSet', 0,0,0,0)