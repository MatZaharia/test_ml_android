# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/18 17:42
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/5/22 3:35

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import base64

def CreateRSAKeys():
    """
    Create a pair of RSA keys.
    :return: None
    """
    code = 'nooneknows'
    # The length of key
    key = RSA.generate(2048)
    # (*For private keys only*) The passphrase used for protecting the output.
    encrypted_key = key.exportKey(passphrase=code, pkcs=8, protection="scryptAndAES128-CBC")
    # private key
    with open('keys/my_private_rsa_key.bin', 'wb') as f:
        f.write(encrypted_key)
    # public key
    with open('keys/my_rsa_public.pem', 'wb') as f:
        f.write(key.publickey().exportKey())

def Encrypt(filename):
    """
    Encrypt the file.
    :param filename: the name of file which will be encrypted
    :return: None
    """

    data = ''
    # 二进制方式读入
    with open(filename, 'rb') as f:
        data = f.read()

    print(data)
    # 二进制方式写入
    with open(filename, 'wb') as out_file:
        # 收件人秘钥 -> 公钥 可以传给用户的
        recipient_key = RSA.import_key(open('my_rsa_public.pem').read())
        print(recipient_key)
        # 一个 16 字节的会话密钥
        session_key = get_random_bytes(16)
        # Encrypt the session key with the public RSA key
        # 用RSA公钥 加密 session key
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))
        # Encrypt the data with the AES session key
        # 再用生成的session key去加密数据data，AES.MODE_EAX是其中一种认证加密模式
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        # 返回tuple，
        # - the ciphertext, as ``bytes``
        # - the MAC tag, as ``bytes``
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)


def Descrypt(filename):
    """
    Decrypt the file.
    :param filename: the name of file which will be decrypted
    :return:
    """
    code = 'nooneknows'
    with open(filename, 'rb') as fobj:
        # code也就是passphrase需要一致 导入私钥
        private_key = RSA.import_key(open('my_private_rsa_key.bin').read(), passphrase=code)
        # 会话密钥, 随机数, 消息认证码, 机密的数据（密文）
        enc_session_key, nonce, tag, ciphertext = [fobj.read(x)
                                                   for x in (private_key.size_in_bytes(),
                                                             16, 16, -1)]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        # 用RSA私钥decrypt出 session key
        session_key = cipher_rsa.decrypt(enc_session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        # 用session key解密data（密文）
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(data)
    with open(filename, 'wb') as wobj:
        wobj.write(data)

if __name__ == '__main__':
    CreateRSAKeys()
