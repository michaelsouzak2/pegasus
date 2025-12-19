import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import shutil


def load_yaml(path):
    with open(path, "r") as f:
        loaded = yaml.safe_load(f)
    return loaded


def clear_directory(dir_path):
    for item in dir_path.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def atleast_nd(a, ndim):
    a = np.asarray(a)
    if a.ndim >= ndim:
        return a
    else:
        return np.expand_dims(a, tuple(range(ndim - a.ndim)))

def make_get_object_by_name(objects):
    def get_object_by_name(name):
        for obj in objects:
            if obj.__name__.lower() == name.lower():
                return obj
        raise ValueError(f"{name} is not defined")
    return get_object_by_name


def get_min_max(data, extra_ratio=0, err_ret=None):
    if data.size == 0:
        return err_ret, err_ret

    vmin = np.min(data)
    vmax = np.max(data)
    delta = vmax - vmin
    
    if extra_ratio > 0:
        vmin -= extra_ratio * delta
        vmax += extra_ratio * delta
    
    return vmin, vmax


def get_expected_location(coords, proba, as_int=False):
    # <https://en.wikipedia.org/wiki/Expected_value>
    # E = sum(x_i * p_i), where sum(p_i) = 1
    expectation = np.sum(proba[..., None] * coords, axis=(0, 1)) / proba.sum()
    if as_int:
        expectation = np.round(expectation).astype(int)
    return tuple(expectation)


def parse_date(s):
    return datetime.strptime(s, "%d-%b-%Y %H:%M:%S.%f")


def make_date_interval_days(date, before=0, after=0):
    date_min = date - timedelta(days=before)
    date_max = date + timedelta(days=after)
    return date_min, date_max

def delete_path(target_path):
    p = Path(target_path)

    if p.is_file():
        p.unlink()
    elif p.is_dir():
        for child in p.iterdir():
            delete_path(child)
        p.rmdir()
    else:
        print(f"'{p}' is neither a file nor a directory.")