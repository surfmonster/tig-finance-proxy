from cmc import coin
from cmc.coin import BuiltInCoin
from client.Client import ClientAbs, QueryDto
from cmc.coin_fetcher import CoinFetcher
from dto.QuoteDto import ProxyQuote


class CMCClientImpl(ClientAbs):

    def __init__(self):
        super().__init__("CMC")

    def is_queryed(self, q: QueryDto) -> bool:
        symbol: str = q.symbol
        be = coin.find_by_symbol(symbol)
        return be is not None

    def proxy(self, q: QueryDto) -> ProxyQuote:
        be = coin.find_by_symbol(q.symbol)
        cinfo = be.getCoinInfo()
        cFetcher = CoinFetcher(cinfo)
        cFetcher.parseHistorical()
        pass
