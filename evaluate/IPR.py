import csv
import random
import pdb
import sys
sys.path.append("..")
import CLIFF

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
        """
        attribute: (lower_bound,uppe_bound]
        """
        self.__attrs.append(attribute)
        self.__upper_bound.append(upper_bound)
        self.__lower_bound.append(lower_bound)

    def __getitem__(self, attr):
        i = self.__attrs.index(attr)
        return self.__lower_bound[i], self.__upper_bound[i]

    def __eq__(self, other):
        for other_attr in other.__attrs:
            if other_attr not in self.__attrs:
                return False
            else:
                a, b = self[other_attr]
                c, d = other[other_attr]
                if a != c or b != d:
                    return False
        return True

class IPR(object):
    def __init__(self, before_db, after_db):
        self.before_db = before_db
        self.after_db = after_db
        self.__sensitive_attrs = []

        # load the before database
        with open(before_db, 'r') as f:
            reader = csv.reader(f)
            self.before_attrs = next(reader)
            self.before_all_data = []
            for line in reader:
                self.before_all_data.append(line)
            self.before_all_data = [map(IPR._str2num, row) for row in self.before_all_data]  # str to numeric

        # load the after database
        with open(after_db, 'r') as f:
            reader = csv.reader(f)
            self.after_attrs = next(reader)
            self.after_all_data = []
            for line in reader:
                self.after_all_data.append(line)
            self.after_all_data = [map(IPR._str2num, row) for row in self.after_all_data]  # str to numeric

        # discrete the attributes...
        # determine the bin_sizes
        bin_sizes = dict()
        for attr in self.after_attrs[:-1]:
            temp = self.before_attrs.index(attr)
            col = [original_data_row[temp] for original_data_row in self.before_all_data]
            bin_sizes[attr] = CLIFF.self_determine_bin_size(col)

        # determine the bin_ranges
        self.bin_ranges = dict()
        for attr in self.after_attrs[:-1]:
            temp = self.before_attrs.index(attr)
            col = [original_data_row[temp] for original_data_row in self.before_all_data]
            self.bin_ranges[attr] = CLIFF.binrange(col, bin_sizes[attr])


    @staticmethod
    def _str2num(s):
        try:
            s = int(s)
        except ValueError:
            try:
                s = float(s)
            except ValueError:
                pass
        return s

    def set_sensitive_attributes(self, sensitive_attribute_list):
        self.__sensitive_attrs = sensitive_attribute_list
        print self.__sensitive_attrs
        for i in self.__sensitive_attrs:
            assert i in self.after_attrs[:-1], "Attribute " + i + " does NOT exist in the database"

        if self.after_attrs[-1] not in self.__sensitive_attrs:  # the class must be sensitive attribute
            self.__sensitive_attrs.append(self.after_attrs[-1])

    def _query_generator(self, query_size=2):
        # select query_size non-sensitive attributes randomly
        query_attrs = []
        while len(query_attrs) < query_size:
            temp = random.choice(self.after_attrs)
            if temp not in self.__sensitive_attrs:
                query_attrs.append(temp)

        # select one row randomly
        sampled_row = random.choice(self.before_all_data)

        # create the query
        query = Query()
        for query_attr in query_attrs:
            value = sampled_row[self.before_attrs.index(query_attr)]
            binr = self.bin_ranges[query_attr]  # bin ranges for the binr
            for boundary in binr:
                upper_bound = boundary
                if upper_bound >= value: break
            if upper_bound != binr[0]:
                lower_bound = binr[binr.index(upper_bound)-1]
            else:
                lower_bound = upper_bound
            if lower_bound == binr[0]: lower_bound -= 0.1  # just to make sure that lower_bound is not included
            query.add_attr(query_attr, upper_bound, lower_bound)

        return query

    def get_queries(self, query_size=2, number_of_queries=1):
        queries = []
        while len(queries) < number_of_queries:
            new_query = self._query_generator(query_size)
            # detect whether existed in the current queries
            exist = False
            for existed_query in queries:
                if existed_query == new_query:
                    exist = True
            if not exist:
                queries.append(new_query)

        pdb.set_trace()
        return queries


def demo():
    ipr = IPR('../Dataset/ant-1.3.csv', '../MorphOut/ant-1.3_0.2.csv')
    ipr.set_sensitive_attributes(['loc', 'rfc', 'lcom', 'ca', 'ce', 'amc'])
    ipr.get_queries(number_of_queries=20)
    pdb.set_trace()


if __name__ == "__main__":
    demo()
