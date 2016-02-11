import csv
import os
import sys
import pdb
sys.path.append(os.path.abspath(".."))


__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
experiment to answer the question: does the CLIFF+MORPHed dataset lead to a better/worse prediction
Measure: pf, pd, g-measure
pd(recall): TP/(TP+FN)
pf: FP/(FP+TN)
g-measure: 2*pd*(1-pf)/(pd+(1-pf))
"""


project_path = [p for p in sys.path if p.endswith('privacy_sharing')][0]+'/'
recorded_attrs = []
_original_recored_index = []


def _str2num(s):
    try:
        s = int(s)
    except ValueError:
        s = float(s)
    return s


def _get_original_recorded_index(model):
    # load the recorded attributes
    with open(project_path + 'MorphOut/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        global recorded_attrs
        recorded_attrs = next(reader)

    with open(project_path + 'TrainSet/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        original_attrs = next(reader)

    global _original_recored_index
    for attr in recorded_attrs:
        _original_recored_index.append(original_attrs.index(attr))


def _load_db(folder, model):
    if not _original_recored_index:
        _get_original_recorded_index(model)

    all_trains = []
    with open(project_path + folder + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pass the first line (csv header)
        for line in reader:
            record_row = [line[i] for i in _original_recored_index]
            record_row = map(_str2num, record_row)
            if record_row[-1] > 0:
                record_row[-1] = 1  # setting the result as binary
            all_trains.append(record_row)

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_original_train(model):
    return _load_db('TrainSet/', model)


def get_moprhed_train(model):
    return _load_db('MorphOut/', model)


def get_original_test(model):
    return _load_db('TestSet/', model)


def predict(model):
    from sklearn import svm
    x, y = get_original_train(model)
    clf = svm.SVC()
    clf.fit(x, y)
    x, actual = get_original_test(model)
    predict = clf.predict(x)
    pdb.set_trace()

if __name__ == '__main__':
    predict('ant-1.3')
