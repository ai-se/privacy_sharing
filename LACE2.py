from __future__ import division
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


def data_distribute_simulator(data_set, number_of_holder):
    """
    This is a simulator. Distribute to the data to different members UNEQUALLY.
    :param data_set:
    :param number_of_holder:
    :return: list of list. each of list represent a data set holder by one person
    """
    data = copy.deepcopy(data_set)  # protect the original parameters
    n = len(data)

    assert n > number_of_holder, "not enough data to simulate!"

    part_size = [random.uniform(0, 1) for _ in xrange(number_of_holder)]
    s = sum(part_size)
    part_size = sorted(map(lambda x: int(n/s*x), part_size))
    # correction
    corr = n - sum(part_size)
    if corr > 0:
        for i in range(0, corr):
            part_size[i] += 1
    if corr < 0:
        for i in range(number_of_holder - corr, number_of_holder):
            part_size[i] -= 1

    random.shuffle(data)

    result = []
    cursor = 0
    for i in part_size:
        result.append(data[cursor: cursor+i])
        cursor += i

    random.shuffle(result)
    return result


def LACE2(model, original_data_folder, final_out_put_folder, holder_number,
          cliff_percent=0.3, morph_alpha=0.15, morph_beta=0.35):
    """

    :param model:
    :param original_data_folder:
    :param final_out_put_folder:
    :param holder_number:
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

    # get the **important** Leaf Distance
    fetch_num = min(len(all_data), 100)
    tmp_all_data_table = random.sample(all_data, fetch_num)
    tmp_all_data_table = csv_data_tools.normalize_cols_for_table([row[:-1] for row in tmp_all_data_table])
    inter_class_dist = find_distinct_distance(tmp_all_data_table)

    # normalize the dataset
    norm_funcs = []
    denorm_funcs = []

    all_data = map(list, zip(*all_data))
    for attr_index, attr_elements in enumerate(all_data[:-1]):
        f1, f2 = csv_data_tools.attr_norm(attr_elements)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
        all_data[attr_index] = map(f1, attr_elements)
    all_data = map(list, zip(*all_data))

    # simulate generate the holders
    holder_datas = data_distribute_simulator(all_data, holder_number)

    # passing the cache between the holders
    CACHE = []
    for holder_data in holder_datas:
        if len(CACHE) == 0:  # the first holder
            init_submit = Cliff_simplified(holder_data, cliff_percent)
            init_submit = MORPH(init_submit, alpha=morph_alpha, beta=morph_beta, db_has_normalized=True)
            CACHE.extend(init_submit)
            # TODO bug unbalance classe
            pdb.set_trace()
        else:  # something exist in the cache
            # TODO addd
            pass


    pdb.set_trace()


logging.basicConfig(level=logging.DEBUG, format="%(filename)s@L%(lineno)d:: %(message)s")
LACE2("xalan-2.7", 'TrainSet', 'final_folder', 5)
