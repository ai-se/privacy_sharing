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
"""


def main_process():
    # TODO ...


if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if arg in ['-clear', '-cls']:
            # delete the files generate by the project
            # will NOT delete the files in dataset
            cliffs = [f for f in os.listdir("./CliffOut") if not f.endswith('.py')]
            morphs = [f for f in os.listdir("./MorphOut") if not f.endswith('.py')]
            pdb.set_trace()
            for f in cliffs: os.remove("./CliffOut/" + f)
            for f in morphs: os.remove("./MorphOut/" + f)
            exit()

    main_process()
