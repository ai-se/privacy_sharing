from __future__ import division
from CLIFF import *
from MORPH import *
from LeaF import *
import sys, traceback
import settings

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


"""
LACE2 means CLIFF + LeaF + MORPH
This file is the control flow of LACE2.
Given the dataset, return the result of LACE2.
"""


def data_distribute_simulator(data_set):
    """
    This is a simulator. Distribute to the data to different members UNEQUALLY.
    :param data_set:
    :return: list of list. each of list represent a data set holder by one person
    """
    data = copy.deepcopy(data_set)  # protect the original parameters
    n = len(data)

    number_of_holder = settings.Lace2_holder_number

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


def LACE2(model, original_data_folder, final_out_put_folder):
    """

    :param model:
    :param original_data_folder:
    :param final_out_put_folder:
    :return:
    """
    # load the database and handle them
    ori_attrs, alldata = toolkit.load_csv(original_data_folder, model)

    tmp_all_data = list()

    record_attrs = settings.record_attrs
    for attr in record_attrs:
        col = zip(*alldata)[ori_attrs.index(attr)]
        tmp_all_data.append(col)
    tmp_all_data.append(zip(*alldata)[-1])

    alldata = copy.deepcopy(map(list, zip(*tmp_all_data)))
    for i in range(len(alldata)):
        alldata[i] = map(toolkit.str2num, alldata[i])

    logging.debug("loading the whole database and col selection done.")

    # get the **important** Leaf Distance
    fetch_num = min(len(alldata), 100)
    tmp_all_data_table = random.sample(alldata, fetch_num)
    tmp_all_data_table = toolkit.normalize_cols_for_table([row[:-1] for row in tmp_all_data_table])
    inter_class_dist = find_distinct_distance(tmp_all_data_table)

    # normalize the dataset
    norm_funcs = []
    denorm_funcs = []

    alldataT = map(list, zip(*alldata))  # transpose mode
    is_int = [True]*len(record_attrs)  # save. for better representation of the output table

    for attr_index, col in enumerate(alldataT[:-1]):
        # save is_int. for better representation of the output table
        for i in col:
            if type(i) is not int:
                is_int[attr_index] = False
                break

        f1, f2 = toolkit.attr_norm(col)
        norm_funcs.append(f1)
        denorm_funcs.append(f2)
        alldataT[attr_index] = map(f1, col)
    alldata = map(list, zip(*alldataT))

    # simulate generate the holders
    holder_datas = data_distribute_simulator(alldata)

    # passing the cache between the holders
    CACHE = []
    for holder_data in holder_datas:
        if len(CACHE) == 0:  # the first holder
            init_submit = cliff_core(holder_data)
            init_submit = MORPH(init_submit, db_has_normalized=True)
            CACHE.extend(init_submit)
        else:  # something exist in the cache
            to_submits = cliff_core(holder_data)
            # print(len(to_submits))
            cache_cursor = len(CACHE)
            # do the Leaf
            for to_submit in to_submits:
                if whether_add_to_private_cache(to_submit, CACHE, inter_class_dist):
                    CACHE.append(to_submit)
        print(len(CACHE))

    # morph
    CACHE = MORPH(CACHE, db_has_normalized=True, effect_scope=[cache_cursor, -1])

    # TODO checking the holder privacy criterion met?
    # denormalize the result
    CACHE = map(list, zip(*CACHE))
    for attr_index, col in enumerate(CACHE[:-1]):
        CACHE[attr_index] = map(denorm_funcs[attr_index], col)
        if is_int[attr_index]:
            CACHE[attr_index] = map(int, CACHE[attr_index])
    CACHE = map(list, zip(*CACHE))
    pdb.set_trace()
    CACHE.insert(0, record_attrs)
    if final_out_put_folder:
        with open(final_out_put_folder+'/'+model+'.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(CACHE)

    return CACHE


def test():
    LACE2("school", 'TrainSet', 'Lace2Out')

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, format='Line %(lineno)d at %(filename)s:\t %(message)s')
        test()
    except:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        # pdb.post_mortem(tb)
