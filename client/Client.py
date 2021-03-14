from abc import ABCMeta, abstractmethod
from flask import Flask
import client.CMCClient

clients = []


class ClientAbs(metaclass=ABCMeta):

    def __init__(self, channel: str):
        self.channel = channel

    def reqByUrlQuery(self, q: str):
        print(q)


def registerClient(c: ClientAbs):
    clients.append(c)
    print(clients)



