from datetime import datetime

from cmc import coin, coin_fetcher
from cmc.coin import BuiltInCoin
from client.client import ClientAbs, QueryDto
from cmc.coin_fetcher import CoinFetcher
from dto.quote_dto import ProxyQuote
from tsdb import coin_dao
from tsdb.coin_dao import CoinDao
from utils import coin_utils, comm_utils


def _get_kit(q: QueryDto) -> (CoinDao, CoinFetcher):
    bie: BuiltInCoin = coin.find_by_symbol(q.symbol)
    cFetcher = coin_fetcher.get_built_in(bie)
    dao = coin_dao.get_built_in(bie)
    return dao, cFetcher


class CMCClientImpl(ClientAbs):

    def __init__(self):
        super().__init__("CMC")

    def save_util_now(self, q: QueryDto) -> None:
        dao, cFetcher = _get_kit(q)
        sAt = dao.get_Last_save_at()
        eAt = datetime.now()
        CMCClientImpl._save_between(q, sAt, eAt)

    @staticmethod
    def _save_between(q: QueryDto, s_at: datetime, e_at: datetime) -> datetime:
        dao, cFetcher = _get_kit(q)
        f_list = cFetcher.parseHistorical(s_at, e_at)
        dao.save_all(f_list)
        return f_list[-1].timestamp

    def get_init_at(self) -> datetime:
        return coin_utils.get_init_at()

    def clear_all(self, q: QueryDto) -> None:
        # TODO IMPL
        pass

    def is_queryed(self, q: QueryDto) -> bool:
        symbol: str = q.symbol
        be = coin.find_by_symbol(symbol)
        return be is not None

    def proxy(self, q: QueryDto) -> ProxyQuote:
        dao, cFetcher = _get_kit(q)
        ans = cFetcher.get_last_when_now()
        return ans

    def check_regular_all(self, q: QueryDto):
        dao, cFetcher = _get_kit(q)
        dao.check_regular_all(self._check_quote)

    def _check_quote(self, init_at: datetime, now: datetime, last_check_at: datetime, point: ProxyQuote) -> datetime:
        pass
        # TODO
        # if last_check_at is None:
        #     last_check_at = init_at
        #
        #     diff = point.timestamp - last_check_at
        #     if diff.seconds > comm_utils.one_day_seconds:
