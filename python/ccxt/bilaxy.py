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
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import ExchangeNotAvailable


class bilaxy (Exchange):

    def describe(self):
        return self.deep_extend(super(bilaxy, self).describe(), {
            'id': 'bilaxy',
            'name': 'Bilaxy',
            'countries': ['CN'],  # Japan, Malta
            'rateLimit': 500,
            'has': {
                'fetchDepositAddress': True,
                'createMarketOrder': False,
                'fetchBidsAsks': True,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrders': True,
                'fetchTickers': True,
            },
            'urls': {
                'logo': 'https://bilaxy.com/dist/images/logo.png',
                'api': {
                    'web': 'https://bilaxy.com',
                    'public': 'https://api.bilaxy.com/v1',
                    'private': 'https://api.bilaxy.com/v1',
                    'v1': 'https://api.bilaxy.com/v1',
                    'v2': 'https://bilaxy.com/api/v2',
                },
                'www': 'https://bilaxy.com',
                'doc': 'https://bilaxy.com/api',
            },
            'api': {
                'public': {
                    'get': [
                        'depth',
                        'coins',
                        'orders',
                        'ticker',
                        'tickers',
                    ],
                },
                'private': {
                    'get': [
                        'balances',
                        'coin_address',
                        'trade_list',
                        'trade_view',
                    ],
                    'post': [
                        'cancel_trade',
                        'trade',
                    ],
                },
                'v2': {
                    'get': [
                        'market/depth',
                        'market/coins',
                        'market/orders',
                    ],
                },
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.0015,
                    'maker': 0.0015,
                },
            },
            'bilaxySymbols': {},
            'commonCurrencies': {
                'CPT': 'Contents Protocol',
                'CRE': 'Carry',
                'EMB': 'Emblem',
                'SFT': 'SportsFix',
                'SMT': 'Smathium',
            },
            'exceptions': {
                '101': {'class': ArgumentsRequired, 'msg': 'The required parameters cannot be empty'},
                '102': {'class': AuthenticationError, 'msg': 'API key dose not exist'},
                '103': {'class': ExchangeError, 'msg': 'API is no longer used'},
                '104': {'class': PermissionDenied, 'msg': 'Permissions closed'},
                '105': {'class': PermissionDenied, 'msg': 'Insufficient authority'},
                '106': {'class': AuthenticationError, 'msg': 'Signature mismatch'},
                '201': {'class': BadRequest, 'msg': 'The asset does not exist'},
                '202': {'class': BadRequest, 'msg': 'The asset cannot be deposit or withdraw'},
                '203': {'class': ExchangeError, 'msg': 'The asset is not yet allocated to the wallet address'},
                '204': {'class': ExchangeError, 'msg': 'Failed to cancel the order'},
                '205': {'class': ExchangeError, 'msg': 'The transaction amount must not be less than 0.0001'},
                '206': {'class': ExchangeError, 'msg': 'The transaction price must not be less than 0.0001'},
                '-100': {'class': ExchangeError, 'msg': 'The transaction is lock'},
                '208': {'class': InsufficientFunds, 'msg': 'Insufficient base currency balance'},
                '209': {'class': AuthenticationError, 'msg': 'The transaction password is error'},
                '210': {'class': BadRequest, 'msg': 'The transaction price is not within the limit price'},
                '-4': {'class': InsufficientFunds, 'msg': 'Insufficient currency balance'},
                '212': {'class': BadRequest, 'msg': 'The maximum amount of the transaction is limited'},
                '213': {'class': BadRequest, 'msg': 'The minimum total amount of the transaction is limited'},
                '401': {'class': BadRequest, 'msg': 'Illegal parameter'},
                '402': {'class': ExchangeNotAvailable, 'msg': 'System error'},
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetCoins()
        markets = response['data']
        result = []
        for i in range(0, len(markets)):
            market = markets[i]
            id = market['name'] + market['group']
            baseId = market['name']
            quoteId = market['group']
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'base': market['priceDecimals'],
                'quote': market['priceDecimals'],
                'amount': market['priceDecimals'],
                'price': market['priceDecimals'],
            }
            active = True
            self.bilaxySymbols[symbol] = market['symbol']
            entry = {
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
                'active': active,
                'precision': precision,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'price': {
                        'min': None,
                        'max': None,
                    },
                    'cost': {
                        'min': 0.01,
                        'max': None,
                    },
                },
            }
            result.append(entry)
        return result

    def get_bilaxy_symbol(self, symbol):
        if self.bilaxySymbols is None:
            raise ExchangeError(self.id + ' markets not loaded')
        if (isinstance(symbol, basestring)) and (symbol in list(self.bilaxySymbols.keys())):
            return self.bilaxySymbols[symbol]
        raise ExchangeError(self.id + ' does not have market symbol ' + symbol)

    def get_symbol_from_bilaxy(self, symbol):
        if self.bilaxySymbols is None:
            raise ExchangeError(self.id + ' markets not loaded')
        keys = list(self.bilaxySymbols.keys())
        for i in range(0, len(keys)):
            id = keys[i]
            if self.bilaxySymbols[id] == symbol:
                return id
        raise ExchangeError(self.id + ' does not have market symbol')

    def fetch_order_book(self, symbol, limit=None, params={}):
        bilaxy_symbol = self.get_bilaxy_symbol(symbol)
        request = {
            'symbol': bilaxy_symbol,
        }
        response = self.publicGetDepth(self.extend(request, params))
        return self.parse_order_book(response['data'])

    def parse_ticker(self, symbol, ticker, market=None):
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': self.safe_float(ticker, 'vol'),
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': self.safe_float(ticker, 'vol'),
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': None,
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_ticker(self, symbol, params={}):
        bilaxy_symbol = self.get_bilaxy_symbol(symbol)
        response = self.publicGetTicker(self.extend({
            'symbol': bilaxy_symbol,
        }, params))
        self.load_markets()
        market = self.market(symbol)
        return self.parse_ticker(symbol, response['data'], market)

    def parse_tickers(self, rawTickers, symbols=None):
        self.load_markets()
        tickers = []
        for i in range(0, len(rawTickers)):
            symbol = self.get_symbol_from_bilaxy(rawTickers[i]['symbol'])
            market = self.market(symbol)
            tickers.append(self.parse_ticker(symbol, rawTickers[i], market))
        return self.filter_by_array(tickers, 'symbol', symbols)

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        rawTickers = self.publicGetTickers(params)
        return self.parse_tickers(rawTickers['data'], symbols)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'count')
        id = self.safe_string(trade, 'id')
        side = self.safe_string(trade, 'type')
        cost = self.safe_float(trade, 'amount')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'id': id,
            'order': None,
            'type': None,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['info']['symbol'],
        }
        if limit is not None:
            request['size'] = limit  # default = 100, maximum = 000
        response = self.publicGetOrders(self.extend(request, params))
        return self.parse_trades(response['data'], market, None, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privateGetBalances(params)
        result = {'info': response['data']}
        balances = response['data']
        for i in range(0, len(balances)):
            balance = balances[i]
            currency = balance['name']
            if currency in self.currencies_by_id:
                currency = self.currencies_by_id[currency]['code']
            account = {
                'free': float(balance['balance']),
                'used': float(balance['frozen']),
                'total': 0.0,
            }
            account['total'] = self.sum(account['free'], account['used'])
            result[currency] = account
        return self.parse_balance(result)

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            raise ExchangeError(self.id + ' response is empty.')
        exceptions = self.exceptions
        bilaxyCode = self.safe_string(response, 'code')
        if bilaxyCode in exceptions:
            ExceptionClass = exceptions[bilaxyCode]['class']
            message = exceptions[bilaxyCode]['msg']
            raise ExceptionClass(self.id + ' ' + message)

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': int(id),
        }
        response = self.privateGetTradeView(self.extend(request, params))
        return self.parse_order(response, market)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'symbol': market['info']['symbol'],
            'type': 0,  # => All orders
        }
        if since is not None:
            request['since'] = since
        response = self.privateGetTradeList(self.extend(request, params))
        return self.parse_orders(response['data'], market, since, limit)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        openParams = {'type': 1}  # 1 => Pending orders
        return self.fetch_orders(symbol, since, limit, self.extend(openParams, params))

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        orders = self.fetch_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 3)  # 3 => Traded completely

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'id': int(id),
        }
        response = self.privatePostCancelTrade(self.extend(request, params))
        order = self.privateGetTradeView({'id': response['data']})
        return self.parse_order(order['data'], market)

    def parse_order_status(self, status):
        statusString = self.number_to_string(status)
        statuses = {
            '1': 'open',
            '2': 'open',
            '3': 'closed',
            '4': 'canceled',
        }
        return self.safe_string(statuses, statusString, statusString)

    def parse_order(self, order, market=None):
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = None
        if market:
            symbol = market['symbol']
        timestamp = None
        datetime = self.safe_string(order, 'datetime')
        if datetime:
            timestamp = self.parse8601(datetime)
        price = self.safe_float(order, 'price')
        amount = self.safe_float(order, 'amount')
        remaining = self.safe_float(order, 'left_amount')
        cost = None
        filled = None
        if remaining is not None:
            if amount is not None:
                filled = amount - remaining
                if self.options['parseOrderToPrecision']:
                    filled = float(self.amount_to_precision(symbol, filled))
                filled = max(filled, 0.0)
            if (price is not None) and (filled is not None):
                cost = price * filled
        id = self.safe_string(order, 'id')
        type = 'limit'  # Bilaxy has only limit orders
        side = self.safe_string(order, 'type')
        if side is not None:
            side = side.lower()
        fee = None
        trades = None
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
            'trades': trades,
        }

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        if price is None:
            raise InvalidOrder(self.id + ' createOrder method requires a price argument')
        request = {
            'symbol': market['info']['symbol'],
            'amount': self.amount_to_precision(symbol, amount),
            'price': self.price_to_precision(symbol, price),
            'type': side,
        }
        response = self.privatePostTrade(self.extend(request, params))
        order = self.privateGetTradeView({'id': response['data']})
        return self.parse_order(order['data'], market)

    def fetch_deposit_address(self, code, params={}):
        balance = self.fetch_balance()
        self.load_markets()
        currency = self.currency(code)
        symbol = self.filter_by(balance['info'], 'name', currency['id'])
        if len(symbol) != 1:
            raise ExchangeError(self.id + ' could not find currency with code ' + code)
        symbol = symbol[0]['symbol']
        request = {
            'symbol': symbol,
        }
        response = self.privateGetCoinAddress(self.extend(request, params))
        address = self.safe_string(response, 'data')
        self.check_address(address)
        return {
            'currency': code,
            'address': address,
            'tag': None,
            'info': response,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        if (api == 'public') or (api == 'v2'):
            if params:
                url += '?' + self.urlencode(params)
            if api == 'v2':
                headers = {'accept': 'application/json'}
        else:
            self.check_required_credentials()
            sorted = self.encode(self.urlencode(self.keysort(self.extend({
                'key': self.apiKey,
                'secret': self.secret,
            }, params))))
            signature = self.hash(sorted, 'sha1')
            query = self.urlencode(self.keysort(self.extend({
                'key': self.apiKey,
                'sign': signature,
            }, params)))
            # print('params:', params, 'sorted:', sorted, 'query:', query)
            if method == 'GET':
                url += '?' + query
            else:
                body = query
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
