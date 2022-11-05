# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/22 15:14
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/6/6 22:48
from typing import Tuple

from golf_federated.utils.data import generate_fl_data, deepcopy_list
from golf_federated.utils.log import loggerhear
from numpy import ndarray


class CustomFederatedDataset(object):
    """

    Class for custom federated datasets.
    Support users to create server or client dataset class objects.
    And divided into training set, test set, multi-part data and other requirements-based content.

    """

    def __init__(
            self,
            train_data: list = [],
            train_label: list = [],
            test_data: list = [],
            test_label: list = [],
            part_num: int = 1,
            part_id: list = [],
            split_data: bool = False,
    ) -> None:
        """

        Initialize the dataset object.

        Args:
            train_data (list): List of file paths to store data values for training. Default as [].
            train_label (list): List of file paths to store data labels for training. Default as [].
            test_data (list): List of file paths to store data values for evaluation. Default as [].
            test_label (list): List of file paths to store data labels for evaluation. Default as [].
            part_num (int): Number of datasets that will be divided and distributed to clients. If dataset is for server, the number of divisions is 1. Default as 1.
            part_id (list): List of names of divided parts, usually the client names. Dataset for server can not set this property. Default as [].
            split_data (bool): Whether the above data file lists are divided according to part_id. Default as False.

        """

        # Initialize object properties.
        self.total_train_data = deepcopy_list(train_data)
        self.total_train_label = deepcopy_list(train_label)
        self.total_test_data = deepcopy_list(test_data)
        self.total_test_label = deepcopy_list(test_label)
        self.part_num = part_num
        self.part_id = deepcopy_list(part_id)
        self.split_data = split_data

        # Judge whether part_id corresponds to part_num.
        if len(part_id) > 0 and len(part_id) != part_num:
            # If part_id does not correspond to part_num, use default part_id.
            loggerhear.log("Please Note  ",
                           'part_id and part_num do not match. Here, serial number is used as part_id.')
            self.part_id = [str(i + 1) for i in range(part_num)]

        # Integrate collections of data files into data.
        federated_data = generate_fl_data(
            train_data=self.total_train_data,
            train_label=self.total_train_label,
            test_data=self.total_test_data,
            test_label=self.total_test_label,
            part_num=self.part_num,
            part_id=self.part_id,
            split_data=self.split_data,
        )

        # Extract from integrated results.
        self.part_data = federated_data['trainPart']
        self.test_data = federated_data['testX']
        self.test_label = federated_data['testY']

    def part_to_list(self) -> list:
        """

        The names and corresponding data in the object are stored in dictionaries.
        This function converts the data in dictionary to list.

        Returns:
            List: Converted data list.

        """

        return_list = list(self.part_data.values())
        return return_list

    def get_part_train(
            self,
            part: str
    ) -> Tuple[ndarray, ndarray, int]:
        """

        Get the training set content corresponding to a part name.

        Args:
            part (str): Specify part name.

        Returns:
            List: Return as a list, including:
                part_train_x (numpy.ndarray): Data values for training.
                part_train_y (numpy.ndarray): Data labels for training.
                part_train_shape (int): Data size for training.

        """

        part_train_x, part_train_y, part_train_shape = self.part_data[part]
        return part_train_x, part_train_y, part_train_shape
