from __future__ import division
from collections import defaultdict
from sklearn.metrics import mean_squared_error, mean_absolute_error
import settings
import toolkit
import pdb

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.3"
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


# TODO only for the binary
# TODO how to cmpr when continuous?
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

    if len(set(actual)) == 2: # binary version err measure
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
    else:  # multi-classfication
        print(mean_squared_error(actual, predict))
        print(mean_absolute_error(actual, predict))
        pdb.set_trace()


def predicting(x, y, model, clf_instance):
    pdb.set_trace()
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

    # generate all sklearer clf instances
    from sklearn import svm, tree
    from sklearn.multiclass import OneVsOneClassifier
    from sklearn.naive_bayes import GaussianNB
    # TODO bug svm learner
    # svm_learner = OneVsOneClassifier(svm.LinearSVC())
    cart_learner = tree.DecisionTreeClassifier()
    gnb = GaussianNB()

    precs_org = []
    precs_prtz = defaultdict(dict)
    for model in models:
        prec_di = dict()
        x, y = get_moprhed_train('Lace2Out', model)
        # x, y = get_original_train(model)
        # prec_di['svm'] = predicting(x, y, model, svm_learner)
        prec_di['cart'] = predicting(x, y, model, cart_learner)
        prec_di['nb'] = predicting(x, y, model, gnb)

        precs_org.append(prec_di)

        for predict_material in we_report_folder:
            global privatized_set_folder
            privatized_set_folder = predict_material

            prec_di = dict()
            prec_di['svm'] = predicting(get_moprhed_train, model, svm_learner)
            prec_di['cart'] = predicting(get_moprhed_train, model, cart_learner)
            prec_di['nb'] = predicting(get_moprhed_train, model, gnb)

            precs_prtz[model][predict_material] = prec_di

    # write the reports
    import datetime
    now = datetime.datetime.now()
    report_output_file_name = project_path + 'Reports/' + 'prediction_measure_'\
        + now.strftime('%y-%m-%d-%H') + '.csv'

    f = open(report_output_file_name, 'w+')

    def check_prtz_prec(model, learner, measure):
        ff = []
        for material in we_report_folder:
            ff.append(str(round(precs_prtz[model][material][learner][measure], 2)))
        return ','.join(ff)

    # write the SVM result
    f.write("SVM,,original," +','.join(we_report_folder) + "\n")
    for m, model in enumerate(models):
        f.write("%s,g,%.2f,%s\n" % (model, precs_org[m]['svm']['g_measure'],
                                    check_prtz_prec(model, 'svm', 'g_measure')))
        f.write(",pd,%.2f,%s\n" % (precs_org[m]['svm']['pd'], check_prtz_prec(model, 'svm', 'pd')))
        f.write(",pf,%.2f,%s\n" % (precs_org[m]['svm']['pf'], check_prtz_prec(model, 'svm', 'pf')))

    # write the CART result
    f.write(','.join(['***'] * (len(we_report_folder) + 3)) + "\n")
    f.write("CART,,original," +','.join(we_report_folder) + "\n")
    for m, model in enumerate(models):
        f.write("%s,g,%.2f,%s\n" % (model, precs_org[m]['cart']['g_measure'],
                                    check_prtz_prec(model, 'cart', 'g_measure')))
        f.write(",pd,%.2f,%s\n" % (precs_org[m]['cart']['pd'], check_prtz_prec(model, 'cart', 'pd')))
        f.write(",pf,%.2f,%s\n" % (precs_org[m]['cart']['pf'], check_prtz_prec(model, 'cart', 'pf')))

    # write the NB result
    f.write(','.join(['***'] * (len(we_report_folder) + 3)) + "\n")
    f.write("NB,,original," +','.join(we_report_folder) + "\n")
    for m, model in enumerate(models):
        f.write("%s,g,%.2f,%s\n" % (model, precs_org[m]['nb']['g_measure'],
                                    check_prtz_prec(model, 'nb', 'g_measure')))
        f.write(",pd,%.2f,%s\n" % (precs_org[m]['nb']['pd'], check_prtz_prec(model, 'nb', 'pd')))
        f.write(",pf,%.2f,%s\n" % (precs_org[m]['nb']['pf'], check_prtz_prec(model, 'nb', 'pf')))

    f.close()


if __name__ == '__main__':
    predict_models(['ant-1.7', 'camel-1.6'], we_report_folder=['Lace1Out', 'Lace2Out'])

