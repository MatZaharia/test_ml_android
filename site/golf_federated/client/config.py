# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/22 20:08
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/19 17:18

import os
import random
import threading
import time
import zipfile
from typing import Callable, Tuple, Any
import numpy as np
import requests
from sseclient import SSEClient
from golf_federated.utils.data import calculate_IW, deepcopy_list, simple_dataset
from golf_federated.utils.log import loggerhear
from golf_federated.utils.model import load_model_parameter, get_model_parameter, set_model_parameter, \
    save_model
from golf_federated.strategy.aggregation.function import fedprox_loss


class Client(object):
    """

    Client object class, the class function supports the main operation of the client.

    """

    def __init__(
            self,
            client_id: str,
            train_data: np.ndarray,
            train_label: np.ndarray,
            model_library: str,
            w_file_initial: str = None,
            model: object = None,
            optimizer: object = None,
            loss: object = None,
            batch_size: int = 1,
            train_epoch: int = 1,
            preprocessing: Callable = None,
            client_test: bool = False,
            test_data: np.ndarray = np.array([]),
            test_label: np.ndarray = np.array([]),
            metrics: list = ["accuracy"],
            client_cal: bool = False,
            cal_data: np.ndarray = np.array([]),
            docker_name: str = '',
            incremental: bool = False,
            initial_rate: float = 0.5,
            cal_IW: bool = False,
            is_prox: bool = False,
            prox_miu=1,
            learning_rate: float = 0.1,
            torch_dataset: object = None,
            device: object = None
    ) -> None:
        """

        Initialize the client object.

        Args:
            client_id (str): Name of the client object.
            train_data (numpy.ndarray): Data values for training.
            train_label (numpy.ndarray): Data labels for training.
            model_library (str): The library used to build model used for training, evaluation or computation.
            w_file_initial (str): Path to store the initialization model parameters file.
            model (object): If model training, evaluation, calculation and other processes are conducted directly without using Docker, model needs to be defined in advance. Default as None.
            optimizer (object): If model training, evaluation, calculation and other processes are conducted directly without using Docker, optimizer needs to be defined in advance. Default as None.
            loss (object): If model training, evaluation, calculation and other processes are conducted directly without using Docker, loss function needs to be defined in advance. Default as None.
            batch_size (int): Number of samples for a single input to the model. Default as 1.
            train_epoch (int): Number of epochs for a single training process of client. Default as 1.
            preprocessing (Callable): Data preprocessing function. Default as None.
            client_test (bool): Whether client conducts local model evaluation. Default as False.
            test_data (numpy.ndarray): Data values for evaluation. Default as numpy.array([]).
            test_label (numpy.ndarray): Data labels for evaluation. Default as numpy.array([]).
            metrics (list): Model evaluation metrics. Default as ["accuracy"].
            client_cal (bool): Whether client conducts local model calculation. Default as False.
            cal_data (numpy.ndarray): Data values for calculation. Default as numpy.array([]).
            docker_name (str): Name of Docker image. Default as ''.
            incremental (bool): Whether this client performs data increment. Note that the incremental data here is mainly based on the client's total data, while users can also add new data in the process. Default as False.
            initial_rate (float): Percentage of initial data to total data. Default as 0.5.
            cal_IW (bool): Whether to calculate the information weighted value. Default as False.
            is_prox (bool): Whether the aggregation algorithm is FedProx. Default as False.
            prox_miu (float): Parameters of the FedProx. Default as 1.
            learning_rate (float): Learning rate of the optimizer. Default as 0.1.
            torch_dataset (object): Dataset class for pytorch. Default as None.
            device (object): CPU or GPU. Default as None.

        """

        # Initialize object properties.
        self.client_id = client_id
        self.total_train_data = train_data
        self.total_train_label = train_label
        self.total_shape = self.total_train_data.shape[0]
        if incremental:
            # Initial data is intercepted in part by default in the order of the overall data.
            initial_part = int(initial_rate * self.total_shape)
            self.increment_train_data = self.total_train_data[0:initial_part]
            self.train_data = self.total_train_data[0:initial_part]
            self.increment_train_label = self.total_train_label[0:initial_part]
            self.train_label = self.total_train_label[0:initial_part]
            self.new_data = []
            self.new_label = []
        else:
            self.train_data = train_data
            self.train_label = train_label
        self.round_increment = False
        self.model_library = model_library
        if w_file_initial is None:
            self.model = model
        else:
            self.model = load_model_parameter(
                model=model,
                filepath=w_file_initial,
                library=self.model_library
            )
        self.w_initial = get_model_parameter(
            model=self.model,
            library=self.model_library,
        )
        self.optimizer = optimizer
        self.loss = loss
        self.batch_size = batch_size
        self.train_epoch = train_epoch
        self.preprocessing = preprocessing
        self.client_test = client_test
        self.test_data = test_data
        self.test_label = test_label
        self.metrics = metrics
        self.client_cal = client_cal
        self.cal_data = cal_data
        self.docker_name = docker_name
        self.is_prox = is_prox
        self.prox_miu = prox_miu
        self.learning_rate = learning_rate
        self.device = device

        # Calculate metrics for evaluating client data.
        self.datasize = self.train_data.shape[0]
        if cal_IW:
            self.IW = calculate_IW(self.train_label)
        else:
            self.IW = 0.0

        # Initialize training related parameters.
        self.can_train = True
        self.stop_train = False
        self.w_latest = deepcopy_list(self.w_initial)
        self.trained_round = 0
        self.allloss = []
        self.allacc = []
        self.docker_first = True
        self.docker_change = False

        # Data preprocessing.
        if self.preprocessing is not None:
            self.train_data, self.train_label, self.test_data, self.test_label = self.preprocessing(self.train_data,
                                                                                                    self.train_label,
                                                                                                    self.test_data,
                                                                                                    self.test_label)

        if (self.model_library == 'tensorflow' or self.model_library == 'keras') and self.is_prox:
            self.model.compile(optimizer=self.optimizer,
                               loss=fedprox_loss(model_library=self.model_library, w_global=self.w_latest,
                                                 w_local=get_model_parameter(
                                                     model=self.model,
                                                     library=self.model_library
                                                 ), miu=self.prox_miu), metrics=self.metrics)
            self.file_ext = '.h5'

        elif self.model is not None and \
                self.optimizer is not None and \
                self.loss is not None and \
                (self.model_library == 'tensorflow' or self.model_library == 'keras'):
            self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.metrics)
            self.file_ext = '.h5'

        elif self.model_library == 'pytorch':
            # Judge whether there is a specified Dataset class, otherwise use the one defined by default.
            if torch_dataset is None:
                torch_dataset = simple_dataset
            if train_data.shape[-1] == 1:
                self.train_data = train_data.reshape(train_data.shape[0], 1, train_data.shape[1], train_data.shape[2])
            if test_data.shape[-1] == 1:
                self.test_data = test_data.reshape(test_data.shape[0], 1, test_data.shape[1], test_data.shape[2])
            self.train_dataset = torch_dataset(data=self.train_data, label=self.train_label)
            self.test_dataset = torch_dataset(data=self.test_data, label=self.test_label)
            from torch.utils.data.dataloader import DataLoader
            self.train_dataloader = DataLoader(dataset=self.train_dataset, batch_size=batch_size)
            self.test_dataloader = DataLoader(dataset=self.test_dataset, batch_size=batch_size)
            self.file_ext = '.pt'

    def train_direct(self) -> bool:
        """

        Directly perform model training.

        """

        # Basic initialization.
        self.trained_round += 1
        loggerhear.log("Client Info  ", 'Training round %d on %s' % (self.trained_round, self.client_id))

        # Judge the model library.
        if self.model_library == 'tensorflow' or self.model_library == 'keras':

            # Update client model parameters.
            self.model = set_model_parameter(
                model=self.model,
                w=self.w_latest,
                library=self.model_library
            )
            if self.is_prox:
                self.model.compile(optimizer=self.optimizer,
                                   loss=fedprox_loss(model_library=self.model_library, w_global=self.w_latest,
                                                     w_local=get_model_parameter(
                                                         model=self.model,
                                                         library=self.model_library
                                                     ), miu=self.prox_miu), metrics=self.metrics)

            # Client model training.
            self.model.fit(
                self.train_data,
                self.train_label,
                batch_size=self.batch_size,
                epochs=self.train_epoch,
                verbose=1
            )

            # Get latest model parameters after training.
            self.w_latest = get_model_parameter(
                model=self.model,
                library=self.model_library
            )

        elif self.model_library == 'pytorch':
            import torch
            # Update client model parameters.
            self.model = set_model_parameter(
                model=self.model,
                w=self.w_latest,
                library=self.model_library
            )

            # Switch mode of model.
            self.model.train()

            # Client model training.
            for epoch in range(self.train_epoch):
                training_loss = 0.0
                training_acc = 0.0
                training_count = 0
                training_total = 0
                for data in self.train_dataloader:
                    input = data[1].float().to(self.device)
                    label = data[0].float().to(self.device)
                    self.optimizer.zero_grad()

                    output = self.model(input)
                    if type(self.loss) == type(torch.nn.CrossEntropyLoss()):
                        label = torch.argmax(label, -1)
                    loss = self.loss(output, label.long())
                    loss.backward()
                    self.optimizer.step()
                    training_loss += loss.item()
                    _, pre = torch.max(output.data, dim=1)
                    training_acc += (pre == label).sum().item()
                    training_count += 1
                    training_total += label.shape[0]

                loggerhear.log("Client Info  ", 'Epoch [%d/%d]:    Loss: %.4f       Accuracy: %.2f' % (
                    epoch, self.train_epoch, training_loss / training_count, training_acc / training_total * 100))

            # Get latest model parameters after training.
            self.w_latest = get_model_parameter(
                model=self.model,
                library=self.model_library
            )

    def eval_direct(self, data=None, label=None) -> Tuple[float, Any]:
        """

        Directly perform model evaluation.

        Returns:
            List: Return as a list, including:
                loss (float): Loss function value.
                acc (Optional): Metric value. Default as accuracy (float).

        """

        # Basic initialization.
        loggerhear.log("Client Info  ",
                       'Evaluating the model of round %d on %s' % (self.trained_round, self.client_id))

        # Judge whether there is data for evaluation, otherwise use training data for evaluation.
        if data is None or label is None:
            if self.client_test:
                x = self.test_data
                y = self.test_label

            else:
                x = self.train_data
                y = self.train_label
        else:
            x = data
            y = label

        # Judge the model library.
        if self.model_library == 'tensorflow' or self.model_library == 'keras':
            # Get evaluation results.
            loss, acc = self.model.evaluate(
                x=x,
                y=y,
                verbose=1
            )

        elif self.model_library == 'pytorch':

            import torch

            # Switch mode of model.
            self.model.eval()

            # Get evaluation results.
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
                    loss = self.loss(output, label.long())
                    test_loss += loss.item()
                    _, pre = torch.max(output.data, dim=1)
                    test_acc += (pre == label).sum().item()
                    test_total += label.size(0)
                    test_count += 1

            loss = test_loss / test_count
            acc = test_acc / test_total

        # Record evaluation results.
        self.allloss.append(loss)
        self.allacc.append(acc)

        return loss, acc

    def cal_direct(self) -> np.ndarray:
        """

        Directly perform model calculation.

        Returns:
            Numpy.ndarray: Model calculation results.

        """

        # Basic initialization.
        cal_result = np.array([])
        loggerhear.log("Client Info  ",
                       'Calculating the model result on %s' % self.client_id)

        # Judge the model library.
        if self.model_library == 'tensorflow' or self.model_library == 'keras':
            # Get calculation results.
            cal_result = self.model.predict(
                self.cal_data
            )

        elif self.model_library == 'pytorch':
            # Get calculation results.
            import torch
            cal_result = np.array()
            with torch.no_grad():
                for data in self.test_dataloader:
                    input = data[1].float().to(self.device)
                    output = self.model(input)
                    cal_result = np.concatenate(cal_result, output)

        return cal_result

    def train_and_eval_by_docker(
            self,
            url: str,
            port: str,
            docker_port: str
    ) -> Tuple[float, Any]:
        """

        Model training and evaluation with Docker.

        Args:
            url (str): Uniform Resource Locator to connect to the host.
            port (str): Port number to connect to the host.
            docker_port (str): Port mapping inside the container.

        Returns:
            List: Return as a list, including:
                loss (float): Loss function value.
                acc (optional): Metric value. Default as accuracy (float).

        """

        # Basic initialization.
        self.trained_round += 1
        loggerhear.log("Client Info  ",
                       'Training and Evaluating round %d on %s with Docker' % (self.trained_round, self.client_id))

        # Judge whether the container is deployed for the first time or the container has changed.
        if self.docker_first or self.docker_change:
            # Request to download the Docker image.
            r = requests.post("http://" + url + ":" + str(port) + "/api/image_download/image.tar")
            b = r.content
            binfile_last = open('./client/image.tar', 'wb')
            binfile_last.write(b)
            binfile_last.close()

            # Load the Docker image.
            os.system('docker load -i ./client/image.tar')

            # Run the Docker container.
            port=str(port)
            docker_port=str(docker_port)
            os.system(
                'docker run --network=bridge -p %s:%s  -dit --name docker_%s %s' % (
                    docker_port, docker_port, self.client_id, self.docker_name))

            # Save relevant data to temporary files.
            np.save('./client/'+self.client_id+'_train_data.npy', self.train_data)
            np.save('./client/'+self.client_id+'_train_label.npy', self.train_label)
            np.save('./client/'+self.client_id+'_test_data.npy', self.test_data)
            np.save('./client/'+self.client_id+'_test_label.npy', self.test_label)

            # Transfer relevant data into the container.
            os.system('docker cp ./client/'+self.client_id+'_train_data.npy docker_'+self.client_id+':/train_data.npy')
            os.system('docker cp ./client/'+self.client_id+'_train_label.npy docker_'+self.client_id+':/train_label.npy')
            os.system('docker cp ./client/'+self.client_id+'_test_data.npy docker_'+self.client_id+':/test_data.npy' )
            os.system('docker cp ./client/'+self.client_id+'_test_label.npy docker_'+self.client_id+':/test_label.npy' )

            # Delete temporary files.
            os.remove('./client/'+self.client_id+'_train_data.npy')
            os.remove('./client/'+self.client_id+'_train_label.npy')
            os.remove('./client/'+self.client_id+'_test_data.npy')
            os.remove('./client/'+self.client_id+'_test_label.npy')

            # Modify parameters.
            self.docker_first = False
            self.docker_change = False

        # Transfer model parameters file into the container.
        os.system('docker cp ./client/global_model%s docker_%s:/' % (self.file_ext, self.client_id))

        # Perform model training and evaluation.
        os.system(
            'docker exec docker_%s python train.py --w_download=%s --train_data=%s --train_label=%s --batch_size=%d '
            '--train_epoch=%d --w_upload=%s --is_train=%s --eval_data=%s --eval_label=%s --eval_result=%s '
            '--is_eval=%s' % (
                self.client_id, './global_model' + self.file_ext, './train_data.npy', './train_label.npy',
                self.batch_size,
                self.train_epoch, './w_up' + self.file_ext, str(True),
                './test_data.npy', './test_label.npy', './eval_result.npy', str(self.client_test)))

        # Export model evaluation results.
        os.system('docker cp  docker_'+self.client_id+':/eval_result.npy ./client/'+self.client_id+'_eval_result.npy')

        # Load and read model evaluation results.
        eval = np.load('./client/'+self.client_id+'_eval_result.npy', allow_pickle=True).item()
        loss = eval['loss']
        acc = eval['acc']

        # Record model evaluation results.
        self.allloss.append(loss)
        self.allacc.append(acc)

        # Export the trained model parameter file and save it to the specified file.
        os.system('docker cp  docker_%s:/w_up%s ./client/%s%s' % (
            self.client_id, self.file_ext, self.client_id, self.file_ext))

        return loss, acc

    def monitor(
            self,
            thread_name: str,
            url: str,
            port: int
    ) -> None:
        """

        Create an information channel and listen to server pushes.

        Args:
            thread_name (str): Child thread name.
            url (str): Uniform Resource Locator to connect to the host.
            port (int): Port number to connect to the host.

        """

        # Define the thread running process function.
        def run_in_thread() -> None:
            """

            Child thread receives the information pushed by SSE(Server-Sent Events) client.

            """

            # Receive information.
            messages = SSEClient("http://" + url + ":" + str(port) + "/api/stream")
            for msg in messages:
                # Judge information content.
                if msg.data == str(b'Update'):
                    # Pause training.
                    # Start training again after receiving and updating local model parameters.
                    self.can_train = False
                    loggerhear.log("Client Info  ", "Global updating on %s!" % self.client_id)
                    r = requests.post(
                        "http://" + url + ":" + str(port) + "/api/model_download/w_latest" + self.file_ext)
                    b = r.content
                    binfile_last = open('./client/global_model' + self.file_ext, 'wb')
                    binfile_last.write(b)
                    binfile_last.close()
                    self.model = load_model_parameter(
                        model=self.model,
                        filepath='./client/global_model' + self.file_ext,
                        library=self.model_library
                    )
                    self.can_train = True

                elif msg.data == str(b'Wait'):
                    # Pause training.
                    self.can_train = False
                    loggerhear.log("Client Info  ", "Client %s is waiting for other clients!" % self.client_id)

                elif msg.data == str(b'Continue'):
                    # Continue training.
                    self.can_train = True

                elif msg.data == str(b'Stop'):
                    # Stop training.
                    loggerhear.log("Client Info  ", "Stop training on %s!" % self.client_id)
                    self.stop_train = True

        # Define the thread running process class.
        class ChildThread(threading.Thread):
            def __init__(
                    self,
                    name: str
            ) -> None:
                """

                Initialize child thread class object.

                Args:
                    name:Child thread name.

                """

                threading.Thread.__init__(self)
                self.name = name

            def run(self) -> None:
                """

                Run the process of child thread.

                """

                run_in_thread()

        # Start child thread
        ChildThread(thread_name).start()

    def runtask(
            self,
            url: str,
            port: str,
            server_id: str = '',
            task_name: str = '',
            is_docker: bool = False,
            docker_port: str = 7788
    ) -> None:
        """

        Perform client tasks, mainly including model training, evaluation, and related data and file exchange.

        Args:
            url (str): Uniform Resource Locator to connect to the host.
            port (str): Port number to connect to the host.
            server_id (str): Name of server to which the task belongs. Default as ''
            task_name (str): Name of the task. Default as ''
            is_docker (bool): Whether to use Docker to perform model training and evaluation. Default as False.
            docker_port (str): Port mapping inside the container. Default as '7788'.

        """

        # Keep running until stop message is received.
        while not self.stop_train:
            # Judge to run process or pause.
            if self.can_train:
                # Judge whether to use Docker.
                if is_docker:
                    # Model training and evaluation.
                    score = self.train_and_eval_by_docker(url, port, docker_port)

                    # Model evaluation results.
                    accuracy = round(score[1], 2)

                else:
                    # Model training.
                    self.train_direct()

                    # Model evaluation and its results.
                    score = self.eval_direct()
                    accuracy = round(score[1], 2)

                    # Save model parameter file to the specified file.
                    save_model(
                        model=self.model,
                        filepath='client/'
                                 + str(self.client_id)
                                 + self.file_ext,
                        library=self.model_library
                    )

                # Info dictionary.
                info_dict = {
                    'client_id':self.client_id,
                    'accuracy': accuracy,
                    'datasize': self.datasize,
                    'IW': self.IW,
                    'trained_round': self.trained_round,
                    'model_library': self.model_library
                }
                np.save('client/'+str(self.client_id)+'_dict.npy', info_dict)

                # Compress model parameter file.
                first_model_zipper = zipfile.ZipFile('client/commit_' + str(self.client_id) + '.zip', 'w',
                                                     compression=zipfile.ZIP_DEFLATED)
                first_model_zipper.write(
                    filename='client/'
                             + str(self.client_id)
                             + self.file_ext,
                    arcname=str(self.client_id) + self.file_ext
                )
                first_model_zipper.write(
                    filename='client/'
                             + str(self.client_id)
                             +'_dict.npy',
                    arcname=str(self.client_id)+'_dict.npy'
                )
                first_model_zipper.close()

                # Binary transfer to server host.
                binfile_first = open('client/commit_' + str(self.client_id) + '.zip', 'rb')
                bin_infomation = binfile_first.read()
                binfile_first.close()
                r = requests.post(
                    "http://" + url + ":" + str(port) + "/api/ReceiveLocalModel",
                    data=bin_infomation,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                ).content

                # Currently, database is not used to query task corresponding to the specific server name and task name.
                # I.e., only a single task is supported.
                # This will be adjusted in subsequent versions. The example is as follows
                # r = requests.post(
                #     "http://" + url + ":" + str(port) + "/api/ReceiveLocalModel",
                #     data={
                #         'aggregation_data': bin_infomation,
                #         'server_id': server_id,
                #         'task_name': task_name
                #     },
                #     headers={"Content-Type": "application/x-www-form-urlencoded"}
                # ).content

                # Judge the response
                if r == b'Stop':
                    # Stop the task.
                    # Delete the container if using Docker.
                    if is_docker:
                        while not (os.popen('docker ps -f name=docker_%s'% self.client_id).read().split('\n')[1])=='':
                            loggerhear.log("Client Info  ",
                                               'Docker container docker_%s being deleting' % (
                                               self.client_id))
                            os.system('docker rm docker_%s -f' % self.client_id)
                        exit(0)
                    break

                elif r == b'Wait':
                    # Pause the task.
                    self.can_train = False

                else:
                    # Continue the task.
                    continue
            else:
                # Continue the task.
                continue

    def data_increment(
            self,
            min_perc: float,
            max_perc: float,
            prob: float
    ) -> None:
        """

        Generate incremental data based on the specified probability and percentage interval.
        Note that the incremental data is not updated to the client here (the function update_client_increment_data needs to be called).

        Args:
            min_perc (float): Lower bound for data increment percentage.
            max_perc (float): Upper bound for data increment percentage.
            prob (float): Probability of performing data increment.

        """

        # Judge whether to perform data increment
        if random.random() < prob:
            # Get a random percentage of data increment.
            percent_new = random.uniform(min_perc, max_perc)

            # Get incremental content and update variables.
            num_new = int(percent_new * self.total_shape)
            index_all = [i for i in range(self.total_shape)]
            index_new = np.random.choice(index_all, size=num_new, replace=False)
            data_new = self.total_train_data[index_new]
            label_new = self.total_train_label[index_new]
            if len(self.new_data) == 0:
                self.new_data = np.array(data_new)
                self.new_label = np.array(label_new)
            else:
                self.new_data = np.concatenate((self.new_data, data_new))
                self.new_label = np.concatenate((self.new_label, label_new))
            self.increment_train_data = np.concatenate((self.increment_train_data, data_new))
            self.increment_train_label = np.concatenate((self.increment_train_label, label_new))
            self.round_increment = True
            loggerhear.log("Client Info  ",
                           "%.2f%% data increment performed on Client %s." % (percent_new * 100, self.client_id))

    def choose_layer(
            self,
            prob_list: list
    ) -> list:
        """

        Get the model parameter and set some of the layers to None based on the specified probability, i.e. some layers are not uploaded.

        Args:
            prob_list (list): Probability list, which corresponds to the parameter layers individually.

        Returns:
            List: Model parameters after adjustment.

        """

        # Deep copy to create a temporary variable.
        return_w = deepcopy_list(self.w_latest)

        # Set some layers to None based on established rules
        temp = True
        for i in range(len(return_w)):
            if prob_list[i] == 999:
                if not temp:
                    return_w[i] = None
            else:
                p = random.random()
                if p > prob_list[i]:
                    return_w[i] = None
                    temp = False
                else:
                    temp = True
        loggerhear.log("Client Info  ",
                       "Adjustment of the model parameter layer on Client %s is completed." % self.client_id)

        return return_w

    def update_client_increment_data(self) -> None:
        """

        Update incremental content to training content.

        """

        self.train_data = self.increment_train_data
        self.train_label = self.increment_train_label
        self.datasize = self.increment_train_label.shape[0]
        self.new_data = []
        self.new_label = []
        loggerhear.log("Client Info  ",
                       "Incremental content is updated to training content on Client %s." % self.client_id)
