""" 17 Category Flower Dataset

Credits: Maria-Elena Nilsback and Andrew Zisserman.
http://www.robots.ox.ac.uk/~vgg/data/flowers/17/

"""
from __future__ import absolute_import

import os
import sys
import urllib
import tarfile

import numpy as np
import pickle

from ..data_utils import *


def load_data(dirname="17flowers", resize_pics=(224, 224), shuffle=True,
    one_hot=False):
    dataset_file = os.path.join(dirname, '17flowers.pkl')
    if not os.path.exists(dataset_file):
        tarpath = maybe_download("17flowers.tgz",
                                 "http://www.robots.ox.ac.uk/~vgg/data/flowers/17/",
                                 dirname)

    X, Y = build_image_dataset_from_dir('17flowers/jpg/',
                                        dataset_file="17flowers.pkl",
                                        resize=resize_pics,
                                        filetypes=['.jpg', '.jpeg'],
                                        convert_gray=False,
                                        shuffle_data=shuffle,
                                        categorical_Y=one_hot)

    return X, Y


def maybe_download(filename, source_url, work_directory):
    if not os.path.exists(work_directory):
        os.mkdir(work_directory)
    filepath = os.path.join(work_directory, filename)
    if not os.path.exists(filepath):
        print("Downloading Oxford 17 category Flower Dataset, Please "
              "wait...")
        filepath, _ = urllib.urlretrieve(source_url + filename, filepath)
        statinfo = os.stat(filepath)
        print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')

        untar(filepath, work_directory)
        build_class_directories(os.path.join(work_directory, 'jpg'))
    return filepath


def build_class_directories(dir):
    dir_id = 0
    class_dir = os.path.join(dir, str(dir_id))
    if not os.path.exists(class_dir):
        os.mkdir(class_dir)
    for i in range(1, 1361):
        if i % 80 == 0 and dir_id < 16:
            dir_id += 1
            class_dir = os.path.join(dir, str(dir_id))
            os.mkdir(class_dir)
        fname = "image_" + ("%.4i" % i) + ".jpg"
        os.rename(os.path.join(dir, fname),
                  os.path.join(class_dir, fname))


def untar(fname, extract_dir):
    if fname.endswith("tar.gz") or fname.endswith("tgz"):
        tar = tarfile.open(fname)
        tar.extractall(extract_dir)
        tar.close()
        print "File Extracted"
    else:
        print "Not a tar.gz/tgz file: '%s '" % sys.argv[0]