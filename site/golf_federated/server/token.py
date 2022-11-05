# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/18 18:07
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/5/22 3:35

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def create_token(username):
    """
    Create a token based on the username.
    :param username: the username to create a token.
    :return: the created token
    """
    key = Serializer('abcdefghijklmm', expires_in=3600)
    token = key.dumps({"username": username}).decode("ascii")
    return token

def verify_token(token):
    """
    The function can verify Identity by the token.
    :param token:
    :return: the username that the token supports.
    """
    key = Serializer('abcdefghijklmm')
    try:
        # convert to a dictionary {'username': '18811891816'}
        data = key.loads(token)
    except Exception:
        return False
    return data