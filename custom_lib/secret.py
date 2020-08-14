import os
import time

from cryptography.fernet import Fernet

class Secret(object):

    def __init__(self, key=None):
        self.__key = os.environ.get('ENC_KEY', key)
        self.__f = Fernet(self.__key)

    def encrypt(self, msg):
        encoded_msg = msg.encode()
        return self.__f.encrypt(encoded_msg).decode()

    def decrypt(self, msg):
        encoded_msg = msg.encode()
        return self.__f.decrypt(encoded_msg).decode()




