# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/23 23:38
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/25 9:27
import os
import time
from typing import List, Callable, Tuple
from numpy import ndarray
from golf_federated.client.config import Client
from golf_federated.strategy.aggregation.basic import BasicFed
from golf_federated.strategy.aggregation.synchronous import FedAVG
from golf_federated.utils.log import loggerhear
from golf_federated.utils.model import save_model, set_model_parameter, load_model_parameter, \
    get_model_parameter
from golf_federated.utils.select import softmax_prob_from_indicators
from golf_federated.utils.zip import zip_model, read_zip
from golf_federated.server.api import app
from golf_federated.utils.data import calculate_information_entropy, deepcopy_list, simple_dataset
from golf_federated.strategy.aggregation.function import fedprox_loss


class Server(object):
    """

    Server object class, the class function supports the main operation of the server.

    """

    def __init__(
            self,
            server_id: str,
            client_list: List[Client] = [],
            device: object = None
    ) -> None:
        """

        Initialize the server object.

        Args:
            server_id (str): Name of the server object.
            client_list (list): List of client objects. Default as [].
            device (object): CPU or GPU. Default as None.

        """

        # Initialize object properties.
        self.server_id = server_id
        self.client_list = deepcopy_list(client_list)
        self.aggregation = None
        self.aggregation_func = None
        self.synchronous = None
        self.model = None
        self.model_library = None
        self.maxround = 0
        self.target_acc = 0
        self.test_data = None
        self.test_label = None
        self.current_round = 0
        self.version_latest = 0
        self.client_w = dict()
        self.client_w_record = dict()
        self.client_ids = []
        self.global_w = []
        self.global_acc = []
        self.global_loss = []
        self.roundbegin_time = None
        self.aggregate_time = None
        self.currentround_cc = 0
        self.round_time = []
        self.round_cc = []
        self.round_acc = []
        self.client_num = len(self.client_list)
        self.sim_cc = False
        self.sim_zip_path = './model/'
        self.client_round_num = dict()
        self.task_name = ''
        self.url = ''
        self.port = 7788
        self.participate_num = 0
        self.preprocessing = None
        self.client_is_uploaded = dict()
        self.client_round_time = dict()
        self.client_model_upload_round = dict()
        self.global_w_file = './model/w_latest'
        self.optimizer = None
        self.loss = None
        self.metrics = []
        self.current_round_time = 0
        self.num_upload = 0
        self.convergence = 0.001
        self.device = device
        self.client_accuracy = dict()
        self.client_datasize = dict()
        self.client_IW = dict()

        # Update the connected client properties.
        for c in self.client_list:
            self.client_ids.append(c.client_id)
            self.client_round_num[c.client_id] = 0
            self.client_model_upload_round[c.client_id] = 0

    def run(
            self,
            execution_form: str,
            model: object,
            model_library: str,
            maxround: int,
            test_data: ndarray,
            test_label: ndarray,
            aggregation: BasicFed = FedAVG(),
            task_name: str = 'Default',
            url: str = '127.0.0.1',
            port: int = 7788,
            preprocessing: Callable = None,
            sim_cc: bool = False,
            sim_zip_path: str = './model/',
            target_acc: float = 0.95,
            optimizer: object = None,
            loss: object = None,
            metrics: list = ["accuracy"],
            save_model_file: bool = True,
            convergence: float = 0.001,
            torch_dataset: object = None
    ) -> None:
        """

        Start task. Support to start multiple times after defining a server object once

        Args:
            execution_form (str): Task execution form. Options are: 'StandAlone' and 'MultiDevice'.
            model (object): Define models for aggregating and evaluating.
            model_library (str): The library used to build model.
            maxround (int): Maximum number of aggregation rounds.
            test_data (numpy.ndarray): Data values for evaluation. Default as numpy.array([]).
            test_label (numpy.ndarray): Data labels for evaluation. Default as numpy.array([]).
            aggregation (golf_federated.strategy.aggregation.basic.BasicFed): Federated aggregate class object. Default as FedAVG().
            task_name (str): Name of the task. Default as 'Default'.
            url (str): Uniform Resource Locator to connect to the host. Default as '127.0.0.1'.
            port (int): Port number to connect to the host. Default as '7788'.
            preprocessing (Callable): Data preprocessing function. Default as None. Default as None.
            sim_cc (bool): Whether to simulate communication cost during stand-alone. Default as False.
            sim_zip_path (str): File save path when simulating communication cost. Default as './model/'.
            target_acc (float): Target accuracy. Default as 0.95.
            optimizer (object): If using tensorflow, model may need to extract compile, and optimizer needs to be defined in advance. Default as None.
            loss (object): If using tensorflow, model may need to extract compile, and loss function needs to be defined in advance. Default as None.
            metrics (list): Model evaluation metrics. Default as ["accuracy"].
            torch_dataset: Dataset class for pytorch.

        """

        # Initialize object properties again.
        self.execution_form = execution_form
        self.aggregation = aggregation
        self.model = model
        self.model_library = model_library
        self.maxround = maxround
        self.test_data = test_data
        self.test_label = test_label
        self.task_name = task_name
        self.url = url
        self.port = port
        self.participate_num = 0
        self.preprocessing = preprocessing
        self.sim_cc = sim_cc
        self.sim_zip_path = sim_zip_path
        self.target_acc = target_acc
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics
        self.aggregation_func = aggregation.aggregate
        self.synchronous = aggregation.synchronous
        self.current_round = 0
        self.current_round_time = 0
        self.version_latest = 0
        self.client_w = dict()
        self.global_w = []
        self.global_acc = []
        self.global_loss = []
        self.global_w_file = './model/w_latest'
        self.roundbegin_time = time.time()
        self.aggregate_time = time.time()
        self.currentround_cc = 0
        self.round_time = []
        self.round_cc = []
        self.round_acc = []
        self.client_model_upload_round = dict()
        self.client_round_time = dict()
        self.client_is_uploaded = dict()
        self.save_model_file = save_model_file
        self.currentround_acc = 0
        self.num_upload = 0
        self.convergence = convergence

        # Update the connected client properties.
        for c in self.client_list:
            self.client_round_num[c.client_id] = 0
            self.client_model_upload_round[c.client_id] = 0
            self.client_is_uploaded[c.client_id] = 0

        if (self.model_library == 'tensorflow' or self.model_library == 'keras') and self.aggregation.name == 'fedprox':
            self.model.compile(
                optimizer=self.optimizer,
                loss=fedprox_loss(model_library=self.model_library),
                metrics=self.metrics
            )
            self.file_ext = '.h5'

        elif self.model_library == 'tensorflow' or self.model_library == 'keras':
            self.model.compile(
                optimizer=self.optimizer,
                loss=self.loss,
                metrics=self.metrics
            )
            self.file_ext = '.h5'

        elif self.model_library == 'pytorch':
            # Judge whether there is a specified Dataset class, otherwise use the one defined by default.
            if torch_dataset is None:
                torch_dataset = simple_dataset
            if test_data.shape[-1] == 1:
                self.test_data = test_data.reshape(test_data.shape[0], 1, test_data.shape[1], test_data.shape[2])
            self.test_dataset = torch_dataset(data=self.test_data, label=self.test_label)
            from torch.utils.data.dataloader import DataLoader
            self.test_dataloader = DataLoader(dataset=self.test_dataset, batch_size=128)
            self.file_ext = '.pt'

        self.global_w_file = self.global_w_file + self.file_ext
        self.current_global_w = get_model_parameter(self.model, library=self.model_library)

        # Judge execution form.
        if self.execution_form == 'StandAlone':
            # Stand-alone synchronous FL.
            if self.synchronous:
                self.run_sync_stand_alone()

            # Stand-alone asynchronous FL.
            else:
                self.run_async_stand_alone()

        elif self.execution_form == 'MultiDevice':
            # Multi-device FL.
            self.run_restful(
                url=self.url,
                port=self.port
            )
        elif self.execution_form == 'OnlyValue':
            loggerhear.log('Server Info  ',
                           "Set value successfully")

        else:
            loggerhear.log("Error Message",
                           "Note that the currently optional values of type are : \n \'StandAlone\' & \'MultiDevice\'")

    def run_restful(
            self,
            url: str,
            port: int
    ) -> None:
        """

        The flask app is run directly here.
        This part will be modified after the web page is optimized.

        Args:
            url (str): Uniform Resource Locator to connect to the host.
            port (int): Port number to connect to the host.

        """

        # Configure the server into flask app and start it.
        class Config(object):
            app.config['SERVER_ID_' + self.server_id + '_' + self.task_name] = self

        app.config.from_object(Config)
        app.run(threaded=True, debug=False, host=url, port=port)

    def run_sync_stand_alone(self) -> None:
        """

        Conduct synchronous FL tasks for stand-alone simulation.

        """

        while self.current_round < self.maxround:
            # Judge whether there is a client access.
            if len(self.client_list) == 0:
                # No client access.
                loggerhear.log("Please Note  ",
                               'There is currently no client access to server.')
                continue

            else:
                self.client_round_time = dict()
                self.single_sync_stand_alone()
                self.roundbegin_time = time.time()
                # Record and aggregate collected model parameters of clients.
                aggre_dict = self.get_aggregate_datadict()
                current_global_w = self.aggregate_and_evaluate(aggre_dict)

                # Judge the result information returned after aggregation.
                if current_global_w == 'Stop':
                    # Evaluation passes, and the task ends.
                    self.current_round = self.maxround + 1
                    break

                elif current_global_w == 'Update':
                    # Update global model parameters and distribute to each client.
                    self.update_client_model()

    def run_async_stand_alone(self) -> None:
        """

        Conduct asynchronous FL tasks for stand-alone simulation.

        """

        self.reset_upload_info()
        while self.current_round < self.maxround:
            # Judge whether there is a client access.
            if len(self.client_list) == 0:
                loggerhear.log("Please Note  ",
                               'There is currently no client access to server.')
                continue

            else:
                # Simulate the asynchronous training process of each client with a loop.
                for c in self.client_list:
                    self.single_async_stand_alone(c)
                    self.client_is_uploaded[c.client_id] = 1
                    self.num_upload += 1
                    if self.num_upload >= self.aggregation.min_to_start:
                        # Aggregate collected model parameters of clients.
                        self.current_round += + 1
                        aggre_dict = self.get_aggregate_datadict()
                        current_global_w = self.aggregate_and_evaluate(aggre_dict)

                        # Judge the result information returned after aggregation.
                        if current_global_w == 'Stop':
                            # Evaluation passes, and the task ends.
                            self.current_round = self.maxround + 1
                            break

                        elif current_global_w == 'Update':
                            # Update global model parameters and distribute to each client.
                            self.update_client_model()
                        self.reset_upload_info()

    def single_sync_stand_alone(self) -> None:
        """

        Execute a round of synchronous training for stand-alone simulation.

        """

        # Initialize the parameters of the round.
        self.roundbegin_time = time.time()
        self.current_round += 1
        self.version_latest = self.current_round
        loggerhear.log('Server Info  ',
                       'Global Round %d with %d Clients to %s of %s' % (
                           self.current_round, self.client_num, self.server_id, self.task_name))
        self.current_round_time = time.time() - self.roundbegin_time

        # Simulate the training process of each client with a loop.
        for c in self.client_list:
            c_begin_time = time.time()
            c.train_direct()
            if self.sim_cc:
                self.currentround_cc += self.sim_zip_for_cc(
                    model=c.model,
                    filename='w_%s' % c.client_id,
                    library=self.model_library
                )
            self.client_w[c.client_id] = deepcopy_list(c.w_latest)
            self.client_round_num[c.client_id] += 1
            self.client_model_upload_round[c.client_id] = self.current_round
            self.client_is_uploaded[c.client_id] = 1
            self.client_round_time[c.client_id] = time.time() - c_begin_time
        self.current_round_time += max(self.client_round_time.values())

    def single_async_stand_alone(
            self,
            c: Client
    ):
        """

        Execute a round on Client c of asynchronous training for stand-alone simulation.

        Args:
            c (Client): The client performing training.

        """

        # Initialize the parameters of the round.
        self.roundbegin_time = time.time()
        c.train_direct()
        loggerhear.log('Server Info  ',
                       'Round %d on Client %s to %s of %s have finished.' % (
                           c.trained_round, c.client_id, self.server_id, self.task_name))
        if self.sim_cc:
            self.currentround_cc += self.sim_zip_for_cc(
                model=c.model,
                filename='w_%s' % c.client_id,
                library=self.model_library
            )
        self.client_w[c.client_id] = deepcopy_list(c.w_latest)
        self.client_model_upload_round[c.client_id] = self.current_round
        self.client_round_num[c.client_id] += 1
        for r in self.client_round_num.values():
            if r > self.version_latest:
                self.version_latest = r
        self.client_round_time[c.client_id] = time.time() - self.roundbegin_time

    def update_client_model(self) -> None:
        """

        Update the local model of each client with the current global model.

        """

        for c in self.client_list:
            self.update_single_client_model(c)

    def update_single_client_model(
            self,
            c: Client
    ) -> None:
        """

        Update the local model of a specific client with the current global model, which is based on server object variables or saved global model files

        Args:
            c (Client): Client that needs to update the model.

        """

        # Judge whether it is based on a saved global model file.
        if self.save_model_file:
            c.model = load_model_parameter(
                model=c.model,
                filepath=self.global_w_file,
                library=c.model_library
            )
            c.w_latest = get_model_parameter(
                model=c.model,
                library=c.model_library
            )

        else:
            c.model = self.model
            c.w_latest = deepcopy_list(self.global_w[-1])

    def get_specific_acc_info(
            self,
            acc: float
    ) -> dict:
        """

        Obtain relevant information to specified accuracy based on historical records.

        Args:
            acc (float): Specified accuracy.

        Returns:
            Dict: Information results are returned as a dictionary, including:
                    total_time (int): Total time to reach specified accuracy.
                    total_cc (int): Total communication cost to achieve specified accuracy.
                    current_acc (float): Exact accuracy value at the specified accuracy.
                    weight (dict): Global model parameters at the specified accuracy.

        """

        target_round = 0
        for i in range(self.current_round):
            if self.global_acc[i] < acc:
                continue
            else:
                target_round = i + 1
        return_dict = {
            'total_time': sum(self.round_time[0:target_round]),
            'total_cc': sum(self.round_cc[0:target_round]),
            'current_acc': self.global_acc[target_round - 1],
            'weight': self.global_w[target_round - 1]
        }

        return return_dict

    def standalone_client_participant(
            self,
            client: Client
    ) -> None:
        """

        Client access for stand-alone simulation.

        Args:
            client (golf_federated.client.config.Client): Client object to access.

        """

        # Judge whether the client has access.
        if client.client_id in self.client_ids:
            # Output information when accessed.
            loggerhear.log("Server Info  ", "%s has participated " % client.client_id)

        else:
            # Update relevant properties and information of clients when not accessed.
            self.client_list.append(client)
            self.client_ids.append(client.client_id)
            self.client_num = len(self.client_ids)
            self.client_round_num[client.client_id] = 0
            self.client_model_upload_round[client.client_id] = 0
            self.client_is_uploaded[client.client_id] = 0

    def multidevice_client_participant(
            self,
            client_id
    ) -> None:
        """

         Different from stand-alone simulation, here client only registers its id when access.

        Args:
            client_id (str): ID of client to access.

        """

        # Judge whether the client has access.
        if client_id in self.client_ids:
            # Output information when accessed.
            loggerhear.log("Server Info  ",
                           "%s has participated in %s of %s" % (client_id, self.task_name, self.server_id))

        else:
            # Update relevant properties and information of clients when not accessed.
            self.client_ids.append(client_id)
            self.client_num = len(self.client_ids)
            self.client_round_num[client_id] = 0
            self.client_model_upload_round[client_id] = 0
            self.client_is_uploaded[client_id] = 0
            self.participate_num += 1

    def eval(self) -> Tuple[float, float]:
        """

        Evaluate global model, which is run directly without Docker because it is set on server.

        Returns:
            List: Return as a list, including:
                loss (float): Loss function value.
                acc (optional): Metric value. Default as accuracy (float).

        """

        # Basic initialization.
        loggerhear.log("Server Info  ", 'Evaluating the global model of Round %d in %s of %s' % (
            self.current_round, self.task_name, self.server_id))

        # Judge the model library.
        if self.model_library == 'tensorflow' or self.model_library == 'keras':
            # Get evaluation results.
            loss, acc = self.model.evaluate(
                x=self.test_data,
                y=self.test_label,
                verbose=1
            )

        elif self.model_library == 'pytorch':
            # Get evaluation results.
            import torch
            self.model.eval()
            test_loss = 0.0
            test_acc = 0.0
            test_count = 0
            test_total = 0
            with torch.no_grad():
                for data in self.test_dataloader:
                    input = data[1].float().to(self.device)
                    label = data[0].float().to(self.device)
                    output = self.model(input)
                    if type(self.loss) == type(torch.nn.CrossEntropyLoss()):
                        label = torch.argmax(label, -1)
                    loss = self.loss(output, label)
                    test_loss += loss.item()
                    _, pre = torch.max(output.data, dim=1)
                    test_acc += (pre == label).sum().item()
                    test_total += label.size(0)
                    test_count += 1

            loss = test_loss / test_count
            acc = test_acc / test_total

        # Record evaluation results.
        self.global_loss.append(loss)
        self.global_acc.append(acc)
        loggerhear.log("Server Info  ",
                       'Round: %d -------- Global Model Test accuracy: %.2f' % (self.current_round, acc))
        self.global_acc.append(acc)

        return loss, acc

    def sim_zip_for_cc(
            self,
            model: object = None,
            filename: str = '',
            library: str = '',
            direct_through_file: bool = False,
            direct_through_file_name: str = ''
    ) -> int:
        """

        In order to simulate and calculate the communication cost during stand-alone simulation, model parameter file is saved and converted into a compressed package and then the size is calculated.

        Args:
            model (object): Model object to process.
            filename (str): Path to model parameter file.
            library (str): The library used to build model.

        Returns:
            Int: Communication cost value calculated by simulation.

        """

        # Judge whether to simulate the communication cost, otherwise return 0 directly.
        if not direct_through_file:
            if self.execution_form == 'StandAlone' or self.execution_form == 'OnlyValue':
                save_model(
                    model=model,
                    filepath=self.sim_zip_path + filename + self.file_ext,
                    library=library
                )
                zip_model(self.sim_zip_path + filename + self.file_ext, self.sim_zip_path + filename + '.zip')
        else:
            zip_model(direct_through_file_name, self.sim_zip_path + filename + '.zip')
        sim_zip_cc = len(read_zip(self.sim_zip_path + filename + '.zip'))
        os.remove(self.sim_zip_path + filename + '.zip')
        return sim_zip_cc

    def receive_and_judge(
            self,
            info_dict: dict,
            client_w: ndarray,
    ) -> str:
        """

        Receive local model parameters uploaded by clients using the RestFul API.
        And then perform a series of business processing, including partial attribute judgment, and global model aggregation and evaluation.

        Args:
            info_dict (dict): Dictionary of Infos of the uploading client.
            client_w (numpy.ndarray): Uploaded local model parameters.

        Returns:
            Str

        """

        # Initialize some properties.
        client_id = info_dict['client_id']
        if client_id not in self.client_ids:
            self.multidevice_client_participant(client_id)
        self.client_w[client_id] = deepcopy_list(client_w)
        self.client_round_num[client_id] = info_dict['trained_round']
        self.client_accuracy[client_id] = info_dict['accuracy']
        self.client_datasize[client_id] = info_dict['datasize']
        self.client_IW[client_id] = info_dict['IW']
        self.client_model_upload_round[client_id] = self.current_round
        self.client_is_uploaded[client_id] = 1

        # Judge whether the aggregation is in synchronous mode or asynchronous mode.
        if self.synchronous:
            # Synchronous mode needs to ensure that all clients upload local model parameters.
            for c in self.client_ids:
                # Judge whether all clients have uploaded.
                if self.client_is_uploaded[c] == 0:
                    # If there are clients that have not uploaded local model parameters, all clients continue to wait.
                    return 'Wait'

                else:
                    continue

        # Judge whether number of clients that have uploaded local model parameters meets the minimum limit required by the aggregation strategy.
        if self.participate_num < self.aggregation.min_to_start:
            return 'Continue'

        # Update latest version value.
        for r in self.client_round_num.values():
            if r > self.version_latest:
                self.version_latest = r

        # Start a new round of global model aggregation and evaluation.
        self.current_round += + 1

        # Judge the type of aggregation strategy, different aggregation strategies require different data input.
        aggre_dict = self.get_aggregate_datadict()

        # Aggregation and evaluation of global models.
        index = self.aggregate_and_evaluate(aggre_dict)

        # Save global model parameters
        save_model(
            model=self.model,
            filepath=self.global_w_file,
            library=self.model_library
        )

        # Update time.
        self.roundbegin_time = time.time()

        return index

    def aggregate_and_evaluate(
            self,
            datadict: dict
    ) -> str:
        """

        Aggregate and update global model.
        Save the processing result to the class object property.
        And return a string label to describe the execution.

        Args:
            datadict (dict): Data that will be input into the aggregation function, which varies by aggregation strategies.

        Returns:
            Str: A string label to describe the execution. This label will affect the behavior of the client when received.

        """

        # Record the current local model of each client before updating.
        for i in self.client_w.keys():
            self.client_w_record[i] = self.client_w[i]

        # Execute the aggregation and update of the global model.
        self.aggregate_and_update(datadict=datadict)

        # Evaluate the current global model.
        loss, acc = self.eval()

        # Simulate communication costs for stand-alone simulation.
        if self.sim_cc:
            if self.synchronous:
                self.currentround_cc += len(self.client_list) * self.sim_zip_for_cc(
                    model=self.model,
                    filename='w_latest',
                    library=self.model_library
                )
            else:
                self.currentround_cc += self.sim_zip_for_cc(
                    model=self.model,
                    filename='w_latest',
                    library=self.model_library
                )

        # Update or record some information or data.
        self.aggregate_time = time.time()
        self.round_time.append(self.aggregate_time - self.roundbegin_time + self.current_round_time)
        self.round_cc.append(self.currentround_cc)
        self.currentround_cc = 0
        self.currentround_acc = acc
        self.round_acc.append(self.currentround_acc)

        # Judge whether specified accuracy is achieved.
        if self.current_round >= 3 and self.round_acc[-1] > self.target_acc:
            # Clears attribute value of the uploaded client model parameters.
            loggerhear.log("Server Info  ", "Get target accuracy in %s of %s !" % (self.task_name, self.server_id))
            self.client_w = dict()

            # Return a stop label to notify each client that the task is over.
            label = 'Stop'
            return label

        # Judge whether the current number of rounds has reached the set maximum number of rounds.
        if self.current_round >= self.maxround:
            # Clears attribute value of the uploaded client model parameters.
            loggerhear.log("Server Info  ", "Maxround has been reached in %s of %s !" % (self.task_name, self.server_id))
            self.client_w = dict()

            # Return a stop label to notify each client that the task is over.
            label = 'Stop'
            return label

        if self.current_round >= 5 and max(self.round_acc[-5:]) - min(self.round_acc[-5:]) < self.convergence:
            # Clears attribute value of the uploaded client model parameters.
            loggerhear.log("Server Info  ", "Get target accuracy in %s of %s !" % (self.task_name, self.server_id))
            self.client_w = dict()

            # Return a stop label to notify each client that the task is over.
            label = 'Stop'
            return label

        # Reset the tag of uploaded clients.
        for c in self.client_ids:
            self.client_is_uploaded[c] = 0

        # Save the current global model.
        if self.save_model_file:
            save_model(
                model=self.model,
                filepath=self.global_w_file,
                library=self.model_library
            )

        # Clears attribute value of the uploaded client model parameters.
        self.client_w = dict()

        # Return a update label to notify each client to update model parameters.
        label = 'Update'
        return label

    def aggregate_and_update(
            self,
            datadict: dict
    ) -> None:
        """

        Execute the aggregation and update of the global model.

        Args:
            datadict (dict): Data that will be input into the aggregation function, which varies by aggregation strategies.

        """

        # Aggregate to get the current global model.
        self.current_global_w = self.aggregation_func(datadict)

        # Record the current global model.
        self.global_w.append(self.current_global_w)

        # Update model parameters
        self.model = set_model_parameter(
            model=self.model,
            w=self.current_global_w,
            library=self.model_library
        )

    def pop_client(
            self,
            client_to_pop: Client
    ) -> None:
        """

        Disconnect the specified client from the client list of this server.

        Args:
            client_to_pop (Client): The specified client object.

        """

        # Iterate through to find the specified client and disconnect.
        j = 0
        for i in range(len(self.client_list)):
            if self.client_list[j] == client_to_pop:
                self.client_list.pop(j)
                loggerhear.log("Server Info  ",
                               "Client %s is disconnected from Server %s!" % (client_to_pop.client_id, self.server_id))
            else:
                j += 1

    def update_client_list(
            self,
            client_list: List[Client]
    ) -> None:
        """

        Update the client list of the server.

        Args:
            client_list (List[Client]): Updated client list.

        """

        # Update client list and related variables.
        self.client_list = deepcopy_list(client_list)
        self.client_ids = []
        self.client_round_num = dict()
        self.client_model_upload_round = dict()
        for c in self.client_list:
            self.client_ids.append(c.client_id)
            self.client_round_num[c.client_id] = 0
            self.client_model_upload_round[c.client_id] = 0
        loggerhear.log("Server Info  ", "Server %s has updated the client list!" % self.server_id)

    def get_aggregate_datadict(self) -> dict:
        """

        Create a data dictionary for function input based on different aggregation methods.

        Returns:
            Dict: Data dictionary as input to aggregation functions.

        """

        # Judge the aggregation strategy name and get the different data dictionary.
        if self.aggregation.name == 'fedavg' or self.aggregation.name == 'fedprox':
            # Get the list of model parameters and dataset size of each client.
            weight_l = []
            data_size_l = []
            for c_id in self.client_ids:
                weight_l.append(self.client_w[c_id])
                if c_id in self.client_datasize.keys():
                    data_size_l.append(self.client_datasize[c_id])
                else:
                    for c in self.client_list:
                        if c.client_id == c_id:
                            data_size_l.append(c.datasize)
            aggre_dict = {'weight': weight_l, 'data_size': data_size_l}
            loggerhear.log("Server Info  ", "Get the data dictionary of %s." % self.aggregation.name)


        elif self.aggregation.name == 'fedfd':
            # Get the ID, model parameters, number of trained rounds of each client
            # and the current version number of the server.
            aggre_dict = {
                'client_id': self.client_ids,
                'weight': self.client_w,
                'client_round': self.client_round_num,
                'version_latest': self.version_latest,
            }
            loggerhear.log("Server Info  ", "Get the data dictionary of %s." % self.aggregation.name)

        elif self.aggregation.name == 'SLMFed_syn':
            # Get the model parameters, aggregation weights of each client
            # and the current global model parameters of the server.
            current_client_w = [self.client_w[c.client_id] for c in self.client_list]
            client_information_richness = [calculate_information_entropy(c.train_label) for c in
                                           self.client_list]
            client_datasize_list = [c.datasize for c in self.client_list]
            aggregate_percentage = softmax_prob_from_indicators([client_information_richness, client_datasize_list])
            aggre_dict = {
                'weight': current_client_w,
                'aggregate_percentage': aggregate_percentage,
                'current_weight': self.current_global_w
            }
            loggerhear.log("Server Info  ", "Get the data dictionary of %s." % self.aggregation.name)

        elif self.aggregation.name == 'SLMFed_asyn':
            # Get the ID, model parameters, aggregation weights of uploaded clients
            # and current global model parameters, accuracy of the server
            # and target accuracy of the task.
            upload_client_id = []
            aggregate_percentage_dict = dict()
            client_information_richness = [calculate_information_entropy(c.train_label) for c in
                                           self.client_list]
            client_datasize_list = [c.datasize for c in self.client_list]
            aggregate_percentage = softmax_prob_from_indicators([client_information_richness, client_datasize_list])
            for i in range(len(self.client_list)):
                c = self.client_list[i]
                aggregate_percentage_dict[c.client_id] = aggregate_percentage[i]

                if self.client_is_uploaded[c.client_id] == 1:
                    upload_client_id.append(c.client_id)
            if len(self.global_acc) > 0:
                current_acc = self.global_acc[-1]
            else:
                current_acc = 0
            aggre_dict = {
                'client_id': upload_client_id,
                'weight': self.client_w_record,
                'aggregate_percentage': aggregate_percentage_dict,
                'current_weight': self.current_global_w,
                'current_acc': current_acc,
                'target_acc': self.target_acc
            }
            loggerhear.log("Server Info  ", "Get the data dictionary of %s." % self.aggregation.name)

        elif self.aggregation.name == 'fedasync':
            # Get the ID, model parameters, and number of rounds of the corresponding global model of uploaded clients
            # and current global model parameters and number of rounds of the server.
            upload_client_id = []
            upload_client_weight = dict()
            upload_client_round = dict()
            for c_id in self.client_ids:
                if self.client_is_uploaded[c_id] == 1:
                    upload_client_id.append(c_id)
                    upload_client_weight[c_id] = self.client_w[c_id]
                    upload_client_round[c_id] = self.client_model_upload_round[c.client_id]
            aggre_dict = {
                'client_id': upload_client_id,
                'weight': upload_client_weight,
                'current_weight': self.current_global_w,
                'current_round': self.current_round,
                'client_round': upload_client_round
            }
            loggerhear.log("Server Info  ", "Get the data dictionary of %s." % self.aggregation.name)

        else:
            # For undeployed aggregation strategies, an empty dictionary is returned and relevant information is prompted.
            aggre_dict = {}
            loggerhear.log("Please Note  ",
                           "%s is not supported at the moment and will return an empty dictionary." % self.aggregation.name)

        return aggre_dict

    def reset_upload_info(self) -> None:
        """

        Reset upload records for all clients.

        """

        self.num_upload = 0
        for c_ in self.client_list:
            self.client_is_uploaded[c_.client_id] = 0
        loggerhear.log("Server Info  ",
                       "Server %s resets the upload records of all connected clients." % self.server_id)
