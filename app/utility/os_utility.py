import os


def make_dir_if_not_exist(dir_path: str):
    try:
        os.mkdir(dir_path)
    except:
        print("INFO: Directory {} already exists".format(dir_path))
        pass
