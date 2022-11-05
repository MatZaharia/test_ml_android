# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/22 19:26
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/27 0:15

import os
from collections import Counter
from typing import Any
import h5py
import numpy as np
from numpy import ndarray
from math import log
from golf_federated.utils.log import loggerhear


def generate_fl_data(
        train_data: list,
        train_label: list,
        test_data: list,
        test_label: list,
        part_num: int,
        part_id: list = [],
        split_data: bool = False,
) -> dict:
    """

    Organize the input file paths, data division information, etc. into dictionary data.
    Default division of the training data part is named as number, which is defined in dataset class.

    Args:
        train_data (list): List of file paths to store data values for training.
        train_label (list): List of file paths to store data labels for training.
        test_data (list): List of file paths to store data values for evaluation.
        test_label (list): List of file paths to store data labels for evaluation.
        part_num (int): Number of datasets that will be divided and distributed to clients. If dataset is for server, the number of divisions is 1.
        part_id (list): List of names of divided parts, usually the client names. Dataset for server can not set this property. Default as [].
        split_data (bool): Whether the above data file lists are divided according to part_id. Default as False.

    Returns:
        Dict: Return after sorting the data into a dictionary, including:
                            'trainPart' (dict): Each part of training data and its ID are stored in a dictionary.
                            'testX' (numpy.ndarray): Organized evaluation data values, use an array to store different records.
                            'testY' (numpy.ndarray): Organized evaluation data labels, use an array to store different records

    """

    # Judge whether the values and labels of train and evaluation data correspond to each other.
    if load_file_list(train_data)['shape'] != load_file_list(train_label)['shape'] \
            or load_file_list(test_data)['shape'] != load_file_list(test_label)['shape']:
        # If one of them does not correspond, output the log and terminate the program.
        loggerhear.log("Error Message", 'You read data and labels with mismatched sizes.' +
                       '\n     Train data has sizes of ' +
                       str(load_file_list(train_data)['shape']) +
                       '\n     while the label has sizes of ' +
                       str(load_file_list(train_label)['shape']) +
                       '\n     Test data has sizes of ' +
                       str(load_file_list(test_data)['shape']) +
                       '\n     while the label has sizes of ' +
                       str(load_file_list(test_label)['shape']))
        exit(1)

    else:
        # Load data from files.
        x_train = load_file_list(train_data)['data']
        y_train = load_file_list(train_label)['data']
        x_test = load_file_list(test_data)['data']
        y_test = load_file_list(test_label)['data']

        # If entire training data is divided according to the set number of parts and part IDs, it is necessary to ensure that the sizes of these things correspond to each other.
        if split_data and len(x_train) == len(y_train) == part_num == len(part_id):
            # If it matches, it will be divided according to the set content.
            loggerhear.log("Common Info  ", 'Split data is initializing according to part_id')
            part_data = match_id_data(
                x=x_train,
                y=y_train,
                part_id=part_id,
                part_num=part_num
            )

        else:
            # Judge whether there are related attributes to set the division.
            if split_data:
                # If there are settings but do not meet the requirements, the user will be notified that the default division method will be used, and the program will not be terminated
                loggerhear.log("Please Note  ",
                               'Number of split data does not match part_num. Here, all data is divided into designed numbers.')

            else:
                loggerhear.log("Common Info  ", 'Here, all data is divided into designed numbers.')

            # Judge whether to initialize training data.
            if len(x_train) > 0 and len(y_train) > 0:
                x_merge = merge_data(x_train)
                y_merge = merge_data(y_train)
                split_data = split_to_num(
                    x=x_merge,
                    y=y_merge,
                    to_num=part_num
                )
                part_data = match_id_data(
                    x=split_data['x'],
                    y=split_data['y'],
                    part_id=part_id,
                    part_num=part_num
                )

            else:
                part_data = []

        # Judge whether to initialize evaluation data.
        if len(x_test) > 0 and len(y_test) > 0:
            x_merge_test = merge_data(x_test)
            y_merge_test = merge_data(y_test)
        else:
            x_merge_test = []
            y_merge_test = []

        loggerhear.log("Common Info  ", 'FL Data Load Successful.')

        # Organized into a dictionary.
        return_dict = {
            'trainPart': part_data,
            'testX': x_merge_test,
            'testY': y_merge_test
        }

        return return_dict


