from abc import ABCMeta, abstractmethod

from dto.quote_dto import ProxyQuote

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

    @abstractmethod
    def clear_all(self, q: QueryDto) -> None:
        pass

    @abstractmethod
    def save_util_now(self, q: QueryDto) -> None:
        pass


def clear_all(q: QueryDto) -> None:
    cabs = _get_client(q)
    cabs.clear_all(q)


def save_all(q: QueryDto) -> None:
    cabs = _get_client(q)
    cabs.save_util_now(q)


def proxy(q: QueryDto) -> ProxyQuote:
    cabs = _get_client(q)
    cabs.proxy(q)


def _get_client(q: QueryDto) -> ClientAbs:
    for c in clients:
        cabs: ClientAbs = c
        if cabs.is_queryed(q):
            return cabs
    raise NameError('not find' + q.symbol)


def register_client(c: ClientAbs):
    clients.append(c)
    print(clients)


def get_client_by_channel(c: str):
    return filter(lambda x: x.channel == c, clients)
