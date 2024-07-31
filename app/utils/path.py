import os


def current_dir(file_name):
    current_dir = os.getcwd()
    return os.path.join(current_dir, file_name)
