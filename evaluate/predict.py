from __future__ import division
from collections import defaultdict
import csv
import csv_data_tools
import os
import sys
sys.path.append(os.path.abspath(".."))


__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
experiment to answer the question: does the CLIFF+MORPHed dataset lead to a better/worse prediction
Measure: pf, pd, g-measure
recall(pd): TP/(TP+FN)
pf: FP/(FP+TN)
g-measure: 2*pd*(1-pf)/(pd+(1-pf))

Learners used for testing: SVM, CART, NB (Naive Bayes)

Main function: predict_models
"""


project_path = [p for p in sys.path if p.endswith('privacy_sharing')][0]+'/'
recorded_attrs = []
_original_recored_index = []
privatized_set_folder = ''


def _get_original_recorded_index(model):
    # load the recorded attributes
    with open(project_path + privatized_set_folder + '/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        global recorded_attrs
        recorded_attrs = next(reader)

    with open(project_path + 'TrainSet/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        original_attrs = next(reader)

    global _original_recored_index
    for attr in recorded_attrs:
        _original_recored_index.append(original_attrs.index(attr))


def get_original_train(model):
    if not _original_recored_index:
        _get_original_recorded_index(model)

    all_trains = []
    with open(project_path + 'TrainSet/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pass the first line (csv header)
        for line in reader:
            record_row = [line[i] for i in _original_recored_index]
            record_row = map(csv_data_tools.str2num, record_row)
            if record_row[-1] > 0:
                record_row[-1] = 1  # setting the result as binary
            all_trains.append(record_row)

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_moprhed_train(model):
    all_trains = []
    with open(project_path + privatized_set_folder + '/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pass the first line (csv header)
        for line in reader:
            record_row = map(csv_data_tools.str2num, line)
            if record_row[-1] > 0:
                record_row[-1] = 1  # setting the result as binary
            all_trains.append(record_row)

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_test(model):
    if not _original_recored_index:
        _get_original_recorded_index(model)

    all_trains = []
    with open(project_path + 'TestSet/' + model + '.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pass the first line (csv header)
        for line in reader:
            record_row = [line[i] for i in _original_recored_index]
            record_row = map(csv_data_tools.str2num, record_row)
            if record_row[-1] > 0:
                record_row[-1] = 1  # setting the result as binary
            all_trains.append(record_row)

    x = [row[:-1] for row in all_trains]
    y = [row[-1] for row in all_trains]

    return x, y


def get_error_measure(actual, predict):
    """
    given the actual list and predict list, return the pd, pf and g-measure
    :param actual:
    :param predict:
    :return: pd, pf, g-measure
    """
    if not type(actual) is list:
        actual = [actual]

    if not type(predict) is list:
        predict = [predict]

    assert len(actual) == len(predict), "length of the actual list and predict list must be the same"

    TP = sum([1 for a, p in zip(actual, predict) if a == 1 and p == 1])
    FP = sum([1 for a, p in zip(actual, predict) if a == 0 and p == 1])
    FN = sum([1 for a, p in zip(actual, predict) if a == 1 and p == 0])
    TN = sum([1 for a, p in zip(actual, predict) if a == 0 and p == 0])

    pd = round(TP / (TP+FN), 2)
    pf = round(FP / (FP+TN), 2)
    g_measure = 2 * pd * (1 - pf) / (pd + (1 - pf))
    g_measure = round(g_measure, 2)

    error = dict()
    error['pd'] = pd
    error['pf'] = pf
    error['g_measure'] = g_measure
    return error


def predict_by_sklearn_er(fetch_train_func, model, clf_instance):
    x, y = fetch_train_func(model)
    clf_instance.fit(x, y)
    x, actual = get_test(model)
    predict = clf_instance.predict(x).tolist()
    return get_error_measure(actual, predict)


def predict_models(models, to_test_folders, writeReports=True, showResults=False):
    """
    Func: given the models list, return the prediction precision.
    Learners: SVM, CART, Naive Bayes
    Require: TrainSet, TestSet, privatized_set_folder
    :param models:
    :param to_test_folders: from which folders material to predict
    :param writeReports:
    :param showResults:
    :return: no explicit returns. depending on whether to show or write the results...
    """

    # TODO using the neural network
    # by NeuroLab?

    if not type(models) is list:
        models = [models]

    if not type(to_test_folders) is list:
        to_test_folders = [to_test_folders]


    global recorded_attrs
    global _original_recored_index
    global privatized_set_folder
    privatized_set_folder = to_test_folders[0]

    # generate all sklearer clf instances
    from sklearn import svm, tree
    from sklearn.naive_bayes import GaussianNB
    svm_learner = svm.SVC()
    cart_learner = tree.DecisionTreeClassifier()
    gnb = GaussianNB()

    precisions_org = []
    precisions_privatized = defaultdict(dict)
    for model in models:
        recorded_attrs = []
        _original_recored_index = []

        precision_dict = dict()
        precision_dict['svm'] = predict_by_sklearn_er(get_original_train, model, svm_learner)
        precision_dict['cart'] = predict_by_sklearn_er(get_original_train, model, cart_learner)
        precision_dict['nb'] = predict_by_sklearn_er(get_original_train, model, gnb)

        precisions_org.append(precision_dict)

        for predict_material in to_test_folders:
            global privatized_set_folder
            privatized_set_folder = predict_material

            precision_dict = dict()
            precision_dict['svm'] = predict_by_sklearn_er(get_moprhed_train, model, svm_learner)
            precision_dict['cart'] = predict_by_sklearn_er(get_moprhed_train, model, cart_learner)
            precision_dict['nb'] = predict_by_sklearn_er(get_moprhed_train, model, gnb)

            precisions_privatized[model][predict_material] = precision_dict

    # show the results
    if showResults:
        for m, model in enumerate(models):
            print 'MODEL : ', model
            print '-' * 5

            print 'SVM from ORGI:     ', str(precisions_org[m]['svm'])
            for material in to_test_folders:
                print 'SVM after %s: %s' % (material, str(precisions_privatized[model][material]['svm']))
            print '-' * 5

            print 'CART from ORGI:    ', str(precisions_org[m]['cart'])
            for material in to_test_folders:
                print 'SVM after %s: %s' % (material, str(precisions_privatized[model][material]['cart']))
            print '-' * 5

            print 'NB from ORGI:      ', str(precisions_org[m]['nb'])
            for material in to_test_folders:
                print 'SVM after %s: %s' % (material, str(precisions_privatized[model][material]['nb']))
            print '-' * 5

            print '\n\n'

    # write the reports
    if writeReports:
        import datetime
        now = datetime.datetime.now()
        report_output_file_name = project_path + 'Reports/' + 'prediction_measure_'\
            + now.strftime('%y-%m-%d-%H') + '.csv'

        f = open(report_output_file_name, 'w+')

        def look_up_precision_dict(model, learner, measure):
            ff = []
            for material in to_test_folders:
                ff.append(str(round(precisions_privatized[model][material][learner][measure], 2)))
            return ','.join(ff)

        # write the SVM result
        f.write("SVM,,original,"+','.join(to_test_folders)+"\n")
        for model in models:
            f.write("%s,g,%.2f,%s\n" % (model, precisions_org[m]['svm']['g_measure'],
                                        look_up_precision_dict(model, 'svm', 'g_measure')))
            f.write(",pd,%.2f,%s\n" % (precisions_org[m]['svm']['pd'], look_up_precision_dict(model, 'svm', 'pd')))
            f.write(",pf,%.2f,%s\n" % (precisions_org[m]['svm']['pf'], look_up_precision_dict(model, 'svm', 'pf')))

        # write the CART result
        f.write(','.join(['***']*(len(to_test_folders)+3))+"\n")
        f.write("CART,,original,"+','.join(to_test_folders)+"\n")
        for model in models:
            f.write("%s,g,%.2f,%s\n" % (model, precisions_org[m]['cart']['g_measure'],
                                        look_up_precision_dict(model, 'cart', 'g_measure')))
            f.write(",pd,%.2f,%s\n" % (precisions_org[m]['cart']['pd'], look_up_precision_dict(model, 'cart', 'pd')))
            f.write(",pf,%.2f,%s\n" % (precisions_org[m]['cart']['pf'], look_up_precision_dict(model, 'cart', 'pf')))

        # write the NB result
        f.write(','.join(['***']*(len(to_test_folders)+3))+"\n")
        f.write("NB,,original,"+','.join(to_test_folders)+"\n")
        for model in models:
            f.write("%s,g,%.2f,%s\n" % (model, precisions_org[m]['nb']['g_measure'],
                                        look_up_precision_dict(model, 'nb', 'g_measure')))
            f.write(",pd,%.2f,%s\n" % (precisions_org[m]['nb']['pd'], look_up_precision_dict(model, 'nb', 'pd')))
            f.write(",pf,%.2f,%s\n" % (precisions_org[m]['nb']['pf'], look_up_precision_dict(model, 'nb', 'pf')))

        f.close()


if __name__ == '__main__':
    get_moprhed_train('ant-1.3')
    predict_models(['ant-1.3', 'ant-1.6', 'ant-1.7'], writeReports=True, showResults=True)

