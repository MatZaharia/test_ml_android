# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/24 13:35
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/20 17:43
from golf_federated.strategy.aggregation.function import fedavg, SLMFedsyn
from golf_federated.strategy.aggregation.basic import BasicFed
from golf_federated.utils.data import deepcopy_list
from golf_federated.utils.log import loggerhear


class FedAVG(BasicFed):
    """

    Synchronous FL with FedAVG.
    From: "Communication-Efficient Learning of Deep Networks from Decentralized Data"
            (http://proceedings.mlr.press/v54/mcmahan17a/mcmahan17a.pdf)

    """

    def __init__(self) -> None:
        """

        Initialize the class object.

        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='fedavg',
            synchronous=True,
            min_to_start=2
        )
        loggerhear.log("Server Info  ", "Being Adopting FedAVG")

    def aggregate(
            self,
            datadict: {
                'weight': list,
                'data_size': list
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             'weight' (list): List of client model parameters.
                             'data_size' (list): List of data sizes on clients.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        weight = deepcopy_list(datadict['weight'])
        data_size = deepcopy_list(datadict['data_size'])

        current_global_w = fedavg(weight, data_size)
        self.global_w.append(current_global_w)

        return current_global_w


class FedProx(BasicFed):
    """

    Synchronous FL with FedProx.
    From: ""
            ()

    """

    def __init__(
            self,
            miu:float=1
    ) -> None:
        """

        Initialize the class object.

        Args:
            miu (float): Corresponds to the parameter μ defined in FedProx. Default as 1.

        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='fedprox',
            synchronous=True,
            min_to_start=2
        )
        self.miu = miu
        loggerhear.log("Server Info  ", "Being Adopting FedProx")

    def aggregate(
            self,
            datadict: {
                'weight': list,
                'data_size': list
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             'weight' (list): List of client model parameters.
                             'data_size' (list): List of data sizes on clients.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        weight = deepcopy_list(datadict['weight'])
        data_size = deepcopy_list(datadict['data_size'])

        current_global_w = fedavg(weight, data_size)
        self.global_w.append(current_global_w)

        return current_global_w


class SLMFed_syn(BasicFed):
    """

        Synchronous FL with SLMFed.
        From: ""
                ()

    """

    def __init__(self) -> None:
        """

        Initialize the class object.

        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='SLMFed_syn',
            synchronous=True,
            min_to_start=2
        )
        loggerhear.log("Server Info  ", "Being Adopting SLMFed_syn")

    def aggregate(
            self,
            datadict: {
                'weight': list,
                'aggregate_percentage': list,
                'current_weight': list
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             weight (list): List of client model parameters for aggregation.
                             aggregate_percentage (list): Aggregate weights for each client.
                             current_weight (list): Current global model parameters.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        weight = deepcopy_list(datadict['weight'])
        aggregate_percentage = deepcopy_list(datadict['aggregate_percentage'])
        current_weight = deepcopy_list(datadict['current_weight'])
        current_global_w = SLMFedsyn(weight=weight, aggregate_percentage=aggregate_percentage,
                                     current_weight=current_weight)
        self.global_w.append(current_global_w)

        return current_global_w
