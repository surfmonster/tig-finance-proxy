import dateutil

import Config
from client.client import QueryDto
from dto.quote_dto import ProxyQuote


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
    ans.open = toFloat(vals['open'])
    ans.high = toFloat(vals['high'])
    ans.low = toFloat(vals['low'])
    ans.close = toFloat(vals['close'])
    ans.volume = toFloat(vals['volume'])
    ans.market_cap = toFloat(vals['market_cap'])
    ans.timestamp = dateutil.parser.parse(vals['timestamp'])
    ans.source = 'coinmarketcap'
    return ans


def toFloat(i):
    ans = float(i)
    return ans


def get_init_at():
    return dateutil.parser.parse(Config.env("coinmarketcap.init.time"))
