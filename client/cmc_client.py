from cmc import coin
from cmc.coin import BuiltInCoin
from client.client import ClientAbs, QueryDto
from cmc.coin_fetcher import CoinFetcher
from dto.QuoteDto import ProxyQuote


class CMCClientImpl(ClientAbs):

    def __init__(self):
        super().__init__("CMC")

    def save_util_now(self, q: QueryDto) -> None:
        cFetcher = CMCClientImpl._gen_fetcher(q)
        cFetcher.saveUntilNow()

    def clear_all(self, q: QueryDto) -> None:
        # TODO IMPL
        pass

    def is_queryed(self, q: QueryDto) -> bool:
        symbol: str = q.symbol
        be = coin.find_by_symbol(symbol)
        return be is not None

    def proxy(self, q: QueryDto) -> ProxyQuote:
        cFetcher = CMCClientImpl._gen_fetcher(q)
        ans = cFetcher.get_last()
        return ans

    @staticmethod
    def _gen_fetcher(q: QueryDto) -> CoinFetcher:
        be = coin.find_by_symbol(q.symbol)
        cinfo = be.getCoinInfo()
        cFetcher = CoinFetcher(cinfo)
        return cFetcher
