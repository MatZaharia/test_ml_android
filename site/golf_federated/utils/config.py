# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/6/4 23:28
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/25 15:26

import warnings
from golf_federated.utils.log import loggerhear

warnings.filterwarnings("ignore", category=Warning)

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import importlib
import sys
from golf_federated.client.config import Client
from golf_federated.data.dataset import CustomFederatedDataset
from golf_federated.server.config import Server
import golf_federated
import yaml


def load_yaml_config(file: str) -> None:
    """

    Get the configuration and start by reading the yaml file.
    Leave empty value for unused fields when modifying yaml file.

    Args:
        file (str): Path where the yaml file is stored

    """

    loggerhear.log("Common Info  ", 'Loading Config from %s' % file)

    # Open yaml file and extract the corresponding data values of some fields.
    file = open(file, 'r', encoding="utf-8")
    content = yaml.load(file)
    data_content = content['data']
    model_content = content['model']

    # Create a federated dataset object.
    fl_data = CustomFederatedDataset(
        train_data=data_content['x_train'],
        train_label=data_content['y_train'],
        test_data=data_content['x_test'],
        test_label=data_content['y_test'],
        part_num=data_content['part_num'],
        part_id=data_content['client_id'],
        split_data=data_content['split_data'],
    )

    # Define model.
    sys.path.append(model_content['filepath'])
    module = importlib.import_module(model_content['module'])
    m = getattr(module, model_content['function'])
    model = m()

    # Judge the model library, define the optimizer and loss function.
    if model_content['model_library'] == 'tensorflow' or model_content['model_library'] == 'keras':
        import tensorflow as tf
        optimizer = getattr(tf.keras.optimizers, model_content['optimizer'])(
            learning_rate=model_content['learning_rate'])
        loss = getattr(tf.keras.losses, model_content['loss'])()
    elif model_content['model_library'] == 'pytorch':
        import torch
        optimizer = getattr(torch.optim, model_content['optimizer'])(
            lr=model_content['learning_rate'])
        loss = getattr(torch.nn, model_content['loss'])()

    # Read data from device-related fields, create server and client objects.
    device_data = content['device']
    have_server = False
    client_list = []
    for key, value in device_data.items():
        # Judge device type, i.e., server or client.
        if value['type'] == 'server':
            # Judge whether the server object has been created, currently only supports a unique server object.
            if have_server:
                # Create more than one will report an error and terminate the program.
                loggerhear.log("Error Message", 'Server already defined')
                exit(1)

            else:
                have_server = True
                server_device = key
                server_id = value['server_id']

        elif value['type'] == 'client':
            # Extract field values and create client objects.
            client_id = value['client_id']
            data_client_n = fl_data.get_part_train(client_id)
            Client_n = Client(
                client_id=client_id,
                train_data=data_client_n[0],
                train_label=data_client_n[1],
                model=model,
                model_library=model_content['model_library'],
                w_file_initial=value['w_file_initial'],
                optimizer=optimizer,
                loss=loss,
                batch_size=value['batch_size'],
                train_epoch=value['train_epoch'],
            )
            client_list.append(Client_n)

    # Judge whether to create a server object.
    if have_server:
        # Extract field values and create server objects.
        server_content = device_data[server_device]
        server = Server(
            server_id=server_id,
            client_list=client_list,
        )
        aggregation_module = getattr(golf_federated.strategy.aggregation, server_content['aggregation_type'])
        aggregation_func = getattr(aggregation_module, server_content['aggregation_func'])
        server.run(
            execution_form=server_content['execution_form'],
            aggregation=aggregation_func(),
            model=model,
            model_library=model_content['model_library'],
            maxround=server_content['maxround'],
            test_data=fl_data.test_data,
            test_label=fl_data.test_label,
            sim_cc=server_content['sim_cc'],
            sim_zip_path=server_content['sim_zip_path'],
            target_acc=server_content['target_acc'],
            optimizer=optimizer,
            loss=loss,
        )
