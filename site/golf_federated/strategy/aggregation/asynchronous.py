# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/24 13:35
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/20 14:09
from golf_federated.strategy.aggregation.basic import BasicFed
from golf_federated.strategy.aggregation.function import fedfd, SLMFedasyn, fedasync
from golf_federated.utils.data import deepcopy_list
from golf_federated.utils.log import loggerhear


class FedFD(BasicFed):
    """

    Asynchronous FL with FedFD.

    """

    def __init__(self) -> None:
        """

        Initialize the class object.

        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='fedfd',
            synchronous=False,
            min_to_start=2
        )
        loggerhear.log("Server Info  ", "Being Adopting FedFD")

    def aggregate(
            self,
            datadict: {
                'client_id': list,
                'weight': dict,
                'client_round': dict,
                'version_latest': int
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             'client_id' (list): ID of clients that upload the models.
                             'weight' (dict): Corresponding dictionary of client IDs and models to aggregate.
                             'client_round' (dict): Corresponding dictionary of client IDs and number of training rounds for local models.
                             'version_latest' (int): Latest model version.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        client_id = deepcopy_list(datadict['client_id'])
        weight = datadict['weight']
        client_round = datadict['client_round']
        version_latest = datadict['version_latest']
        current_global_w = fedfd(
            client_id=client_id,
            weight=weight,
            client_round=client_round,
            version_latest=version_latest
        )
        self.global_w.append(current_global_w)

        return current_global_w


class FedAsync(BasicFed):
    """

        Asynchronous FL with FedAsync.
        From: "Asynchronous Federated Optimization"
                (https://opt-ml.org/oldopt/papers/2020/paper_28.pdf)

    """

    def __init__(
            self,
            alpha: float = 0.5,
            beta: float = 0.0,
            staleness: str = 'Polynomial'
    ) -> None:
        """

        Initialize the class object.

        Args:
            alpha (float): Corresponds to the parameter α defined in FedAsync.
            beta (float): Corresponds to the parameter β defined in FedAsync.
            staleness (str): Corresponds to the name of the function defined in FedAsync.

        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='fedasync',
            synchronous=False,
            min_to_start=5
        )
        self.alpha = alpha
        self.beta = beta
        self.staleness = staleness
        loggerhear.log("Server Info  ", "Being Adopting FedAsync")

    def aggregate(
            self,
            datadict: {
                'client_id': list,
                'weight': dict,
                'current_weight': list,
                'current_round': int,
                'client_round': dict
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             'client_id' (list): List of client IDs for aggregation.
                             'weight' (dict): Dictionary of client model parameters for aggregation.
                             'current_weight' (list): Current global model parameters.
                             'current_round' (int): Number of current training round.
                             'client_round' (dict): Number of global round corresponding to the model trained by each client.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        client_id = deepcopy_list(datadict['client_id'])
        weight = datadict['weight']
        current_weight = deepcopy_list(datadict['current_weight'])
        current_round = datadict['current_round']
        client_round = datadict['client_round']
        current_global_w = fedasync(
            client_id=client_id,
            weight=weight,
            staleness=self.staleness,
            current_weight=current_weight,
            current_round=current_round,
            client_round=client_round,
            alpha=self.alpha,
            beta=self.beta
        )
        self.global_w.append(current_global_w)

        return current_global_w


class SLMFed_asyn(BasicFed):
    """

        Asynchronous FL with SLMFed.
        From: ""
                ()

    """

    def __init__(
            self,
            func: str = 'other'
    ) -> None:
        """
        
        Initialize the class object.
                
        Args:
            func (str):  Function to adjust aggregation weights. Default as 'other'.
            
        """

        # Inherit parent class and initialize object properties.
        super().__init__(
            name='SLMFed_asyn',
            synchronous=False,
            min_to_start=1
        )
        self.func = func
        loggerhear.log("Server Info  ", "Being Adopting SLMFed_asyn")

    def aggregate(
            self,
            datadict: {
                'client_id': list,
                'weight': dict,
                'aggregate_percentage': dict,
                'current_weight': list,
                'current_acc': float,
                'target_acc': float
            }
    ) -> list:
        """

        Perform model aggregation.

        Args:
            datadict (dict): Data that will be input into the aggregation function, including:
                             'client_id' (list): List of client IDs for aggregation.
                             'weight' (dict): Dictionary of client model parameters for aggregation.
                             'aggregate_percentage' (dict): Aggregate weights for each client.
                             'current_weight' (list): Current global model parameters.
                             'current_acc' (float): Current accuracy corresponding to the global model.
                             'target_acc' (float): Target accuracy of the task.

        Returns:
            List: The model generated after aggregation. And use a list to store the parameters of different layers.

        """

        client_id = deepcopy_list(datadict['client_id'])
        weight = datadict['weight']
        aggregate_percentage = datadict['aggregate_percentage']
        current_weight = deepcopy_list(datadict['current_weight'])
        current_acc = datadict['current_acc']
        target_acc = datadict['target_acc']
        current_global_w = SLMFedasyn(
            client_id=client_id,
            weight=weight,
            aggregate_percentage=aggregate_percentage,
            current_weight=current_weight,
            current_acc=current_acc,
            func=self.func,
            target_acc=target_acc
        )
        self.global_w.append(current_global_w)

        return current_global_w