def split_to_num(
        x: ndarray,
        y: ndarray,
        to_num: int,
) -> dict:
    """

    Divide data into specified amount.

    Args:
        x (numpy.ndarray): Data values.
        y (numpy.ndarray): Data labels.
        to_num (int): Number of datasets that will be divided and distributed to clients.

    Returns:
        Dict: Data is returned as a dictionary, including:
                            'x' (list): List of divided data values.
                            'y' (list): List of divided data labels.

    """

    # Size of data values and labels.
    x_shape = x.shape[0]
    y_shape = y.shape[0]

    # Judge whether the size of the data value and label match.
    if x_shape != y_shape:
        # Output log and terminate program if there is no match.
        loggerhear.log("Error Message", 'Unable to split data due to size mismatch (%d - %d)' % (x_shape, y_shape))
        exit(1)

    else:
        # Divide data into specified amount.
        return_x = []
        return_y = []
        part_size = int(to_num / x_shape)
        for num in range(to_num):
            begin = num * part_size
            if num == to_num - 1:
                end = (num + 1) * part_size
            else:
                end = x_shape
            return_x.append(x[begin:end])
            return_y.append(y[begin:end])

        # Represent data values and labels as a dictionary.
        return_dict = {
            'x': return_x,
            'y': return_y
        }

        return return_dict


def merge_data(data_list: list):
    """

    Merge data stored in list into an array.

    Args:
        data_list (list): List of data.

    Returns:
        Numpy.ndarray: Merged data array.

    """

    # Merge data using a loop.
    first = True
    merge_data = data_list[0]
    for data in data_list:
        if first:
            first = False
            continue
        else:
            merge_data = np.concatenate((merge_data, data), axis=0)

    return merge_data


def match_id_data(
        x: ndarray,
        y: ndarray,
        part_id: list,
        part_num: int
) -> dict:
    """

    The divided data and each part id are represented by a dictionary.

    Args:
        x (numpy.ndarray): Value of the divided data, generally stored in an array, or stored in a list.
        y (numpy.ndarray): Label of the divided data, generally stored in an array, or stored in a list.
        part_id (list): List of names of divided parts, usually the client names.
        part_num (int): Number of parts.

    Returns:
        Dict: A dictionary that stores the divided data and their names.

    """

    # Initialize a dictionary.
    return_dict = dict()

    # List or array.
    try:
        data_shape = x.shape[0]
    except:
        data_shape = len(x)

    # Use a loop to store parts of data, including values, labels and their sizes.
    for num in range(part_num):
        return_dict[part_id[num]] = [x[num], y[num], data_shape]

    return return_dict


def load_file_list(filelist: list) -> dict:
    """

    Load data from a list of file paths.

    Args:
        filelist (list): List of file paths to store data.

    Returns:
        Dict: Data is returned as a dictionary, including a list of data and a list of corresponding sizes.

    """

    # Initialize lists.
    data_list = []
    data_shape_list = []

    # Use a loop to read data.
    for file in filelist:
        data = load_file(file)
        try:
            data_shape = data.shape[0]
        except:
            data_shape = len(data)
        data_list.append(data)
        data_shape_list.append(data_shape)

    # Data is represented by a dictionary.
    return_dict = {
        'data': data_list,
        'shape': data_shape_list
    }

    return return_dict


def load_file(filepath: str) -> ndarray:
    """

    Load data from the specified file path.

    Args:
        filepath (str): The file path where the data is stored.

    Returns:
        Numpy.ndarray: Loaded data.

    """

    loggerhear.log("Common Info  ", 'Loading Data from %s' % os.path.abspath(filepath))
    file_extension = os.path.splitext(filepath)[-1]

    # Judge the file format.
    if file_extension == '.npy':
        # Use numpy library functions to read npy files
        item = np.load(filepath)

    else:
        # When asked to read an unsupported file format, log out and terminate the program.
        loggerhear.log("Error Message", 'Loading %s Error' % filepath)
        exit(1)

    return item


