# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/28 21:03
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/5/28 21:03

import warnings

warnings.filterwarnings("ignore", category=Warning)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from CNN import create_cnn_for_mnist

import tensorflow as tf

from golf_federated.client.config import Client
from golf_federated.data.dataset import CustomFederatedDataset



if __name__ == '__main__':
    data_dir = './data/'
    x_train = [data_dir + 'x_train_6.npy']
    y_train = [data_dir + 'y_train_6.npy']
    x_test = [data_dir + 'x_test_6.npy']
    y_test = [data_dir + 'y_test_6.npy']
    client_id = ['Client6']

    mnist_fl_data = CustomFederatedDataset(
        train_data=x_train,
        train_label=y_train,
        test_data=x_test,
        test_label=y_test,
        part_num=1,
        part_id=client_id,
        split_data=True,
    )

    model = create_cnn_for_mnist()

    optimizer = tf.keras.optimizers.SGD(learning_rate=0.03)
    loss = tf.keras.losses.CategoricalCrossentropy()
    batch_size = 128
    train_epoch = 1
    max_round = 100
    data_client_n = mnist_fl_data.get_part_train(client_id[0])
    Client_1 = Client(
        client_id=client_id[0],
        train_data=data_client_n[0],
        train_label=data_client_n[1],
        model=model,
        model_library='tensorflow',
        optimizer=optimizer,
        loss=loss,
        batch_size=batch_size,
        train_epoch=train_epoch,
        client_test=True,
        test_data=mnist_fl_data.test_data,
        test_label=mnist_fl_data.test_label,
    )
    Client_1.monitor(
        thread_name='monitor',
        url='127.0.0.1',
        port='7788',

    )
    Client_1.runtask(
        url='127.0.0.1',
        port='7788',
        server_id='server1',
        task_name='MultiDeviceTest'
    )

