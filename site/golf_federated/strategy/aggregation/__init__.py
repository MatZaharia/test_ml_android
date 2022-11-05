# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/24 14:47
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/5/24 14:47

from golf_federated.strategy.aggregation import asynchronous as asynchronous
from golf_federated.strategy.aggregation import basic as basic
from golf_federated.strategy.aggregation import function as function
from golf_federated.strategy.aggregation import synchronous as synchronous




__all__=[
    'asynchronous',
    'basic',
    'function',
    'synchronous',
]