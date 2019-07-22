# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class indodax (Exchange):

    def describe(self):
        return self.deep_extend(super(indodax, self).describe(), {
            'id': 'indodax',
            'name': 'INDODAX',
            'countries': ['ID'],  # Indonesia
            'has': {
                'CORS': False,
                'createMarketOrder': False,
                'fetchTickers': False,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchClosedOrders': True,
                'fetchOpenOrders': True,
                'fetchMyTrades': False,
                'fetchCurrencies': False,
                'withdraw': True,
            },
            'version': '1.8',  # as of 9 April 2018
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/37443283-2fddd0e4-281c-11e8-9741-b4f1419001b5.jpg',
                'api': {
                    'public': 'https://indodax.com/api',
                    'private': 'https://indodax.com/tapi',
                },
                'www': 'https://www.indodax.com',
                'doc': 'https://indodax.com/downloads/BITCOINCOID-API-DOCUMENTATION.pdf',
                'referral': 'https://indodax.com/ref/testbitcoincoid/1',
            },
            'api': {
                'public': {
                    'get': [
                        '{pair}/ticker',
                        '{pair}/trades',
                        '{pair}/depth',
                    ],
                },
                'private': {
                    'post': [
                        'getInfo',
                        'transHistory',
                        'trade',
                        'tradeHistory',
                        'getOrder',
                        'openOrders',
                        'cancelOrder',
                        'orderHistory',
                        'withdrawCoin',
                    ],
                },
            },
            'markets': {
                # HARDCODING IS DEPRECATED
                # but they don't have a corresponding endpoint in their API
                'BTC/IDR': {'id': 'btc_idr', 'symbol': 'BTC/IDR', 'base': 'BTC', 'quote': 'IDR', 'baseId': 'btc', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.0001, 'max': None}}},
                'ACT/IDR': {'id': 'act_idr', 'symbol': 'ACT/IDR', 'base': 'ACT', 'quote': 'IDR', 'baseId': 'act', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': None, 'max': None}}},
                'ADA/IDR': {'id': 'ada_idr', 'symbol': 'ADA/IDR', 'base': 'ADA', 'quote': 'IDR', 'baseId': 'ada', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': None, 'max': None}}},
                'BCD/IDR': {'id': 'bcd_idr', 'symbol': 'BCD/IDR', 'base': 'BCD', 'quote': 'IDR', 'baseId': 'bcd', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': None, 'max': None}}},
                'BCH/IDR': {'id': 'bch_idr', 'symbol': 'BCH/IDR', 'base': 'BCH', 'quote': 'IDR', 'baseId': 'bch', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.001, 'max': None}}},
                'BTG/IDR': {'id': 'btg_idr', 'symbol': 'BTG/IDR', 'base': 'BTG', 'quote': 'IDR', 'baseId': 'btg', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'BTS/IDR': {'id': 'bts_idr', 'symbol': 'BTS/IDR', 'base': 'BTS', 'quote': 'IDR', 'baseId': 'bts', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'DASH/IDR': {'id': 'drk_idr', 'symbol': 'DASH/IDR', 'base': 'DASH', 'quote': 'IDR', 'baseId': 'drk', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'DOGE/IDR': {'id': 'doge_idr', 'symbol': 'DOGE/IDR', 'base': 'DOGE', 'quote': 'IDR', 'baseId': 'doge', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 1000, 'max': None}}},
                'ETH/IDR': {'id': 'eth_idr', 'symbol': 'ETH/IDR', 'base': 'ETH', 'quote': 'IDR', 'baseId': 'eth', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'ETC/IDR': {'id': 'etc_idr', 'symbol': 'ETC/IDR', 'base': 'ETC', 'quote': 'IDR', 'baseId': 'etc', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.1, 'max': None}}},
                'GSC/IDR': {'id': 'gsc_idr', 'symbol': 'GSC/IDR', 'base': 'GSC', 'quote': 'IDR', 'baseId': 'gsc', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.1, 'max': None}}},
                'IGNIS/IDR': {'id': 'ignis_idr', 'symbol': 'IGNIS/IDR', 'base': 'IGNIS', 'quote': 'IDR', 'baseId': 'ignis', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 1, 'max': None}}},
                'LTC/IDR': {'id': 'ltc_idr', 'symbol': 'LTC/IDR', 'base': 'LTC', 'quote': 'IDR', 'baseId': 'ltc', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'NPXS/IDR': {'id': 'npxs_idr', 'symbol': 'NPXS/IDR', 'base': 'NPXS', 'quote': 'IDR', 'baseId': 'npxs', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 1, 'max': None}}},
                'NXT/IDR': {'id': 'nxt_idr', 'symbol': 'NXT/IDR', 'base': 'NXT', 'quote': 'IDR', 'baseId': 'nxt', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 5, 'max': None}}},
                'STQ/IDR': {'id': 'stq_idr', 'symbol': 'STQ/IDR', 'base': 'STQ', 'quote': 'IDR', 'baseId': 'stq', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': None, 'max': None}}},
                'TEN/IDR': {'id': 'ten_idr', 'symbol': 'TEN/IDR', 'base': 'TEN', 'quote': 'IDR', 'baseId': 'ten', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 5, 'max': None}}},
                'TRX/IDR': {'id': 'trx_idr', 'symbol': 'TRX/IDR', 'base': 'TRX', 'quote': 'IDR', 'baseId': 'trx', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': None, 'max': None}}},
                'WAVES/IDR': {'id': 'waves_idr', 'symbol': 'WAVES/IDR', 'base': 'WAVES', 'quote': 'IDR', 'baseId': 'waves', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.1, 'max': None}}},
                'XEM/IDR': {'id': 'nem_idr', 'symbol': 'XEM/IDR', 'base': 'XEM', 'quote': 'IDR', 'baseId': 'nem', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 1, 'max': None}}},
                'XLM/IDR': {'id': 'str_idr', 'symbol': 'XLM/IDR', 'base': 'XLM', 'quote': 'IDR', 'baseId': 'str', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 20, 'max': None}}},
                'XRP/IDR': {'id': 'xrp_idr', 'symbol': 'XRP/IDR', 'base': 'XRP', 'quote': 'IDR', 'baseId': 'xrp', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 10, 'max': None}}},
                'XZC/IDR': {'id': 'xzc_idr', 'symbol': 'XZC/IDR', 'base': 'XZC', 'quote': 'IDR', 'baseId': 'xzc', 'quoteId': 'idr', 'precision': {'amount': 8, 'price': 0}, 'limits': {'amount': {'min': 0.1, 'max': None}}},
                'BTS/BTC': {'id': 'bts_btc', 'symbol': 'BTS/BTC', 'base': 'BTS', 'quote': 'BTC', 'baseId': 'bts', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'DASH/BTC': {'id': 'drk_btc', 'symbol': 'DASH/BTC', 'base': 'DASH', 'quote': 'BTC', 'baseId': 'drk', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 6}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'DOGE/BTC': {'id': 'doge_btc', 'symbol': 'DOGE/BTC', 'base': 'DOGE', 'quote': 'BTC', 'baseId': 'doge', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 1, 'max': None}}},
                'ETH/BTC': {'id': 'eth_btc', 'symbol': 'ETH/BTC', 'base': 'ETH', 'quote': 'BTC', 'baseId': 'eth', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 5}, 'limits': {'amount': {'min': 0.001, 'max': None}}},
                'LTC/BTC': {'id': 'ltc_btc', 'symbol': 'LTC/BTC', 'base': 'LTC', 'quote': 'BTC', 'baseId': 'ltc', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 6}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'NXT/BTC': {'id': 'nxt_btc', 'symbol': 'NXT/BTC', 'base': 'NXT', 'quote': 'BTC', 'baseId': 'nxt', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'TEN/BTC': {'id': 'ten_btc', 'symbol': 'TEN/BTC', 'base': 'TEN', 'quote': 'BTC', 'baseId': 'ten', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'XEM/BTC': {'id': 'nem_btc', 'symbol': 'XEM/BTC', 'base': 'XEM', 'quote': 'BTC', 'baseId': 'nem', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 1, 'max': None}}},
                'XLM/BTC': {'id': 'str_btc', 'symbol': 'XLM/BTC', 'base': 'XLM', 'quote': 'BTC', 'baseId': 'str', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
                'XRP/BTC': {'id': 'xrp_btc', 'symbol': 'XRP/BTC', 'base': 'XRP', 'quote': 'BTC', 'baseId': 'xrp', 'quoteId': 'btc', 'precision': {'amount': 8, 'price': 8}, 'limits': {'amount': {'min': 0.01, 'max': None}}},
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'maker': 0,
                    'taker': 0.003,
                },
            },
            'exceptions': {
                'exact': {
                    'invalid_pair': BadRequest,  # {"error":"invalid_pair","error_description":"Invalid Pair"}
                    'Insufficient balance.': InsufficientFunds,
                    'invalid order.': OrderNotFound,
                    'Invalid credentials. API not found or session has expired.': AuthenticationError,
                    'Invalid credentials. Bad sign.': AuthenticationError,
                },
                'broad': {
                    'Minimum price': InvalidOrder,
                    'Minimum order': InvalidOrder,
                },
            },
        })

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetInfo(params)
        balances = self.safe_value(response, 'return', {})
        free = self.safe_value(balances, 'balance', {})
        used = self.safe_value(balances, 'balance_hold', {})
        result = {'info': response}
        currencyIds = list(free.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_float(free, currencyId)
            account['used'] = self.safe_float(used, currencyId)
            result[code] = account
        return self.parse_balance(result)

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair': self.market_id(symbol),
        }
        orderbook = self.publicGetPairDepth(self.extend(request, params))
        return self.parse_order_book(orderbook, None, 'buy', 'sell')

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
        }
        response = self.publicGetPairTicker(self.extend(request, params))
        ticker = response['ticker']
        timestamp = self.safe_float(ticker, 'server_time') * 1000
        baseVolume = 'vol_' + market['baseId'].lower()
        quoteVolume = 'vol_' + market['quoteId'].lower()
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'buy'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'sell'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': None,
            'average': None,
            'baseVolume': self.safe_float(ticker, baseVolume),
            'quoteVolume': self.safe_float(ticker, quoteVolume),
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is not None:
            timestamp *= 1000
        id = self.safe_string(trade, 'tid')
        symbol = None
        if market is not None:
            symbol = market['symbol']
        type = None
        side = self.safe_string(trade, 'type')
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if price is not None:
            if amount is not None:
                cost = price * amount
        return {
            'id': id,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'type': type,
            'side': side,
            'order': None,
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
            'pair': market['id'],
        }
        response = self.publicGetPairTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def parse_order(self, order, market=None):
        side = None
        if 'type' in order:
            side = order['type']
        status = self.safe_string(order, 'status', 'open')
        if status == 'filled':
            status = 'closed'
        elif status == 'calcelled':
            status = 'canceled'
        symbol = None
        cost = None
        price = self.safe_float(order, 'price')
        amount = None
        remaining = None
        filled = None
        if market is not None:
            symbol = market['symbol']
            quoteId = market['quoteId']
            baseId = market['baseId']
            if (market['quoteId'] == 'idr') and('order_rp' in list(order.keys())):
                quoteId = 'rp'
            if (market['baseId'] == 'idr') and('remain_rp' in list(order.keys())):
                baseId = 'rp'
            cost = self.safe_float(order, 'order_' + quoteId)
            if cost:
                amount = cost / price
                remainingCost = self.safe_float(order, 'remain_' + quoteId)
                if remainingCost is not None:
                    remaining = remainingCost / price
                    filled = amount - remaining
            else:
                amount = self.safe_float(order, 'order_' + baseId)
                cost = price * amount
                remaining = self.safe_float(order, 'remain_' + baseId)
                filled = amount - remaining
        average = None
        if filled:
            average = cost / filled
        timestamp = self.safe_integer(order, 'submit_time')
        fee = None
        id = self.safe_string(order, 'order_id')
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': None,
            'symbol': symbol,
            'type': 'limit',
            'side': side,
            'price': price,
            'cost': cost,
            'average': average,
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'status': status,
            'fee': fee,
        }

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrder requires a symbol')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'order_id': id,
        }
        response = self.privatePostGetOrder(self.extend(request, params))
        orders = response['return']
        order = self.parse_order(self.extend({'id': id}, orders['order']), market)
        return self.extend({'info': response}, order)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        market = None
        request = {}
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = self.privatePostOpenOrders(self.extend(request, params))
        rawOrders = response['return']['orders']
        # {success: 1, return: {orders: null}} if no orders
        if not rawOrders:
            return []
        # {success: 1, return: {orders: [... objects]}} for orders fetched by symbol
        if symbol is not None:
            return self.parse_orders(rawOrders, market, since, limit)
        # {success: 1, return: {orders: {marketid: [... objects]}}} if all orders are fetched
        marketIds = list(rawOrders.keys())
        exchangeOrders = []
        for i in range(0, len(marketIds)):
            marketId = marketIds[i]
            marketOrders = rawOrders[marketId]
            market = self.markets_by_id[marketId]
            parsedOrders = self.parse_orders(marketOrders, market, since, limit)
            exchangeOrders = self.array_concat(exchangeOrders, parsedOrders)
        return exchangeOrders

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ExchangeError(self.id + ' fetchOrders requires a symbol')
        self.load_markets()
        request = {}
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['pair'] = market['id']
        response = self.privatePostOrderHistory(self.extend(request, params))
        orders = self.parse_orders(response['return']['orders'], market, since, limit)
        orders = self.filter_by(orders, 'status', 'closed')
        if symbol is not None:
            return self.filter_by_symbol(orders, symbol)
        return orders

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        if type != 'limit':
            raise ExchangeError(self.id + ' allows limit orders only')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'pair': market['id'],
            'type': side,
            'price': price,
        }
        currency = market['baseId']
        if side == 'buy':
            request[market['quoteId']] = amount * price
        else:
            request[market['baseId']] = amount
        request[currency] = amount
        result = self.privatePostTrade(self.extend(request, params))
        return {
            'info': result,
            'id': str(result['return']['order_id']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder requires a symbol argument')
        side = self.safe_value(params, 'side')
        if side is None:
            raise ExchangeError(self.id + ' cancelOrder requires an extra "side" param')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'order_id': id,
            'pair': market['id'],
            'type': side,
        }
        return self.privatePostCancelOrder(self.extend(request, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        # Custom string you need to provide to identify each withdrawal.
        # Will be passed to callback URL(assigned via website to the API key)
        # so your system can identify the request and confirm it.
        # Alphanumeric, max length 255.
        requestId = self.milliseconds()
        # Alternatively:
        # requestId = self.uuid()
        request = {
            'currency': currency['id'],
            'withdraw_amount': amount,
            'withdraw_address': address,
            'request_id': str(requestId),
        }
        if tag:
            request['withdraw_memo'] = tag
        response = self.privatePostWithdrawCoin(self.extend(request, params))
        #
        #     {
        #         "success": 1,
        #         "status": "approved",
        #         "withdraw_currency": "xrp",
        #         "withdraw_address": "rwWr7KUZ3ZFwzgaDGjKBysADByzxvohQ3C",
        #         "withdraw_amount": "10000.00000000",
        #         "fee": "2.00000000",
        #         "amount_after_fee": "9998.00000000",
        #         "submit_time": "1509469200",
        #         "withdraw_id": "xrp-12345",
        #         "txid": "",
        #         "withdraw_memo": "123123"
        #     }
        #
        id = None
        if ('txid' in list(response.keys())) and len((response['txid']) > 0):
            id = response['txid']
        return {
            'info': response,
            'id': id,
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        if api == 'public':
            url += '/' + self.implode_params(path, params)
        else:
            self.check_required_credentials()
            body = self.urlencode(self.extend({
                'method': path,
                'nonce': self.nonce(),
            }, params))
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Key': self.apiKey,
                'Sign': self.hmac(self.encode(body), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response):
        if response is None:
            return
        # {success: 0, error: "invalid order."}
        # or
        # [{data, ...}, {...}, ...]
        if isinstance(response, list):
            return  # public endpoints may return []-arrays
        error = self.safe_value(response, 'error', '')
        if not('success' in list(response.keys())) and error == '':
            return  # no 'success' property on public responses
        if self.safe_integer(response, 'success', 0) == 1:
            # {success: 1, return: {orders: []}}
            if not('return' in list(response.keys())):
                raise ExchangeError(self.id + ': malformed response: ' + self.json(response))
            else:
                return
        feedback = self.id + ' ' + body
        exact = self.exceptions['exact']
        if error in exact:
            raise exact[error](feedback)
        broad = self.exceptions['broad']
        broadKey = self.findBroadlyMatchedKey(broad, error)
        if broadKey is not None:
            raise broad[broadKey](feedback)
        raise ExchangeError(feedback)  # unknown message
