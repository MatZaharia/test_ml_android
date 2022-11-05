# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/7/14 23:12
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/22 23:12
import random
from typing import Tuple

import numpy as np
from golf_federated.utils.data import deepcopy_list, list_normalization
from golf_federated.utils.log import loggerhear


def random_select(
        client_list: list,
        client_selected_probability: list
) -> list:
    """

    Random client selection without limit on quantity.

    Args:
        client_list (list): Total client list.
        client_selected_probability (list): The probability of being selected for each client.

    Returns:
        List: List of selected clients.

    """

    return_client = []
    for i in range(len(client_list)):
        p = client_selected_probability[i]
        if random.random() < p:
            return_client.append(client_list[i])
    if len(return_client) == 0:
        client_selected_probability_max = max(client_selected_probability)
        id = client_selected_probability.index(client_selected_probability_max)
        return_client.append(client_list[id])
    loggerhear.log("Common Info  ", 'Clients are selected randomly without limit on quantity.')

    return return_client


def random_select_with_percentage(
        client_list: list,
        client_selected_probability: list,
        select_percentage: float
) -> list:
    """

    Random client selection based on a specified percentage.

    Args:
        client_list (list): Total client list.
        client_selected_probability (list): The probability of being selected for each client.
        select_percentage (float): Percentage of selected clients.

    Returns:
        List: List of selected clients.

    """

    return_client = []
    rest_client_list = deepcopy_list(client_list)
    rest_client_selected_probability = deepcopy_list(client_selected_probability)
    select_num = int(select_percentage * len(client_list))
    for i in range(select_num):
        item = random_pick(rest_client_list, rest_client_selected_probability)
        return_client.append(rest_client_list[item])
        rest_client_list.pop(item)
        rest_client_selected_probability.pop(item)
    loggerhear.log("Common Info  ", '%d clients are selected randomly.' % select_num)

    return return_client


def rank_select_with_percentage(
        client_list: list,
        client_selected_probability: list,
        select_percentage: float
) -> list:
    """

    Ranked client selection based on a specified percentage.

    Args:
        client_list (list): Total client list.
        client_selected_probability (list): The probability of being selected for each client.
        select_percentage (float): Percentage of selected clients.

    Returns:
        List: List of selected clients.

    """

    return_client = []
    rank = np.argsort(client_selected_probability)
    select_num = int(select_percentage * len(client_list))
    for i in range(select_num):
        return_client.append(client_list[rank[-1 - i]])
    loggerhear.log("Common Info  ", '%d clients are selected rankly.' % select_num)

    return return_client


def random_pick(
        obj: list,
        prob: list
) -> int:
    """

    Randomly select an object from the list and get its index number.

    Args:
        obj (list): Source list.
        prob (list): The corresponding probability of objects.

    Returns:
        Int: The selected index number.

    """

    r = sum(prob) * random.random()
    s = 0.0
    for i in range(len(obj)):
        s += prob[i]
        if r <= s:
            return i

    return -1


def client_increment(
        client_list_now: list,
        client_list_rest: list,
        min_perc: float,
        max_perc: float,
        prob: float
) -> Tuple[list, list, int, int]:
    """

    Generate incremental clients or disconnect some clients based on the specified probability and percentage interval.

    Args:
        client_list_now (list): List of existing clients.
        client_list_rest (list): List of clients available for incremental.
        min_perc (float): Lower bound for data increment percentage.
        max_perc (float): Upper bound for data increment percentage.
        prob (float): Probability of performing data increment.

    Returns:
        List: Return as a list, including:
            New list of existing clients,
            New list of clients available for incremental,
            Number of new clients,
            Flat indicating whether generate incremental clients or disconnect some clients.

    """

    # Initialize temporary variables.
    shape_now = len(client_list_now)
    shape_rest = len(client_list_rest)
    percent_new = random.uniform(min_perc, max_perc)
    num_change = int(percent_new * shape_now)

    # Judge whether to execute the client increment.
    if random.random() < prob:
        # Generate incremental clients.
        flat = 1
        num_new = num_change
        client_new = []
        # Judge whether the number of clients available for selection is enough
        if num_new <= shape_rest:
            index_all = [i for i in range(shape_rest)]
            index_new = list(np.random.choice(index_all, size=num_new, replace=False))
            index_new.sort()
            for i in range(len(index_new)):
                id = -i - 1
                client_new.append(client_list_rest[index_new[id]])
                client_list_rest.pop(index_new[id])

        else:
            # Disconnect some clients.
            num_change = shape_rest
            client_new = client_list_rest
            client_list_rest = []
        for c in client_new:
            c.round_increment = True
        client_list_now = deepcopy_list(client_list_now) + deepcopy_list(client_new)
        loggerhear.log("Common Info  ", '%d clients are incremented.' % num_change)

    else:
        flat = 0
        num_leave = num_change
        # Judge whether the number of existing clients is enough.
        if num_leave <= shape_now:
            index_all = [i for i in range(shape_now)]
            index_leave = np.random.choice(index_all, size=num_leave, replace=False)
            client_leave = client_list_now[index_leave]
            client_list_now.pop(index_leave)

        else:
            num_change = 0
            client_leave = []
        client_list_rest = deepcopy_list(client_list_rest) + deepcopy_list(client_leave)
        loggerhear.log("Common Info  ", '%d clients are disconnected.' % num_change)

    return deepcopy_list(client_list_now), deepcopy_list(client_list_rest), num_change, flat


def softmax_prob_from_indicators(indicators: list) -> list:
    """

    Convert each index value into probability with softmax.

    Args:
        indicators (list): List of indicators.

    Returns:
        List: List of probabilities after softmax.

    """

    # Judge whether the size of each indicator is the same.
    if all(len(indicators[0]) == len(l) for l in indicators):
        length = len(indicators[0])
        indicators_norm_sum = [0 for i in range(length)]
        for ind_ in indicators:
            ind = list_normalization(ind_)
            ind_e = [np.exp(i) for i in ind]
            ind_e_sum = sum(ind_e)
            indicators_norm_sum = [indicators_norm_sum[i] + ind_e[i] / ind_e_sum for i in range(length)]
        len_ind = len(indicators)
        result = [i / len_ind for i in indicators_norm_sum]
        return result

    else:
        loggerhear.log("Error Message", 'Size of each indicator is not the same')
        exit(1)
