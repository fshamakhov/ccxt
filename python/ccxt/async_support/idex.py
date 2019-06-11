# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError


class idex (Exchange):

    def describe(self):
        return self.deep_extend(super(idex, self).describe(), {
            'id': 'idex',
            'name': 'Idex',
            'countries': ['JP', 'MT'],  # Japan, Malta
            'rateLimit': 500,
            'has': {
                'fetchDepositAddress': False,
                'CORS': False,
                'fetchBidsAsks': True,
                'fetchTickers': True,
                'fetchOHLCV': False,
                'fetchMyTrades': False,
                'fetchOrder': True,
                'fetchOrders': False,
                'fetchOpenOrders': True,
                'fetchClosedOrders': True,
                'withdraw': False,
                'fetchFundingFees': False,
                'fetchDeposits': False,
                'fetchWithdrawals': False,
                'fetchTransactions': False,
            },
            'urls': {
                'logo': 'https://idex.market/assets/IDEX_sf-color.svg',
                'api': {
                    'web': 'https://idex.market',
                    'public': 'https://api.idex.market',
                    'private': 'https://api.idex.market',
                },
                'www': 'https://idex.market',
                'doc': 'https://docs.idex.market',
            },
            'api': {
                'public': {
                    'get': [
                        'returnTicker',  # "market": "ETH_SAN"
                        'returnCurrencies',
                        'return24Volume',
                        'returnOrderBook',  # "market": "ETH_AURA", "count": 1
                    ],
                    'post': [
                        'returnTicker',  # "market": "ETH_SAN"
                        'returnCurrencies',
                        'return24Volume',
                        'returnOrderBook',  # "market": "ETH_AURA", "count": 1
                    ],
                },
                'private': {
                    'post': [
                        'returnBalances',  # "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208",
                        'returnCompleteBalances',  # "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
                        'returnDepositsWithdrawals',  # "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208", "start": 0, "end": 0
                        'returnOpenOrders',  # "market": "ETH_AURA", "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208", "count": 10, "cursor": "2228127"
                        'returnOrderStatus',  # "orderHash": "0x22a9ba7f8dd37ed24ae327b14a8a941b0eb072d60e54bcf24640c2af819fc7ec"
                        'returnOrderTrades',  # "orderHash": "0x22a9ba7f8dd37ed24ae327b14a8a941b0eb072d60e54bcf24640c2af819fc7ec"
                        'returnTradeHistory',  # "market": "ETH_AURA", "address": "0x2dbdcec64db33e673140fbd0ceef610a273b84db", "start": 5000, "end": 10000, "sort": "desc", "count": 10, "cursor": "1000"
                        'returnContractAddress',  # "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
                        'returnNextNonce',  # "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
                        'order',  # https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-order-payload.js
                        'cancel',  # https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-cancel-payload.js
                        'trade',  # https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-trade-payload.js
                        'withdraw',
                    ],
                },
            },
            'requiredCredentials': {
                'apiKey': False,
                'secret': False,
                'uid': False,
                'login': False,
                'password': False,
                'twofa': False,  # 2-factor authentication(one-time password key)
                'privateKey': True,  # a "0x"-prefixed hexstring private key for a wallet
                'walletAddress': True,  # the wallet address "0x"-prefixed hexstring
                'token': False,  # reserved for HTTP auth in some cases,
                'idexContractAddress': True,
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.002,
                    'maker': 0.001,
                },
            },
            'idexContractAddress': None,
            'commonCurrencies': {
                'GET': 'GET Protocol',
                'GET2': 'GET',
                'AIC': 'AKAI',
                'BTT': 'Blocktrade Token',
                'ONE': 'Menlo One',
                'ONG': 'SoMee.Social',
                'SMT': 'Sun Money Token',
                'VNT': 'Vanta Network',
                'PRO': 'ProChain',
                'PRO2': 'PRO',
                'TFT': 'Travelling Free Token',
                'BLUE': 'Ethereum Blue',
                'ACC': 'Accelerator',
                'CAT2': 'BitClave',
            },
            'currencyAddresses': None,
        })

    def get_currency(self, currency=''):
        if currency in self.currencyAddresses:
            return self.currencyAddresses[currency]
        raise ExchangeError('Exchange ' + self.id + 'currency ' + currency + ' not found')

    async def fetch_markets(self, params={}):
        self.currencyAddresses = await self.publicGetReturnCurrencies(params)
        response = await self.publicGetReturnTicker()
        symbols = list(response.keys())
        result = []
        for i in range(0, len(symbols)):
            id = symbols[i]
            market = response[id]
            ids = id.split('_')
            baseId = ids[1].upper()
            quoteId = ids[0].upper()
            baseCurrency = self.get_currency(baseId)
            quoteCurrency = self.get_currency(quoteId)
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            precision = {
                'base': baseCurrency['decimals'],
                'quote': quoteCurrency['decimals'],
            }
            active = True
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
                        'min': 0.15,
                        'max': None,
                    },
                },
            }
            result.append(entry)
        return result

    async def fetch_order_book(self, symbol, limit=None, params={}):
        if limit is None:
            limit = 100
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
            'count': limit,
        }
        order_book = await self.publicGetReturnOrderBook(self.extend(request, params))
        return self.parse_order_book(order_book, None, 'bids', 'asks', 'price', 'amount')

    def parse_ticker(self, symbol, ticker, market=None):
        last = self.safe_float(ticker, 'last')
        return {
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'highestBid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'lowestAsk'),
            'askVolume': None,
            'vwap': None,
            'open': None,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_float(ticker, 'percentChange'),
            'average': None,
            'baseVolume': self.safe_float(ticker, 'baseVolume'),
            'quoteVolume': self.safe_float(ticker, 'quoteVolume'),
            'info': ticker,
        }

    async def fetch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'market': market['id'],
        }
        response = await self.publicGetReturnTicker(self.extend(request, params))
        return self.parse_ticker(symbol, response, market)

    async def parse_tickers(self, rawTickers, symbols=None):
        await self.load_markets()
        keys = list(rawTickers.keys())
        tickers = []
        for i in range(0, len(keys)):
            id = keys[i]
            ids = id.split('_')
            baseId = ids[1].upper()
            quoteId = ids[0].upper()
            base = self.common_currency_code(baseId)
            quote = self.common_currency_code(quoteId)
            symbol = base + '/' + quote
            market = self.market(symbol)
            tickers.append(self.parse_ticker(symbol, rawTickers[id], market))
        return self.filter_by_array(tickers, 'symbol', symbols)

    async def fetch_tickers(self, symbols=None, params={}):
        await self.load_markets()
        rawTickers = await self.publicGetReturnTicker(params)
        return await self.parse_tickers(rawTickers, symbols)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'][api]
        url += '/' + path
        if method == 'GET':
            if params:
                url += '?' + self.urlencode(params)
        else:
            headers['Content-Type'] = 'application/json'
            if api != 'public':
                self.check_required_credentials()
            body = self.json(params)
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
