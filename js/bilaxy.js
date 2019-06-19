'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
const { ExchangeError } = require ('./base/errors');

//  ---------------------------------------------------------------------------

module.exports = class bilaxy extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'bilaxy',
            'name': 'Bilaxy',
            'countries': ['CN'], // Japan, Malta
            'rateLimit': 500,
            'has': {
                'fetchDepositAddress': false,
                'CORS': false,
                'fetchBidsAsks': true,
                'fetchTickers': true,
                'fetchOHLCV': false,
                'fetchMyTrades': false,
                'fetchOrder': true,
                'fetchOrders': true,
                'fetchOpenOrders': true,
                'fetchClosedOrders': true,
                'withdraw': false,
                'fetchFundingFees': false,
                'fetchDeposits': false,
                'fetchWithdrawals': false,
                'fetchTransactions': false,
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
                    'tierBased': false,
                    'percentage': true,
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
        });
    }

    async fetchMarkets (params = {}) {
        let response = await this.publicGetCoins ();
        let markets = response['data'];
        let result = [];
        for (let i = 0; i < markets.length; i++) {
            let market = markets[i];
            let id = market['name'] + market['group'];
            let baseId = market['name'];
            let quoteId = market['group'];
            let base = this.commonCurrencyCode (baseId);
            let quote = this.commonCurrencyCode (quoteId);
            let symbol = base + '/' + quote;
            let precision = {
                'base': market['priceDecimals'],
                'quote': market['priceDecimals'],
                'amount': market['priceDecimals'],
                'price': market['priceDecimals'],
            };
            let active = true;
            this.bilaxySymbols[symbol] = market['symbol'];
            let entry = {
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
                        'min': undefined,
                        'max': undefined,
                    },
                    'price': {
                        'min': undefined,
                        'max': undefined,
                    },
                    'cost': {
                        'min': 0.01,
                        'max': undefined,
                    },
                },
            };
            result.push (entry);
        }
        return result;
    }

    getBilaxySymbol (symbol) {
        if (this.bilaxySymbols === undefined) {
            throw new ExchangeError (this.id + ' markets not loaded');
        }
        if ((typeof symbol === 'string') && (symbol in this.bilaxySymbols)) {
            return this.bilaxySymbols[symbol];
        }
        throw new ExchangeError (this.id + ' does not have market symbol ' + symbol);
    }

    getSymbolFromBilaxy (symbol) {
        if (this.bilaxySymbols === undefined) {
            throw new ExchangeError (this.id + ' markets not loaded');
        }
        let keys = Object.keys (this.bilaxySymbols);
        for (let i = 0; i < keys.length; i++) {
            let id = keys[i];
            if (this.bilaxySymbols[id] === symbol) {
                return id;
            }
        }
        throw new ExchangeError (this.id + ' does not have market symbol');
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        let bilaxy_symbol = this.getBilaxySymbol (symbol);
        let request = {
            'symbol': bilaxy_symbol,
        };
        let response = await this.publicGetDepth (this.extend (request, params));
        return this.parseOrderBook (response['data']);
    }

    parseTicker (symbol, ticker, market = undefined) {
        let last = this.safeFloat (ticker, 'last');
        return {
            'symbol': symbol,
            'timestamp': undefined,
            'datetime': undefined,
            'high': this.safeFloat (ticker, 'high'),
            'low': this.safeFloat (ticker, 'low'),
            'bid': this.safeFloat (ticker, 'buy'),
            'bidVolume': this.safeFloat (ticker, 'vol'),
            'ask': this.safeFloat (ticker, 'sell'),
            'askVolume': this.safeFloat (ticker, 'vol'),
            'vwap': undefined,
            'open': undefined,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': undefined,
            'percentage': undefined,
            'average': undefined,
            'baseVolume': undefined,
            'quoteVolume': undefined,
            'info': ticker,
        };
    }

    async fetchTicker (symbol, params = {}) {
        let bilaxy_symbol = this.getBilaxySymbol (symbol);
        let response = await this.publicGetTicker (this.extend ({
            'symbol': bilaxy_symbol,
        }, params));
        await this.loadMarkets ();
        let market = this.market (symbol);
        return this.parseTicker (symbol, response['data'], market);
    }

    async parseTickers (rawTickers, symbols = undefined) {
        await this.loadMarkets ();
        let tickers = [];
        for (let i = 0; i < rawTickers.length; i++) {
            let symbol = this.getSymbolFromBilaxy (rawTickers[i]['symbol']);
            let market = this.market (symbol);
            tickers.push (this.parseTicker (symbol, rawTickers[i], market));
        }
        return this.filterByArray (tickers, 'symbol', symbols);
    }

    async fetchTickers (symbols = undefined, params = {}) {
        await this.loadMarkets ();
        let rawTickers = await this.publicGetTickers (params);
        return await this.parseTickers (rawTickers['data'], symbols);
    }

    parseTrade (trade, market = undefined) {
        const timestamp = this.safeInteger (trade, 'date');
        const price = this.safeFloat (trade, 'price');
        const amount = this.safeFloat (trade, 'count');
        const id = this.safeString (trade, 'id');
        const side = this.safeString (trade, 'type');
        const cost = this.safeFloat (trade, 'amount');
        let symbol = undefined;
        if (market !== undefined) {
            symbol = market['symbol'];
        }
        return {
            'info': trade,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'symbol': symbol,
            'id': id,
            'order': undefined,
            'type': undefined,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
        };
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'symbol': market['info']['symbol'],
        };
        if (limit !== undefined) {
            request['size'] = limit; // default = 100, maximum = 000
        }
        const response = await this.publicGetOrders (this.extend (request, params));
        return this.parseTrades (response['data'], market, undefined, limit);
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'][api];
        url += '/' + path;
        if ((api === 'public') || (api === 'v2')) {
            if (Object.keys (params).length)
                url += '?' + this.urlencode (params);
            if (api === 'v2')
                headers = { 'accept': 'application/json' };
        } else {
            this.checkRequiredCredentials ();
            let signature = this.urlencode (this.keysort (this.extend ({
                'key': this.apiKey,
                'secret': this.secret,
            }, params)));
            signature = this.hash (this.encode (signature), 'sha1');
            let query = this.urlencode (this.keysort (this.extend ({
                'key': this.apiKey,
            }, params)));
            query += '&' + 'sign=' + signature;
            if (method === 'GET') {
                url += '?' + query;
            } else {
                body = query;
                headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
            }
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }
};
