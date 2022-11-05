# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/25 17:49
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/6/15 10:29
from golf_federated.utils.log import loggerhear


class BasicFed(object):
    """

    Aggregation strategy base class

    """

    def __init__(
            self,
            name: str,
            synchronous: bool,
            min_to_start: int
    ) -> None:
        """

        Initialize the base class object of the aggregation strategy, which is called when subclasses inherit.

        Args:
            name (str): Name of aggregation strategy.
            synchronous (bool): Synchronous FL or not.
            min_to_start (int): Minimum number of received local model parameters for global model aggregation.

        """

        # Initialize object properties.
        self.name = name
        self.synchronous = synchronous
        self.min_to_start = min_to_start
        self.aggregation_num = 0
        self.global_w = []

    def aggregate(
            self,
            datadict: dict
    ) -> None:
        """

        Aggregation function. This needs to be overridden in subclasses.

        Args:
            datadict (dict): Data that will be input into the aggregation function, which varies by aggregation strategies.

        """

        # If this function is called directly or not overridden, output log will indicate undefined.
        loggerhear.log("Error Message", 'Aggregation method not defined')
