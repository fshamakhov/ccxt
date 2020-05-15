# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange

# -----------------------------------------------------------------------------

try:
    basestring  # Python 3
except NameError:
    basestring = str  # Python 2
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ExchangeNotAvailable


class _1btcxe(Exchange):

    def describe(self):
        return self.deep_extend(super(_1btcxe, self).describe(), {
            'id': '_1btcxe',
            'name': '1BTCXE',
            'countries': ['PA'],  # Panama
            'comment': 'Crypto Capital API',
            'has': {
                'CORS': True,
                'withdraw': True,
            },
            'timeframes': {
                '1d': '1year',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766049-2b294408-5ecc-11e7-85cc-adaff013dc1a.jpg',
                'api': 'https://1btcxe.com/api',
                'www': 'https://1btcxe.com',
                'doc': 'https://1btcxe.com/api-docs.php',
            },
            'api': {
                'public': {
                    'get': [
                        'stats',
                        'historical-prices',
                        'order-book',
                        'transactions',
                    ],
                },
                'private': {
                    'post': [
                        'balances-and-info',
                        'open-orders',
                        'user-transactions',
                        'btc-deposit-address/get',
                        'btc-deposit-address/new',
                        'deposits/get',
                        'withdrawals/get',
                        'orders/new',
                        'orders/edit',
                        'orders/cancel',
                        'orders/status',
                        'withdrawals/new',
                    ],
                },
            },
        })

    def fetch_markets(self, params={}):
        return [
            {'id': 'USD', 'symbol': 'BTC/USD', 'base': 'BTC', 'quote': 'USD', 'baseId': 'BTC', 'quoteId': 'USD'},
            {'id': 'EUR', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'BTC', 'quoteId': 'EUR'},
            {'id': 'CNY', 'symbol': 'BTC/CNY', 'base': 'BTC', 'quote': 'CNY', 'baseId': 'BTC', 'quoteId': 'CNY'},
            {'id': 'RUB', 'symbol': 'BTC/RUB', 'base': 'BTC', 'quote': 'RUB', 'baseId': 'BTC', 'quoteId': 'RUB'},
            {'id': 'CHF', 'symbol': 'BTC/CHF', 'base': 'BTC', 'quote': 'CHF', 'baseId': 'BTC', 'quoteId': 'CHF'},
            {'id': 'JPY', 'symbol': 'BTC/JPY', 'base': 'BTC', 'quote': 'JPY', 'baseId': 'BTC', 'quoteId': 'JPY'},
            {'id': 'GBP', 'symbol': 'BTC/GBP', 'base': 'BTC', 'quote': 'GBP', 'baseId': 'BTC', 'quoteId': 'GBP'},
            {'id': 'CAD', 'symbol': 'BTC/CAD', 'base': 'BTC', 'quote': 'CAD', 'baseId': 'BTC', 'quoteId': 'CAD'},
            {'id': 'AUD', 'symbol': 'BTC/AUD', 'base': 'BTC', 'quote': 'AUD', 'baseId': 'BTC', 'quoteId': 'AUD'},
            {'id': 'AED', 'symbol': 'BTC/AED', 'base': 'BTC', 'quote': 'AED', 'baseId': 'BTC', 'quoteId': 'AED'},
            {'id': 'BGN', 'symbol': 'BTC/BGN', 'base': 'BTC', 'quote': 'BGN', 'baseId': 'BTC', 'quoteId': 'BGN'},
            {'id': 'CZK', 'symbol': 'BTC/CZK', 'base': 'BTC', 'quote': 'CZK', 'baseId': 'BTC', 'quoteId': 'CZK'},
            {'id': 'DKK', 'symbol': 'BTC/DKK', 'base': 'BTC', 'quote': 'DKK', 'baseId': 'BTC', 'quoteId': 'DKK'},
            {'id': 'HKD', 'symbol': 'BTC/HKD', 'base': 'BTC', 'quote': 'HKD', 'baseId': 'BTC', 'quoteId': 'HKD'},
            {'id': 'HRK', 'symbol': 'BTC/HRK', 'base': 'BTC', 'quote': 'HRK', 'baseId': 'BTC', 'quoteId': 'HRK'},
            {'id': 'HUF', 'symbol': 'BTC/HUF', 'base': 'BTC', 'quote': 'HUF', 'baseId': 'BTC', 'quoteId': 'HUF'},
            {'id': 'ILS', 'symbol': 'BTC/ILS', 'base': 'BTC', 'quote': 'ILS', 'baseId': 'BTC', 'quoteId': 'ILS'},
            {'id': 'INR', 'symbol': 'BTC/INR', 'base': 'BTC', 'quote': 'INR', 'baseId': 'BTC', 'quoteId': 'INR'},
            {'id': 'MUR', 'symbol': 'BTC/MUR', 'base': 'BTC', 'quote': 'MUR', 'baseId': 'BTC', 'quoteId': 'MUR'},
            {'id': 'MXN', 'symbol': 'BTC/MXN', 'base': 'BTC', 'quote': 'MXN', 'baseId': 'BTC', 'quoteId': 'MXN'},
            {'id': 'NOK', 'symbol': 'BTC/NOK', 'base': 'BTC', 'quote': 'NOK', 'baseId': 'BTC', 'quoteId': 'NOK'},
            {'id': 'NZD', 'symbol': 'BTC/NZD', 'base': 'BTC', 'quote': 'NZD', 'baseId': 'BTC', 'quoteId': 'NZD'},
            {'id': 'PLN', 'symbol': 'BTC/PLN', 'base': 'BTC', 'quote': 'PLN', 'baseId': 'BTC', 'quoteId': 'PLN'},
            {'id': 'RON', 'symbol': 'BTC/RON', 'base': 'BTC', 'quote': 'RON', 'baseId': 'BTC', 'quoteId': 'RON'},
            {'id': 'SEK', 'symbol': 'BTC/SEK', 'base': 'BTC', 'quote': 'SEK', 'baseId': 'BTC', 'quoteId': 'SEK'},
            {'id': 'SGD', 'symbol': 'BTC/SGD', 'base': 'BTC', 'quote': 'SGD', 'baseId': 'BTC', 'quoteId': 'SGD'},
            {'id': 'THB', 'symbol': 'BTC/THB', 'base': 'BTC', 'quote': 'THB', 'baseId': 'BTC', 'quoteId': 'THB'},
            {'id': 'TRY', 'symbol': 'BTC/TRY', 'base': 'BTC', 'quote': 'TRY', 'baseId': 'BTC', 'quoteId': 'TRY'},
            {'id': 'ZAR', 'symbol': 'BTC/ZAR', 'base': 'BTC', 'quote': 'ZAR', 'baseId': 'BTC', 'quoteId': 'ZAR'},
        ]

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalancesAndInfo(params)
        balance = response['balances-and-info']
        result = {'info': balance}
        codes = list(self.currencies.keys())
        for i in range(0, len(codes)):
            code = codes[i]
            currency = self.currency(code)
            currencyId = currency['id']
            account = self.account()
            account['free'] = self.safe_float(balance['available'], currencyId)
            account['used'] = self.safe_float(balance['on_hold'], currencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'currency': self.market_id(symbol),
        }
        response = self.publicGetOrderBook(self.extend(request, params))
        return self.parse_order_book(response['order-book'], None, 'bid', 'ask', 'price', 'order_amount')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        request = {
            'currency': self.market_id(symbol),
        }
        response = self.publicGetStats(self.extend(request, params))
        ticker = self.safe_value(response, 'stats', {})
        last = self.safe_float(ticker, 'last_price')
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': self.safe_float(ticker, 'max'),
            'low': self.safe_float(ticker, 'min'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': self.safe_float(ticker, 'daily_change'),
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': self.safe_float(ticker, 'total_btc_traded'),
            'info': ticker,
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1d', since=None, limit=None):
        return [
            self.parse8601(ohlcv['date'] + ' 00:00:00'),
            None,
            None,
            None,
            self.safe_float(ohlcv, 'price'),
            None,
        ]

    def fetch_ohlcv(self, symbol, timeframe='1d', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetHistoricalPrices(self.extend({
            'currency': market['id'],
            'timeframe': self.timeframes[timeframe],
        }, params))
        ohlcvs = self.to_array(self.omit(response['historical-prices'], 'request_currency'))
        return self.parse_ohlcvs(ohlcvs, market, timeframe, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_timestamp(trade, 'timestamp')
        id = self.safe_string(trade, 'id')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        type = None
        side = self.safe_string(trade, 'maker_type')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = amount * price
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': type,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = self.publicGetTransactions(self.extend(request, params))
        trades = self.to_array(self.omit(response['transactions'], 'request_currency'))
        return self.parse_trades(trades, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'side': side,
            'type': type,
            'currency': self.market_id(symbol),
            'amount': amount,
        }
        if type == 'limit':
            request['limit_price'] = price
        result = self.privatePostOrdersNew(self.extend(request, params))
        return {
            'info': result,
            'id': result,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        return self.privatePostOrdersCancel(self.extend(request, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency['id'],
            'amount': float(amount),
            'address': address,
        }
        response = self.privatePostWithdrawalsNew(self.extend(request, params))
        return {
            'info': response,
            'id': response['result']['uuid'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        if self.id == 'cryptocapital':
            raise ExchangeError(self.id + ' is an abstract base API for _1btcxe')
        url = self.urls['api'] + '/' + path
        if api == 'public':
            if params:
                url += '?' + self.urlencode(params)
        else:
            self.check_required_credentials()
            query = self.extend({
                'api_key': self.apiKey,
                'nonce': self.nonce(),
            }, params)
            request = self.json(query)
            query['signature'] = self.hmac(self.encode(request), self.encode(self.secret))
            body = self.json(query)
            headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if isinstance(response, basestring):
            if response.find('Maintenance') >= 0:
                raise ExchangeNotAvailable(self.id + ' on maintenance')
        if 'errors' in response:
            errors = []
            for e in range(0, len(response['errors'])):
                error = response['errors'][e]
                errors.append(error['code'] + ': ' + error['message'])
            errors = ' '.join(errors)
            raise ExchangeError(self.id + ' ' + errors)
        return response
