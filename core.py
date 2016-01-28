import pdb, csv, re
from CLIFF import *
from MORPH import *
import os,sys
import glob

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
"""

'''SETTING THE DEFAULT VALUE HERE.'''
DEFAULT = {
    'model': 'ant-1.3',
    'CLIFF_percentage': 20,

}

_cliff_percent = DEFAULT['CLIFF_percentage']


def main_process(model):
    print _cliff_percent
    print model


if __name__ == "__main__":
    models = []

    for i, arg in enumerate(sys.argv):

        if arg in ['-clear', '-cls']:
            # delete the files generate by the project
            # will NOT delete the files in dataset
            cliffs = [f for f in os.listdir("./CliffOut") if not f.endswith('.py')]
            morphs = [f for f in os.listdir("./MorphOut") if not f.endswith('.py')]
            for f in cliffs: os.remove("./CliffOut/" + f)
            for f in morphs: os.remove("./MorphOut/" + f)
            exit()

        if arg in ['-model', '-models']:
            # recording all the user_set_models
            for user_set_model in sys.argv[i+1:]:
                if user_set_model[0] == '-': break
                models.append(user_set_model)

        if arg.lower().startswith('-cliff_per'):  # e.g. -CLIFF_percentage
            # recording the cliff percentage
            percentage = float(sys.argv[i+1])
            percentage *= 100 if percentage <= 1 else 1
            _cliff_percent = int(percentage)
            assert _cliff_percent <= 100, sys.argv[i+1] + " is not a valid percentage."

    if len(models) == 0:
        models = [DEFAULT['model']]  # by default, the small dataset. ant-1.3

    # check the validation for the models
    existed_models = [os.path.splitext(f)[0] for f in os.listdir("./Dataset/")]
    for model in models:
        assert model in existed_models, model + "does NOT in the dataset. Please check it again."

    for model in models:
        main_process(model)
