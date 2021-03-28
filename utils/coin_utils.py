import dateutil

import Config
from client.client import QueryDto
from dto.quote_dto import ProxyQuote
from utils import comm_utils


def to_proxy_quote(q: dict, symbol: str, name: str) -> ProxyQuote:
    ans = ProxyQuote()
    ans.symbol = symbol
    ans.name = name
    ans.category = 'cryptocurrency'

    ans.time_open = q['time_open']
    ans.time_close = q['time_close']
    ans.time_high = q['time_high']
    ans.time_low = q['time_low']
    vals = q['quote']['USD']
    ans.open = comm_utils.to_float(vals['open'])
    ans.high = comm_utils.to_float(vals['high'])
    ans.low = comm_utils.to_float(vals['low'])
    ans.close = comm_utils.to_float(vals['close'])
    ans.volume = comm_utils.to_float(vals['volume'])
    ans.market_cap = comm_utils.to_float(vals['market_cap'])
    ans.timestamp = dateutil.parser.parse(vals['timestamp'])
    ans.source = 'coinmarketcap'
    return ans





def get_init_at():
    return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))
