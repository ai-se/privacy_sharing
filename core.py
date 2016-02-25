from CLIFF import CLIFF
from MORPH import *
import os
import sys

__author__ = "Jianfeng Chen"
__copyright__ = "Copyright (C) 2016 Jianfeng Chen"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "jchen37@ncsu.edu"

"""
core.py: the main entrance and process for the whole project
available argument list:
-cls                | clear all the generated dataset by this project
-models             | specify one or more models to test
-CLIFF_percentage   | specify the percentage used in the CLIFF algorithm
-testRatio          | set the ratio of test set size (for evaluate the prediction precision)
"""

'''SETTING THE DEFAULT VALUE HERE.'''
DEFAULT = {
    'model': ['ant-1.3','ant-1.4', 'ant-1.5', 'ant-1.6', 'ant-1.7', 'camel-1.6', 'redaktor'],
    'test_set_ratio': 0.3,
    'CLIFF_percentage': 20,
    'MORPH_alpha': 0.15,
    'MORPH_beta': 0.35,
}

_cliff_percent = DEFAULT['CLIFF_percentage']
_test_set_ratio = DEFAULT['test_set_ratio']
models = DEFAULT['model']


def data_set_split(model):
    """
    split the data as testing set and non-testing set (training set)
    :param model: name of the model
    """
    # load the original data
    with open('Dataset/' + model + '.csv', 'r') as db:
        reader = csv.reader(db)
        head = next(reader)
        all_original_data = []
        for line in reader:
            all_original_data.append(line)

    # split the data body
    random.shuffle(all_original_data)
    line = int(len(all_original_data) * (1 - _test_set_ratio))

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
    CLIFF(model, _cliff_percent, writeout=True)  # run CLIFF algorithm
    MORPH(model, writeout=True, alpha=DEFAULT['MORPH_alpha'], beta=DEFAULT['MORPH_beta'])  # run morph algorithm


def program_loading():
    global models, _cliff_percent, _test_set_ratio

    for i, arg in enumerate(sys.argv):
        # parsing the arguments
        if arg in ['-clear', '-cls', '-clean']:
            # delete the files generate by the project
            # will NOT delete the files in dataset
            cliffs = [f for f in os.listdir("./CliffOut") if not f.endswith('.py')]
            morphs = [f for f in os.listdir("./MorphOut") if not f.endswith('.py')]
            tests = [f for f in os.listdir("./TestSet") if not f.endswith('.py')]
            trains = [f for f in os.listdir("./TrainSet") if not f.endswith('.py')]
            for f in cliffs: os.remove("./CliffOut/" + f)
            for f in morphs: os.remove("./MorphOut/" + f)
            for f in tests: os.remove("./TestSet/" + f)
            for f in trains: os.remove("./TrainSet/" + f)
            exit()

        elif arg in ['-model', '-models']:
            # recording all the user_set_models
            for user_set_model in sys.argv[i+1:]:
                if user_set_model[0] == '-': break
                models.append(user_set_model)

        elif arg.lower().startswith('-cliff_per'):  # e.g. -CLIFF_percentage
            # recording the cliff percentage
            percentage = float(sys.argv[i+1])
            percentage *= 100 if percentage <= 1 else 1
            _cliff_percent = int(percentage)
            assert _cliff_percent <= 100, sys.argv[i+1] + " is not a valid percentage."

        elif arg in ['-test_ratio', '-test_set_ratio', '-testratio', '-testRatio']:
            # recording the test set ratio
            _test_set_ratio = float(sys.argv[i+1])
            assert 0 < _test_set_ratio < 1, "test set ratio must be in (0,1)"

        elif arg.startswith('-'):
            # display the waring or manual information
            if arg not in ['-help', '-h']:
                print "ERROR: illegal option: " + arg
            print "available argument list:\n \
                    -cls                | clear all the generated dataset by this project\n \
                    -models             | specify one or more models to test\n \
                    -CLIFF_percentage   | specify the percentage used in the CLIFF algorithm\n \
                    -testRatio          | set the ratio of test set size (for evaluate the prediction precision)"
            exit(0)

    if len(models) == 0:
        models = DEFAULT['model']  # by default, the small dataset. ant-1.3

    # check the validation for the models
    existed_models = [os.path.splitext(f)[0] for f in os.listdir("./Dataset/")]
    for model in models:
        assert model in existed_models, model + "does NOT in the dataset. Please check it again."


if __name__ == '__main__':
    program_loading()

    for model in models:
        main_process(model)

    from evaluate.predict import *
    from evaluate.IPR import *

    predict_models(models, writeReports=True)

    sen_list = ['loc', 'rfc', 'lcom', 'ca', 'ce', 'amc']
    for model in models:
        report_IPR(model, 'DataSet', 'MorphOut', sen_list)
