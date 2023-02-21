import requests
from pybit import spot
from fake_useragent import FakeUserAgent


def get_kline_pybit(symbol, interval, limit=200):
    """
    used https://pypi.org/project/pybit/
    Function getting kline data
    :param symbol: name of the couple, example: BTCUSDT -> str
    :param interval: time interval of the couple, exmaple: 1m, 5m, 10m -> str
    :param category: This API don't have category
    :param limit: Limit for data size per page. [1, 200]. Default: 200
    :return:
              'ret_code': 0,
              'ret_msg': '',
              'result': [
                [
                  1676970660000,        -> Start time, unit in millisecond
                  '17994.68',           -> Open price
                  '17994.68',           -> High price
                  '17994.68',           -> Low price
                  '17994.68',           -> Close price
                  '0.003947',           -> Trading volume
                  1676970720000,        -> End time, unit in millisecond
                  '71.02500196',        -> Quote asset volume
                  8,                    -> Number of trades
                  0,                    -> Taker buy volume in base asset
                  0                     -> Taker buy volume in quote asset
                ]
              ],
              'ext_info': None,
              'ext_code': None
    """
    session_unauth = spot.HTTP(
        endpoint='https://api-testnet.bybit.com',
    )
    data = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }

    return session_unauth.query_kline(**data)
print(get_kline_pybit('btcusdt', '1m', limit=1))


def get_kline_v5(symbol, interval, category='spot', limit=200):
    """
    :param symbol: name of the couple, example: BTCUSDT, ETHUSDT -> str
    :param interval: time interval of the couple, exmaple: 1,3,5,15,30,60,120,240,360,720 -> int; D,M,W -> str
    :param category: category of product type, exmaple: spot, linear, inverse -> str
    :param limit: Limit for data size per page. [1, 200]. Default: 200
    :return:
              'retCode': 0,
              'retMsg': 'OK',
              'result': {
                'category': 'spot',
                'symbol': 'BTCUSDT',
                'list': [
                  [
                    '1676970120000',        -> Start time of the candle (ms)
                    '17994.68',             -> Open price
                    '17994.68',             -> Highest price
                    '17994.67',             -> Lowest price
                    '17994.68',             -> Close price. Is the last traded price when the candle is not closed
                    '0.023655',             -> Trade volume. Unit of contract: pieces of contract. Unit of spot: quantity of coins
                    '425.66415012'          -> Turnover. Unit of figure: quantity of quota coin
                  ]
                ]
              },
              'retExtInfo': {},
              'time': 1676970160179
    """
    url = 'https://api-testnet.bybit.com/v5/market/kline'

    data = {
        'category': category,
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }

    headers = {
        'User-Agent': FakeUserAgent().random
    }

    return requests.get(url, headers=headers, params=data).json()


print(get_kline_v5('btcusdt', 1, limit=1))

def get_kline_v3(symbol, interval, limit=1000):
    """
    :param symbol: Name of the trading paire, example: BTCUSDT, ETHUSDT -> str
    :param interval: time interval of the couple, exmaple: 1m,3m,5m,15m,30m,1h,2h,4h,6h,12h,1d,1w,1M -> str
    :param category: This API don't have category
    :param limit: Limit for data size. [1, 1000]. Default: 1000
    :return:
              'retCode': 0,
              'retMsg': 'OK',
              'result': {
                'list': [
                  {
                    't': 1676969820000,     -> Timestamp(ms)
                    's': 'BTCUSDT',         -> Name of the trading pair
                    'sn': 'BTCUSDT',        -> Alias
                    'c': '17963.39',        -> Close price
                    'h': '17963.39',        -> High price
                    'l': '17963.38',        -> Low price
                    'o': '17963.39',        -> Open price
                    'v': '0.070116'         -> Trading volume
                  }
                ]
              },
              'retExtInfo': {},
              'time': 1676969861900
    """
    url = 'https://api-testnet.bybit.com/spot/v3/public/quote/kline'

    data = {
        'symbol': symbol.upper(),
        'interval': interval,
        'limit': limit
    }

    headers = {
        'User-Agent': FakeUserAgent().random
    }

    return requests.get(url, headers=headers, params=data).json()
print(get_kline_v3('btcusdt', '1m', limit=1))
