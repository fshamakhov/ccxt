# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import InvalidOrder


class mercado (Exchange):

    def describe(self):
        return self.deep_extend(super(mercado, self).describe(), {
            'id': 'mercado',
            'name': 'Mercado Bitcoin',
            'countries': ['BR'],  # Brazil
            'rateLimit': 1000,
            'version': 'v3',
            'has': {
                'CORS': True,
                'createMarketOrder': True,
                'fetchOrder': True,
                'withdraw': True,
                'fetchOHLCV': True,
                'fetchOrders': True,
                'fetchOpenOrders': True,
                'fetchTicker': True,
                'fetchTickers': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '2w': '2w',
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27837060-e7c58714-60ea-11e7-9192-f05e86adb83f.jpg',
                'api': {
                    'public': 'https://www.mercadobitcoin.net/api',
                    'private': 'https://www.mercadobitcoin.net/tapi',
                    'v4Public': 'https://www.mercadobitcoin.com.br/v4',
                },
                'www': 'https://www.mercadobitcoin.com.br',
                'doc': [
                    'https://www.mercadobitcoin.com.br/api-doc',
                    'https://www.mercadobitcoin.com.br/trade-api',
                ],
            },
            'api': {
                'public': {
                    'get': [
                        '{coin}/orderbook/',  # last slash critical
                        '{coin}/ticker/',
                        '{coin}/trades/',
                        '{coin}/trades/{from}/',
                        '{coin}/trades/{from}/{to}',
                        '{coin}/day-summary/{year}/{month}/{day}/',
                    ],
                },
                'private': {
                    'post': [
                        'cancel_order',
                        'get_account_info',
                        'get_order',
                        'get_withdrawal',
                        'list_system_messages',
                        'list_orders',
                        'list_orderbook',
                        'place_buy_order',
                        'place_sell_order',
                        'place_market_buy_order',
                        'place_market_sell_order',
                        'withdraw_coin',
                    ],
                },
                'v4Public': {
                    'get': [
                        '{coin}/candle/',
                    ],
                },
            },
            'markets': {
                'BTC/BRL': {'id': 'BRLBTC', 'symbol': 'BTC/BRL', 'base': 'BTC', 'quote': 'BRL', 'precision': {'amount': 8, 'price': 5}, 'suffix': 'Bitcoin'},
                'LTC/BRL': {'id': 'BRLLTC', 'symbol': 'LTC/BRL', 'base': 'LTC', 'quote': 'BRL', 'precision': {'amount': 8, 'price': 5}, 'suffix': 'Litecoin'},
                'BCH/BRL': {'id': 'BRLBCH', 'symbol': 'BCH/BRL', 'base': 'BCH', 'quote': 'BRL', 'precision': {'amount': 8, 'price': 5}, 'suffix': 'BCash'},
                'XRP/BRL': {'id': 'BRLXRP', 'symbol': 'XRP/BRL', 'base': 'XRP', 'quote': 'BRL', 'precision': {'amount': 8, 'price': 5}, 'suffix': 'Ripple'},
                'ETH/BRL': {'id': 'BRLETH', 'symbol': 'ETH/BRL', 'base': 'ETH', 'quote': 'BRL', 'precision': {'amount': 8, 'price': 5}, 'suffix': 'Ethereum'},
            },
            'fees': {
                'trading': {
                    'maker': 0.3 / 100,
                    'taker': 0.7 / 100,
                },
            },
        })

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['base'],
        }
        response = self.publicGetCoinOrderbook(self.extend(request, params))
        return self.parse_order_book(response)

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin': market['base'],
        }
        response = self.publicGetCoinTicker(self.extend(request, params))
        ticker = self.safe_value(response, 'ticker', {})
        timestamp = self.safe_integer(ticker, 'date')
        if timestamp is not None:
            timestamp *= 1000
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
            'baseVolume': self.safe_float(ticker, 'vol'),
            'quoteVolume': None,
            'info': ticker,
        }

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer(trade, 'date')
        if timestamp is not None:
            timestamp *= 1000
        symbol = None
        if market is not None:
            symbol = market['symbol']
        id = self.safe_string(trade, 'tid')
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
        method = 'publicGetCoinTrades'
        request = {
            'coin': market['base'],
        }
        if since is not None:
            method += 'From'
            request['from'] = int(since / 1000)
        to = self.safe_integer(params, 'to')
        if to is not None:
            method += 'To'
        response = getattr(self, method)(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostGetAccountInfo(params)
        data = self.safe_value(response, 'response_data', {})
        balances = self.safe_value(data, 'balance', {})
        result = {'info': response}
        currencyIds = list(balances.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safe_currency_code(currencyId)
            if currencyId in balances:
                balance = self.safe_value(balances, currencyId, {})
                account = self.account()
                account['free'] = self.safe_float(balance, 'available')
                account['total'] = self.safe_float(balance, 'total')
                result[code] = account
        return self.parse_balance(result)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'coin_pair': self.market_id(symbol),
        }
        method = self.capitalize(side) + 'Order'
        if type == 'limit':
            method = 'privatePostPlace' + method
            request['limit_price'] = self.price_to_precision(symbol, price)
            request['quantity'] = self.amount_to_precision(symbol, amount)
        else:
            method = 'privatePostPlaceMarket' + method
            if side == 'buy':
                if price is None:
                    raise InvalidOrder(self.id + ' createOrder() requires the price argument with market buy orders to calculate total order cost(amount to spend), where cost = amount * price. Supply a price argument to createOrder() call if you want the cost to be calculated for you from price and amount')
                request['cost'] = self.price_to_precision(symbol, amount * price)
            else:
                request['quantity'] = self.amount_to_precision(symbol, amount)
        response = getattr(self, method)(self.extend(request, params))
        # TODO: replace self with a call to parseOrder for unification
        return {
            'info': response,
            'id': str(response['response_data']['order']['order_id']),
        }

    def cancel_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'order_id': id,
        }
        response = self.privatePostCancelOrder(self.extend(request, params))
        #
        #     {
        #         response_data: {
        #             order: {
        #                 order_id: 2176769,
        #                 coin_pair: 'BRLBCH',
        #                 order_type: 2,
        #                 status: 3,
        #                 has_fills: False,
        #                 quantity: '0.10000000',
        #                 limit_price: '1996.15999',
        #                 executed_quantity: '0.00000000',
        #                 executed_price_avg: '0.00000',
        #                 fee: '0.00000000',
        #                 created_timestamp: '1536956488',
        #                 updated_timestamp: '1536956499',
        #                 operations: []
        #             }
        #         },
        #         status_code: 100,
        #         server_unix_timestamp: '1536956499'
        #     }
        #
        responseData = self.safe_value(response, 'response_data', {})
        order = self.safe_value(responseData, 'order', {})
        return self.parse_order(order, market)

    def parse_order_status(self, status):
        statuses = {
            '2': 'open',
            '3': 'canceled',
            '4': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        #
        #     {
        #         "order_id": 4,
        #         "coin_pair": "BRLBTC",
        #         "order_type": 1,
        #         "status": 2,
        #         "has_fills": True,
        #         "quantity": "2.00000000",
        #         "limit_price": "900.00000",
        #         "executed_quantity": "1.00000000",
        #         "executed_price_avg": "900.00000",
        #         "fee": "0.00300000",
        #         "created_timestamp": "1453838494",
        #         "updated_timestamp": "1453838494",
        #         "operations": [
        #             {
        #                 "operation_id": 1,
        #                 "quantity": "1.00000000",
        #                 "price": "900.00000",
        #                 "fee_rate": "0.30",
        #                 "executed_timestamp": "1453838494",
        #             },
        #         ],
        #     }
        #
        id = self.safe_string(order, 'order_id')
        side = None
        if 'order_type' in order:
            side = 'buy' if (order['order_type'] == 1) else 'sell'
        status = self.parse_order_status(self.safe_string(order, 'status'))
        symbol = None
        if market is None:
            marketId = self.safe_string(order, 'coin_pair')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(order, 'created_timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
        fee = {
            'cost': self.safe_float(order, 'fee'),
            'currency': market['quote'],
        }
        price = self.safe_float(order, 'limit_price')
        # price = self.safe_float(order, 'executed_price_avg', price)
        average = self.safe_float(order, 'executed_price_avg')
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'executed_quantity')
        remaining = amount - filled
        cost = filled * average
        lastTradeTimestamp = self.safe_integer(order, 'updated_timestamp')
        if lastTradeTimestamp is not None:
            lastTradeTimestamp = lastTradeTimestamp * 1000
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': lastTradeTimestamp,
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
            'trades': None,  # todo parse trades(operations)
        }

    def fetch_order(self, id, symbol=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
            'order_id': int(id),
        }
        response = self.privatePostGetOrder(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        order = self.safe_value(responseData, 'order')
        return self.parse_order(order, market)

    def withdraw(self, code, amount, address, tag=None, params={}):
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'coin': currency['id'],
            'quantity': '{:.10f}'.format(amount),
            'address': address,
        }
        if code == 'BRL':
            account_ref = ('account_ref' in list(params.keys()))
            if not account_ref:
                raise ExchangeError(self.id + ' requires account_ref parameter to withdraw ' + code)
        elif code != 'LTC':
            tx_fee = ('tx_fee' in list(params.keys()))
            if not tx_fee:
                raise ExchangeError(self.id + ' requires tx_fee parameter to withdraw ' + code)
            if code == 'XRP':
                if tag is None:
                    if not('destination_tag' in list(params.keys())):
                        raise ExchangeError(self.id + ' requires a tag argument or destination_tag parameter to withdraw ' + code)
                else:
                    request['destination_tag'] = tag
        response = self.privatePostWithdrawCoin(self.extend(request, params))
        return {
            'info': response,
            'id': response['response_data']['withdrawal']['id'],
        }

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        timestamp = self.safe_integer(ohlcv, 'timestamp')
        if timestamp is not None:
            timestamp = timestamp * 1000
        return [
            timestamp,
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'volume'),
        ]

    def fetch_ohlcv(self, symbol, timeframe='5m', since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'precision': self.timeframes[timeframe],
            'coin': market['id'].lower(),
        }
        if limit is not None and since is not None:
            request['from'] = int(since / 1000)
            request['to'] = self.sum(request['from'], limit * self.parse_timeframe(timeframe))
        elif since is not None:
            request['from'] = int(since / 1000)
            request['to'] = self.sum(self.seconds(), 1)
        elif limit is not None:
            request['to'] = self.seconds()
            request['from'] = request['to'] - (limit * self.parse_timeframe(timeframe))
        response = self.v4PublicGetCoinCandle(self.extend(request, params))
        candles = self.safe_value(response, 'candles', [])
        return self.parse_ohlcvs(candles, market, timeframe, since, limit)

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrders() requires a symbol argument')
        self.load_markets()
        market = self.market(symbol)
        request = {
            'coin_pair': market['id'],
        }
        response = self.privatePostListOrders(self.extend(request, params))
        responseData = self.safe_value(response, 'response_data', {})
        orders = self.safe_value(responseData, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api] + '/'
        query = self.omit(params, self.extract_params(path))
        if api == 'public' or (api == 'v4Public'):
            url += self.implode_params(path, params)
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            url += self.version + '/'
            nonce = self.nonce()
            body = self.urlencode(self.extend({
                'tapi_method': path,
                'tapi_nonce': nonce,
            }, params))
            auth = '/tapi/' + self.version + '/' + '?' + body
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'TAPI-ID': self.apiKey,
                'TAPI-MAC': self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha512),
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        response = self.fetch2(path, api, method, params, headers, body)
        if 'error_message' in response:
            raise ExchangeError(self.id + ' ' + self.json(response))
        return response
