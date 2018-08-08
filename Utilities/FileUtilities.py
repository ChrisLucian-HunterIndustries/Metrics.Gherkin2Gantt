import os
from distutils.dir_util import copy_tree


def move_from_results_to_sharepoint(share_point_location):
    copy_from_location = 'Results'
    copy_tree(copy_from_location, share_point_location)


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)