from __future__ import division
import toolkit
import logging
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
__email__ = "jchen37@ncsu.edu"


"""
LeaF is an online, incremental technique for clustering data. The clusters are the "leaders" and all other instances
are the "followers".

Reference 1: Duda, Richard O., Peter E. Hart, and David G. Stork. Pattern classification. John Wiley & Sons, 2012.
Reference 2: Peters, Fayola, Tim Menzies, and Lucas Layman. "LACE2: better privacy-preserving data sharing for
cross project defect prediction."
Proceedings of the 37th International Conference on Software Engineering-Volume 1. IEEE Press, 2015.
"""


def find_distinct_distance(normalized_data_set):
    """
    find the median of distance which can distinguish the data.
    :param normalized_data_set: dataset to calculate. The dataset must be normalized
    :return: float-distance
    """

    n = len(normalized_data_set)

    # find out all kinds of classes in the dataset
    classes = list(set([i[-1]for i in normalized_data_set]))
    assert len(classes) > 1, "unfortunately all data selected are in same class."
    classes_index = dict()
    for c in classes:
        classes_index[c] = [index for index, i in enumerate(normalized_data_set) if i[-1] == c]

    distances = []
    for data in normalized_data_set:
        c = data[-1]
        diff_class_data_indices = [index for index in range(n) if index not in classes_index[c]]
        distances.append(min([toolkit.euclidean_dist(data, normalized_data_set[index])
                              for index in diff_class_data_indices]))
    import numpy
    median_dist = numpy.median(numpy.array(distances))
    logging.debug("The distinguish distance is %f" % median_dist)
    return median_dist


def whether_add_to_private_cache(data_instance, existed_cache, distinguish_distance):
    """

    :param data_instance: this should be normalized
    :param existed_cache: this should be normalized
    :param distinguish_distance:
    :return:
    """
    # TODO whether need to check the class?!
    for data in existed_cache:
        if toolkit.euclidean_dist(data_instance, data) <= distinguish_distance:
            return False

    return True


if __name__ == '__main__':
    print('this is testing sentence.')
    logging.basicConfig(level=logging.DEBUG)
    # d = [[1,2,3,4,1], [1,3,4,5,0], [4,6,7,4,0], [21,2,2,1,1], [4,4,6,7,0], [1,2,6,9,2]]
    # print find_distinct_diff(d)

    pdb.set_trace()
