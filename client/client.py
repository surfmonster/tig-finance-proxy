from abc import ABCMeta, abstractmethod


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

    @abstractmethod
    def clear_all(self,symbol:str) -> None :
        pass

    @abstractmethod
    def save_util_now(self,symbol:str) ->None :
        pass


def proxy(q: QueryDto) -> ProxyQuote:
    for c in clients:
        cabs: ClientAbs = c
        if cabs.is_queryed(q):
            return cabs.proxy(q)
    raise NameError('not find' + q.symbol)


def register_client(c: ClientAbs):
    clients.append(c)
    print(clients)


def get_client_by_channel(c: str):
    return filter(lambda x: x.channel == c, clients)
