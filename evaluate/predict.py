from __future__ import division

import csv
import time
from collections import OrderedDict

from sklearn import svm, tree
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, classification_report
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from tmp import settings

from tools import toolkit

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.2"
__email__ = "jchen37@ncsu.edu"

"""
experiment to answer the question: does the CLIFF+MORPHed dataset lead to a better/worse prediction
Main function: predict_models
"""


project_path = settings.project_path


def get_original_train(model):
    ori_attrs, all_trains = toolkit.load_csv('TrainSet', model)
    all_trains = map(lambda r:map(toolkit.str2num, r), all_trains)  # change the numbers if possible

    trainsT = map(list, zip(*all_trains))
    tmp_trainsT = list()
    for oa, col in zip(ori_attrs, trainsT):
        if oa in settings.record_attrs:
            tmp_trainsT.append(col)
    tmp_trainsT.append(trainsT[-1])

    all_trains = map(list, zip(*tmp_trainsT))

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_moprhed_train(source_folder, model):
    # type: (str, str) -> list, list
    _, all_trains = toolkit.load_csv(source_folder, model)
    all_trains = map(lambda r:map(toolkit.str2num, r), all_trains)  # change the numbers if possible

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_test(model):
    ori_attrs, all_trains = toolkit.load_csv('TestSet', model)
    all_trains = map(lambda r: map(toolkit.str2num, r), all_trains)  # change the numbers if possible

    trainsT = map(list, zip(*all_trains))
    tmp_trainsT = list()
    for oa, col in zip(ori_attrs, trainsT):
        if oa in settings.record_attrs:
            tmp_trainsT.append(col)
    tmp_trainsT.append(trainsT[-1])

    all_trains = map(list, zip(*tmp_trainsT))

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_error_measure(actual, predict):
    # type: (list, list) -> list
    actual = toolkit.make_it_list(actual)
    predict = toolkit.make_it_list(predict)

    assert len(actual) == len(predict), "length of the actual list and predict list must be the same"

    err = OrderedDict()

    if settings.predict_mode is 'CLASSIFICATION_BIN':
        TP = sum([1 for a, p in zip(actual, predict) if a == 1 and p == 1])
        FP = sum([1 for a, p in zip(actual, predict) if a == 0 and p == 1])
        FN = sum([1 for a, p in zip(actual, predict) if a == 1 and p == 0])
        TN = sum([1 for a, p in zip(actual, predict) if a == 0 and p == 0])

        pd = round(TP / (TP+FN), 2)
        pf = round(FP / (FP+TN), 2)
        g_measure = 2 * pd * (1 - pf) / (pd + (1 - pf))
        g_measure = round(g_measure, 2)

        err['pd'] = pd
        err['pf'] = pf
        err['g_measure'] = g_measure

    if settings.predict_mode is 'CLASSIFICATION_MUL':
        target_names = list(sorted(set(actual)))
        assert True, 'Please check here. under construction...'
        return classification_report(actual, predict, target_names)

    if settings.predict_mode is 'REGRESSION':
        err['RMSE'] = mean_squared_error(actual, predict) ** 0.5
        err['MAE'] = mean_absolute_error(actual, predict)

    return err


def predicting(x, y, model, clf_instance):
    clf_instance.fit(x, y)
    test_x, actual = get_test(model)
    predict = clf_instance.predict(test_x).tolist()
    return get_error_measure(actual, predict)


def predict_models(models, we_report_folder):
    """
    Func: given the models list, return the prediction precision.
    Learners: SVM, CART, Naive Bayes
    Require: TrainSet, TestSet, privatized_set_folder
    :param models:
    :param we_report_folder: from which folders material to predict
    :return: no explicit returns. depending on whether to show or write the results...
    """

    models = toolkit.make_it_list(models)
    we_report_folder = toolkit.make_it_list(we_report_folder)

    privatized_set_folder = we_report_folder[0]

    clfs = list()

    if settings.predict_mode is 'CLASSIFICATION_BIN':
        print("Predicting at the classification mode (binary)")
        svm_clf = svm.SVC()
        cart_clf = tree.DecisionTreeClassifier()
        nb_clf = GaussianNB()
        clfs = [('svm', svm_clf), ('cart', cart_clf), 'naive bayes', nb_clf]

    if settings.predict_mode is 'CLASSIFICATION_MUL':
        print("Predicting at the classification mode (multiple)")
        svm_clf = OneVsRestClassifier(svm.SVC(kernel='linear'))
        cart_clf = tree.DecisionTreeClassifier()
        nb_clf = OneVsRestClassifier(GaussianNB())
        clfs = [('svm', svm_clf), ('cart', cart_clf), 'naive bayes', nb_clf]

    if settings.predict_mode is 'REGRESSION':
        print("Predicting at the regression mode.")

        lg = LinearRegression()
        dt_clf = tree.DecisionTreeRegressor()
        # TODO the neual network??!
        clfs = [('linear regression', lg), ('decision tree', dt_clf)]

    report_at = csv.writer(open('Reports/PREDICTION_report.csv', 'a'))
    date = time.strftime('%m%d%y')

    for model in models:
        # get the prediction at original dataset
        x, y = get_original_train(model)
        for clf_name, clf in clfs:
            err = predicting(x, y, model, clf)
            for k, v in err.items(): report_at.writerow([date, time.time(), model, 'NoHandle', clf_name, k, "%.4f"%v])

        # get the refined dataset
        for re in we_report_folder:
            x, y = get_moprhed_train(re, model)
            for clf_name, clf in clfs:
                err = predicting(x, y, model, clf)
                for k, v in err.items(): report_at.writerow([date, time.time(), model, re, clf_name, k, "%.4f"%v])

if __name__ == '__main__':
    predict_models(['ant-1.7', 'camel-1.6'], we_report_folder=['Lace1Out', 'Lace2Out'])

