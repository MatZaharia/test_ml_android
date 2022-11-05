# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/24 16:15
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/5/24 16:15

import tensorflow as tf
# import os
#
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def create_cnn_for_mnist():
    return tf.keras.Sequential(
        [
            tf.keras.layers.Conv2D(
                32, kernel_size=(5, 5),
                activation='relu',
                input_shape=(28, 28, 1),
            ),
            tf.keras.layers.Conv2D(64, (5, 5), activation='relu'),
            tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
            tf.keras.layers.Dropout(0.25),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(10, activation='softmax'),
        ]
    )