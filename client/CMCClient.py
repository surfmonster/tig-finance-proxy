from cmc.Coin import BuiltInCoin
from client.Client import ClientAbs, QueryDto
from dto.QuoteDto import ProxyQuote


class CMCClientImpl(ClientAbs):

    def __init__(self):
        super().__init__("CMC")

    def is_queryed(self, q: QueryDto) -> bool:
        symbol: str = q.symbol
        for bc in BuiltInCoin:
            if bc.value == symbol:
                return True
        return False

    def proxy(self, q: QueryDto) -> ProxyQuote:
        pass
