from Coin import BuiltInCoin
from client.Client import ClientAbs, registerClient, QueryDto


class CMCClientImpl(ClientAbs):

    def __init__(self):
        super().__init__("CMC")

    def is_queryed(self, q: QueryDto) -> bool:
        symbol: str = q.symbol
        for bc in BuiltInCoin:
            if bc.value == symbol:
                return True
        return False

    def proxy(self, q: QueryDto) -> bool:
        pass

