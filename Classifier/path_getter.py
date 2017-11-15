import os


def get_path(relativePath):
    abs_path = os.path.abspath(relativePath)
    return abs_path
