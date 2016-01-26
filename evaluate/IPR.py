import csv, copy
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"


"""
IPR is the increase privacy ratio. It is based on the adversarial accuracy gain.
quantifies an attacker's ability to predict the sensitive attribute value of a target t.
Higher IPR indicates higher privacy-preserving (the better).
Reference:
[1] Brickell, Justin, and Vitaly Shmatikov.
"The cost of privacy: destruction of data-mining utility in anonymized data publishing."
Proceedings of the 14th ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2008.

[2] Peters, Fayola, et al. "Balancing privacy and utility in cross-company defect prediction."
Software Engineering, IEEE Transactions on 39.8 (2013): 1054-1068.
"""


class Query(object):
    def __init__(self):
        self.__attrs = []
        self.__upper_bound = []
        self.__lower_bound = []

    def add_attr(self, attribute, upper_bound, lower_bound):
        self.__attrs.append(attribute)
        self.__upper_bound.append(upper_bound)
        self.__lower_bound.append(lower_bound)

    def __getitem__(self, attr):
        i = self.__attrs.index(attr)
        return self.__lower_bound[i], self.__upper_bound[i]


class IPR(object):
    def __init__(self, before_db, after_db):
        self.before_db = before_db
        self.after_db = after_db

        # load the before database
        with open(before_db, 'r') as f:
            reader = csv.reader(f)
            self.before_attrs = next(reader)
            self.before_all_data = []
            for line in reader:
                self.before_all_data.append(line)

        # load the after database
        with open(after_db, 'r') as f:
            reader = csv.reader(f)
            self.after_attrs = next(reader)
            self.after_all_data = []
            for line in reader:
                self.after_all_data.append(line)

    def query_generator(self, query_size=3):

        query = []
        return query


def testing():
    ipr = IPR('../Dataset/ant-1.3.csv', '../MorphOut/ant-1.3_0.2.csv')
    pdb.set_trace()


if __name__ == "__main__":
    testing()
