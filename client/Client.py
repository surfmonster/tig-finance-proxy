import json
from abc import ABCMeta, abstractmethod
from flask import Flask
import client.CMCClient
from urllib.parse import unquote

from dto.QuoteDto import ProxyQuote

clients: list = []


class QueryDto:
    symbol: str
    category: str

    def __init__(self, **entries):
        self.__dict__.update(entries)


class ClientAbs(metaclass=ABCMeta):

    def __init__(self, channel: str):
        self.channel = channel

    @abstractmethod
    def is_queryed(self, q: QueryDto) -> bool:
        pass

    @abstractmethod
    def proxy(self, q: QueryDto) -> ProxyQuote:
        pass


def registerClient(c: ClientAbs):
    clients.append(c)
    print(clients)


def getClientByChannel(c: str):
    return filter(lambda x: x.channel == c, clients)
