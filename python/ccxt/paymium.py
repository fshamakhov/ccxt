# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class paymium (Exchange):

    def describe(self):
        return self.deep_extend(super(paymium, self).describe(), {
            'id': 'paymium',
            'name': 'Paymium',
            'countries': ['FR', 'EU'],
            'rateLimit': 2000,
            'version': 'v1',
            'has': {
                'CORS': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27790564-a945a9d4-5ff9-11e7-9d2d-b635763f2f24.jpg',
                'api': 'https://paymium.com/api',
                'www': 'https://www.paymium.com',
                'doc': [
                    'https://github.com/Paymium/api-documentation',
                    'https://www.paymium.com/page/developers',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        'countries',
                        'data/{id}/ticker',
                        'data/{id}/trades',
                        'data/{id}/depth',
                        'bitcoin_charts/{id}/trades',
                        'bitcoin_charts/{id}/depth',
                    ],
                },
                'private': {
                    'get': [
                        'merchant/get_payment/{UUID}',
                        'user',
                        'user/addresses',
                        'user/addresses/{btc_address}',
                        'user/orders',
                        'user/orders/{UUID}',
                        'user/price_alerts',
                    ],
                    'post': [
                        'user/orders',
                        'user/addresses',
                        'user/payment_requests',
                        'user/price_alerts',
                        'merchant/create_payment',
                    ],
                    'delete': [
                        'user/orders/{UUID}/cancel',
                        'user/price_alerts/{id}',
                    ],
                },
            },
            'markets': {
                'BTC/EUR': {'id': 'eur', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'btc', 'quoteId': 'eur'},
            },
            'fees': {
                'trading': {
                    'maker': 0.0059,
                    'taker': 0.0059,
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetUser(params)
        result = {'info': response}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            code = currencies[i]
            currencyId = self.currencyId(code)
            free = 'balance_' + currencyId
            if free in response:
                account = self.account()
                used = 'locked_' + currencyId
                account['free'] = self.safe_float(response, free)
                account['used'] = self.safe_float(response, used)
                result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'id': self.market_id(symbol),
        }
        response = self.publicGetDataIdDepth(self.extend(request, params))
        return self.parse_order_book(response, None, 'bids', 'asks', 'price', 'amount')

    def fetch_ticker(self, symbol, params={}):
        request = {
            'id': self.market_id(symbol),
        }
        ticker = self.publicGetDataIdTicker(self.extend(request, params))
        timestamp = self.safe_timestamp(ticker, 'at')
        vwap = self.safe_float(ticker, 'vwap')
        baseVolume = self.safe_float(ticker, 'volume')
        quoteVolume = None
        if baseVolume is not None and vwap is not None:
            quoteVolume = baseVolume * vwap
        last = self.safe_float(ticker, 'price')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_float(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_float(ticker, 'variation'),
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }

    def parse_trade(self, trade, market):
        timestamp = self.safe_timestamp(trade, 'created_at_int')
        id = self.safe_string(trade, 'uuid')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        side = self.safe_string(trade, 'side')
        price = self.safe_float(trade, 'price')
        amountField = 'traded_' + market['base'].lower()
        amount = self.safe_float(trade, amountField)
        cost = None
        if price is not None:
            if amount is not None:
                cost = amount * price
        return {
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': None,
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
            'id': market['id'],
        }
        response = self.publicGetDataIdTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'type': self.capitalize(type) + 'Order',
            'currency': self.market_id(symbol),
            'direction': side,
            'amount': amount,
        }
        if type != 'market':
            request['price'] = price
        response = self.privatePostUserOrders(self.extend(request, params))
        return {
            'info': response,
            'id': response['uuid'],
        }

    def cancel_order(self, id, symbol=None, params={}):
        request = {
            'UUID': id,
        }
        return self.privateDeleteUserOrdersUUIDCancel(self.extend(request, params))

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + url
            if method == 'POST':
                if query:
                    body = self.json(query)
                    auth += body
            headers = {
                'Api-Key': self.apiKey,
                'Api-Signature': self.hmac(self.encode(auth), self.encode(self.secret)),
                'Api-Nonce': nonce,
                'Content-Type': 'application/json',
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'errors' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