def calculate_IW(y: ndarray) -> float:
    """

    Calculate the information weighted value of client data.

    Args:
        y (numpy.ndarray): Client data labels.

    Returns:
        Float: Calculated information weighted value.

    """

    # Initialize.
    IW = 0
    xx = np.zeros(y.shape[1])
    part = np.zeros(10)

    # Calculate information entropy.
    for i in range(0, y.shape[0]):
        for j in range(0, y.shape[1]):
            if y[i, j] == 1:
                xx[j] += 1
    for i in range(0, 10):
        part[i] = xx[i] / y.shape[0]
        if part[i] == 0:
            continue
        IW += part[i] * log(part[i], 2) * (-1)

    # Keep 3 decimals.
    IW = round(IW, 3)

    return IW


def calculate_SIC(
        new_label: ndarray,
        old_label: ndarray,
        c: float
) -> float:
    """

    Calculate self-information change indicator of data.

    Args:
        new_label (ndarray): Labels of new data.
        old_label (ndarray): Labels of old data.
        c (float): A constant used to avoid the generation of infinite value.

    Returns:
        Float: The self-information change indicator.

    """

    # Relevant statistics based on data labels.
    element_new = dict(Counter(new_label))
    element_old = dict(Counter(old_label))
    len_new_label = sum(element_new.values())
    len_old_label = sum(element_old.values())
    label_old = list(element_old.keys())
    label_new = list(element_new.keys())
    label_sum = set(label_old + label_new)

    # Calculate SIC.
    SIC = 0
    for label in label_sum:
        if label in element_new:
            p_new = element_new[label] / len_new_label
        else:
            p_new = 0
        if label in element_old:
            p_old = element_old[label] / len_old_label
        else:
            p_old = 0
        SIC = SIC + p_new * log((p_new + c) / (p_old + c), 2)

    return SIC


def calculate_information_entropy(label: ndarray) -> float:
    """

    Calculate information entropy of data.

    Args:
        label (ndarray): Labels of data.

    Returns:
        Float: The information entropy.

    """

    # Relevant statistics based on data labels.
    element = dict(Counter(label))
    len_label = sum(element.values())

    # Calculate information entropy.
    infor_entropy = 0
    for label in element:
        a = element[label] / len_label
        infor_entropy = infor_entropy + a * log(a, 2) * (-1)

    return infor_entropy


def save_to_h5(
        content: Any,
        filename: str
) -> None:
    """

    Save the specified content to an h5 file.

    Args:
        content (Any): The specified content.
        filename (str): Name of the h5 file.

    """

    with h5py.File(filename + '.h5') as f:
        f['data'] = content
        f.close()
    loggerhear.log("Common Info  ", 'The specified content is written to %s.h5.' % filename)


def calculate_label_num(label: ndarray) -> float:
    """

        Calculate the number of data labels.

        Args:
            label (ndarray): Labels of data.

        Returns:
            Float: The number of data labels.

    """

    len_label = len(set(label))

    return len_label


def deepcopy_list(list_to_copy: list) -> list:
    """

    Deep copy list iteratively.

    Args:
        list_to_copy (list): Source of copy.

    Returns:
        List: Result of deep copy.

    """

    if len(list_to_copy) == 0:
        return []
    else:
        if type(list_to_copy[0]) != list:
            return [x for x in list_to_copy]
        else:
            return [deepcopy_list(list_to_copy[x]) for x in range(len(list_to_copy))]


def list_normalization(list_: list) -> list:
    """

    Normalize the list of data.

    Args:
        list_ (list): Data list.

    Returns:
        List: Normalized data list.

    """
    list_min = min(list_)
    list_max = max(list_)
    if list_max == list_min:
        return [1 / len(list_) for i in range(len(list_))]
    else:
        return [(list_[i] - list_min) / (list_max - list_min) for i in range(len(list_))]

from torch.utils.data.dataset import Dataset
class simple_dataset(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label
        self.length = data.shape[0]

    def __getitem__(self, mask):
        label = self.label[mask]
        data = self.data[mask]
        return label, data

    def __len__(self):
        return self.length
