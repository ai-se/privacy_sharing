from __future__ import division
import csv
import random
import sys
import os
sys.path.append(os.path.abspath(".."))
import CLIFF
import copy
import toolkit
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.0"
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

# TODO according the mail: only one sensitive attribute


class Query(object):
    def __init__(self):
        self.__attrs = []
        self.__upper_bound = []
        self.__lower_bound = []
        self.sampled = []

    def add_attr(self, attribute, upper_bound, lower_bound):
        """
        attribute: (lower_bound,upper_bound]
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

    def __repr__(self):
        res = ''
        for a in self.__attrs:
            res += a + ' [' + str(self[a]) + ']' + '\n'
        return res

    def get_attrs(self):
        return self.__attrs


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
            self.before_all_data = [map(toolkit.str2num, row) for row in self.before_all_data]  # str to numeric

        # load the after database
        with open(after_db, 'r') as f:
            reader = csv.reader(f)
            self.after_attrs = next(reader)
            self.after_all_data = []
            for line in reader:
                self.after_all_data.append(line)
            self.after_all_data = [map(toolkit.str2num, row) for row in self.after_all_data]  # str to numeric

        # discrete the attributes...
        # determine the bin_ranges
        self.bin_ranges = dict()
        for attr in self.after_attrs[:-1]:
            temp = self.before_attrs.index(attr)
            col = [original_data_row[temp] for original_data_row in self.before_all_data]
            self.bin_ranges[attr] = toolkit.binrange(col)

    def set_sensitive_attributes(self, sensitive_attribute_list):
        self.__sensitive_attrs = copy.deepcopy(sensitive_attribute_list)
        for i in self.__sensitive_attrs:
            assert i in self.after_attrs[:-1], "Attribute " + i + " does NOT exist in the database"

        if self.after_attrs[-1] not in self.__sensitive_attrs:  # the class must be sensitive attribute
            self.__sensitive_attrs.append(self.after_attrs[-1])

    def _query_generator(self, query_size=2):
        # select query_size non-sensitive attributes randomly
        query_attrs = []
        while len(query_attrs) < query_size:
            temp = random.choice(self.after_attrs)
            if temp not in self.__sensitive_attrs + query_attrs:
                query_attrs.append(temp)

        # select one row randomly
        sampled_row = random.choice(self.before_all_data)

        # create the query
        query = Query()
        query.sampled = sampled_row
        # pdb.set_trace()
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
            # pdb.set_trace()
            query.add_attr(query_attr, upper_bound, lower_bound)

        return query

    def get_queries(self, query_size=2, number_of_queries=1):
        queries = []
        while len(queries) < number_of_queries:
            new_query = self._query_generator(query_size)
            if new_query not in queries: queries.append(new_query)  # detect whether existed in the current queries
        return queries

    def _get_breach_from_query(self, query):
        """
        find the rows which match the query in original database and modified database
        TODO confirm from the LACE2's author
        :param query:
        :return: true if s_max(G) == s_max(G')
        """
        attrs = query.get_attrs()
        # query_target_index_before = [self.before_attrs.index(attr) for attr in attrs]
        query_target_index_after = [self.after_attrs.index(attr) for attr in attrs]

        # find the data that match the query in G and G'
        G_before = []
        for row in self.before_all_data:
            passed = True
            for attr in attrs:
                lower_bound, upper_bound = query[attr]
                target_before_i = self.before_attrs.index(attr)
                if not lower_bound < row[target_before_i] <= upper_bound:
                    passed = False
            if passed:
                G_before.append(row)

        G_after = []
        for row in self.after_all_data:
            passed = True
            for attr_index, attr in enumerate(attrs):
                lower_bound, upper_bound = query[attr]
                if not lower_bound < row[query_target_index_after[attr_index]] <= upper_bound:
                    passed = False
            if passed:
                G_after.append(row)

        # case -1: no matched data in original database
        assert len(G_before) > 0, "check the query_generator. No matched data in original database for this query!"

        # case 0: no matched data in the modified database
        if len(G_after) == 0:
            return False

        assert len(self.__sensitive_attrs) > 0, "Sensitive attributes need to be set up at " + self.before_db

        for sensitive_attr in self.__sensitive_attrs[:-1]:
            sen_before_index = self.before_attrs.index(sensitive_attr)
            sen_after_index = self.after_attrs.index(sensitive_attr)

            bin = self.bin_ranges[sensitive_attr]
            hist_before = [0] * (len(bin) - 1)
            hist_after = [0] * (len(bin) - 1)

            for row in G_before:
                tmp_cursor = 0
                if row[sen_before_index] != bin[0]:
                    while row[sen_before_index] < bin[tmp_cursor]:
                        tmp_cursor += 1
                    tmp_cursor -= 1
                hist_before[tmp_cursor] += 1

            for row in G_after:
                tmp_cursor = 0
                if row[sen_after_index] != bin[0]:
                    while row[sen_after_index] < bin[tmp_cursor]:
                        tmp_cursor += 1
                    tmp_cursor -= 1
                hist_after[tmp_cursor] += 1

            max_hist_before_index = hist_before.index(max(hist_before))
            max_hist_after_index = hist_after.index(max(hist_after))

            if max_hist_before_index != max_hist_after_index:
                return False

        return True

    def get_ipr(self, query_size=2, number_of_queries=1):
        queries = self.get_queries(query_size, number_of_queries)

        ipr = 0
        for query in queries:
            if self._get_breach_from_query(query):
                ipr += 1

        return int((1 - ipr / len(queries)) * 100)


def report_IPR(model, org_folder, privatized_folder, sensitive_attributes, query_size=4, number_of_queries=100):
    project_path = [p for p in sys.path if p.endswith('privacy_sharing')][0]+'/'

    ipr = IPR(project_path + org_folder + '/' + model + '.csv',
              project_path + privatized_folder + '/' + model + '.csv')

    ipr.set_sensitive_attributes(sensitive_attributes)
    result = ipr.get_ipr(query_size, number_of_queries)

    with open(project_path + 'Reports/IPR_report.csv', 'a+') as f:
        import datetime
        now = datetime.datetime.now()
        w = csv.writer(f, delimiter=',', lineterminator='\n')
        w.writerow([now.strftime('%y-%m-%d %H:%M'), model, sensitive_attributes, org_folder, privatized_folder, result])


def demo():
    sen_list = ['loc', 'amc', 'rfc']
    report_IPR('ant-1.7', 'DataSet', 'Lace1Out', sen_list)


if __name__ == "__main__":
    demo()
