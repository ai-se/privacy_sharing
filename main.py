from LACE1 import LACE1
from LACE2 import LACE2
from evaluate.predict import *
from evaluate.apriori_cmpr import *
from evaluate.IPR import *
import sys
import os
import settings

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "2.2"
__email__ = "jchen37@ncsu.edu"

"""
To clean, run python core.py -cls
"""


def data_set_split(model):
    """
    split the data as testing set and non-testing set (training set)
    NOTE: handing the dependent variable here.
    :param model: name of the model
    """
    # load the original data
    with open('Dataset/' + model + '.csv', 'r') as db:
        reader = csv.reader(db)
        head = next(reader)
        all_original_data = []
        for line in reader:
            all_original_data.append(line)

    # discrete the independent variable
    classes = [i[-1] for i in all_original_data]  # last column in the origin csv file
    classes = map(toolkit.str2num, classes)
    if 0 in classes:
        # binary the classification
        classes = [int(bool(int(c))) for c in classes]
    else:
        from toolkit import binrange
        slot = binrange(classes)
        tmp_c = list()
        for c in classes:
            cursor = 0
            for i in slot:
                if c > i:
                    cursor += 1
                else:
                    break
            tmp_c.append(cursor)
        classes = tmp_c

    for l, c in zip(all_original_data, classes):
        l[-1] = c
    # discrete done

    # split the data body
    random.shuffle(all_original_data)
    line = int(len(all_original_data) * (1 - settings.test_set_ratio))

    # write the train set
    with open('TrainSet/' + model + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([head])
        writer.writerows(all_original_data[0:line])

    # write the test set
    with open('TestSet/' + model + '.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([head])
        writer.writerows(all_original_data[line:])


def main_process(model):
    """
    split the model training set and testing set
    do the CLIFF algorithm
    do the MORPH algorithm
    :param model:
    :return:
    """
    data_set_split(model)
    #
    # from LACE1 import LACE1
    # LACE1(model, 'TrainSet', 'Lace1Out', _cliff_percent, DEFAULT['MORPH_alpha'],
    #       DEFAULT['MORPH_beta'], ['all_attributes'])
    #
    # from LACE2 import LACE2
    # LACE2(model, 'TrainSet', 'Lace2Out', DEFAULT['Lace2_holder_number'],
    #       _cliff_percent, DEFAULT['MORPH_alpha'], DEFAULT['MORPH_beta'])


def exp4school():
    print('========Here is the experiment for shcoolcard model========')
    assert settings.model == ['school'], "check the model settings in setting.py"

    model = 'school'
    data_set_split(model)

    LACE1(model, 'TrainSet', 'Lace1Out')
    LACE2(model, 'TrainSet', 'Lace2Out')

    # predict_models(model, ['Lace1Out', 'Lace2Out'])
    # print('precision report done...')

    # apriori_report(model, 'TrainSet', ['Lace1Out', 'Lace2Out'])
    # print('apriori report done...')

    ipr_report(model, 'TrainSet', ['Lace1Out', 'Lace2Out'])
    # print('ipr report done...')


def cleaning():
    cliffs = [f for f in os.listdir("./CliffOut") if not f.endswith('.py')]
    lace1s = [f for f in os.listdir("./Lace1Out") if not f.endswith('.py')]
    lace2s = [f for f in os.listdir("./Lace2Out") if not f.endswith('.py')]
    tests = [f for f in os.listdir("./TestSet") if not f.endswith('.py')]
    trains = [f for f in os.listdir("./TrainSet") if not f.endswith('.py')]
    for f in cliffs: os.remove("./CliffOut/" + f)
    for f in lace1s: os.remove("./Lace1Out/" + f)
    for f in lace2s: os.remove("./Lace2Out/" + f)
    for f in tests: os.remove("./TestSet/" + f)
    for f in trains: os.remove("./TrainSet/" + f)

    # delete the temporary file in the project
    import fnmatch
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.pyc'):
            matches.append(os.path.join(root, filename))
    for f in matches: os.remove(f)


if __name__ == '__main__':
    if set(sys.argv) & {'-clear', '-cls', '-clean'}:
        cleaning()
        print("cleaning...done")
        exit(0)

    import debug
    for i in range(20):
        exp4school()
        print('Repeat %d done.'%i)

