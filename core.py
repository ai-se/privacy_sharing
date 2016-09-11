from CLIFF import CLIFF
from MORPH import *
import sys, os

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
    'model': ['camel-1.6', 'xerces-1.4', 'ant-1.6', 'ant-1.7'],
    'test_set_ratio': 0.2,
    'CLIFF_percentage': 20,
    'Lace2_holder_number': 5,
    'MORPH_alpha': 0.15,
    'MORPH_beta': 0.35,
}

_cliff_percent = DEFAULT['CLIFF_percentage']
_test_set_ratio = DEFAULT['test_set_ratio']
models = DEFAULT['model']


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

    # discrete the dependent variable
    classes = [i[-1] for i in all_original_data]  # last column in the origin csv file
    classes = map(data_tools.str2num, classes)
    if 0 in classes:
        # binary the classification
        classes = [int(bool(int(c))) for c in classes]
    else:
        from data_tools import binrange
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

    from LACE1 import LACE1
    LACE1(model, 'TrainSet', 'Lace1Out', _cliff_percent, DEFAULT['MORPH_alpha'],
          DEFAULT['MORPH_beta'], ['all_attributes'])

    from LACE2 import LACE2
    LACE2(model, 'TrainSet', 'Lace2Out', DEFAULT['Lace2_holder_number'],
          _cliff_percent, DEFAULT['MORPH_alpha'], DEFAULT['MORPH_beta'])


def exp4school():
    print('========Here is the experiment for shcoolcard model========')
    model = 'school'

    data_set_split(model)
    from LACE1 import LACE1
    LACE1(model,
          'TrainSet',
          'Lace1Out',
          _cliff_percent,
          DEFAULT['MORPH_alpha'],
          DEFAULT['MORPH_beta'],
          ['ADM_RATE', 'SAT_AVG', 'TUITFTE', 'RET_FT4', 'PCTFLOAN', 'PCTPELL', 'DEBT_MDN', 'C150_4', 'CDR3'])

    print('Wrote in LACE1.')

    from evaluate.predict import *
    predict_models([model], ['Lace1Out'], writeReports=True)
    print("Lace1 predict report wrote.")


def program_loading():
    global models, _cliff_percent, _test_set_ratio

    for i, arg in enumerate(sys.argv):
        # parsing the arguments
        if arg in ['-clear', '-cls', '-clean']:
            # delete the files generate by the project
            # will NOT delete the files in dataset
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
                    matches. append(os.path.join(root,filename))
            for f in matches: os.remove(f)

            exit()

        elif arg in ['-model', '-models']:
            models = []
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
                print("ERROR: illegal option: " + arg)
            print("available argument list:\n \
                    -cls                | clear all the generated dataset by this project\n \
                    -models             | specify one or more models to test\n \
                    -CLIFF_percentage   | specify the percentage used in the CLIFF algorithm\n \
                    -testRatio          | set the ratio of test set size (for evaluate the prediction precision)")
            exit(0)

    if len(models) == 0:
        models = DEFAULT['model']  # by default, the small dataset. ant-1.3

    # check the validation for the models
    existed_models = [os.path.splitext(f)[0] for f in os.listdir("./Dataset/")]
    for model in models:
        assert model in existed_models, model + "does NOT in the dataset. Please check it again."

# if __name__ == '__main__':
#     program_loading()
#     for model in models:
#         main_process(model)
#
#     from evaluate.predict import *
#     from evaluate.IPR import *
#     from evaluate.apriori_cmpr import *
#
#     predict_models(models, ['Lace1Out', 'Lace2Out'], writeReports=True)
#
#     sen_list = ['loc']  # one sensitive attribute
#     for model in models:
#         report_IPR(model, 'DataSet', 'Lace1Out', sen_list)
#         report_IPR(model, 'DataSet', 'Lace2Out', sen_list)
#
#     for model in models:
#         apriori_report(model, 'DataSet', 'Lace1Out', conclusion_only=True, min_support=0.4, min_confidence=0.8)
#         apriori_report(model, 'DataSet', 'Lace2Out', conclusion_only=True, min_support=0.4, min_confidence=0.8)

if __name__ == '__main__':
    import debug
    program_loading()
    exp4school()
