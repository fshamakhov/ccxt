'use strict';

//  ---------------------------------------------------------------------------

const Exchange = require ('./base/Exchange');
const { ExchangeError, ArgumentsRequired, ExchangeNotAvailable, InsufficientFunds, AuthenticationError, PermissionDenied, BadRequest, InvalidOrder } = require ('./base/errors');

//  ---------------------------------------------------------------------------

module.exports = class bilaxy extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'bilaxy',
            'name': 'Bilaxy',
            'countries': ['CN'], // Japan, Malta
            'rateLimit': 500,
            'has': {
                'fetchDepositAddress': true,
                'createLimitOrder': true,
                'createMarketOrder': false,
                'createOrder': true,
                'fetchBalance': true,
                'fetchBidsAsks': true,
                'fetchClosedOrders': true,
                'fetchOpenOrders': true,
                'fetchOrder': true,
                'fetchOrders': true,
                'fetchTickers': true,
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
            'exceptions': {
                '101': { 'class': ArgumentsRequired, 'msg': 'The required parameters cannot be empty' },
                '102': { 'class': AuthenticationError, 'msg': 'API key dose not exist' },
                '103': { 'class': ExchangeError, 'msg': 'API is no longer used' },
                '104': { 'class': PermissionDenied, 'msg': 'Permissions closed' },
                '105': { 'class': PermissionDenied, 'msg': 'Insufficient authority' },
                '106': { 'class': AuthenticationError, 'msg': 'Signature mismatch' },
                '201': { 'class': BadRequest, 'msg': 'The asset does not exist' },
                '202': { 'class': BadRequest, 'msg': 'The asset cannot be deposit or withdraw' },
                '203': { 'class': ExchangeError, 'msg': 'The asset is not yet allocated to the wallet address' },
                '204': { 'class': ExchangeError, 'msg': 'Failed to cancel the order' },
                '205': { 'class': ExchangeError, 'msg': 'The transaction amount must not be less than 0.0001' },
                '206': { 'class': ExchangeError, 'msg': 'The transaction price must not be less than 0.0001' },
                '-100': { 'class': ExchangeError, 'msg': 'The transaction is lock' },
                '208': { 'class': InsufficientFunds, 'msg': 'Insufficient base currency balance' },
                '209': { 'class': AuthenticationError, 'msg': 'The transaction password is error' },
                '210': { 'class': BadRequest, 'msg': 'The transaction price is not within the limit price' },
                '-4': { 'class': InsufficientFunds, 'msg': 'Insufficient currency balance' },
                '212': { 'class': BadRequest, 'msg': 'The maximum amount of the transaction is limited' },
                '213': { 'class': BadRequest, 'msg': 'The minimum total amount of the transaction is limited' },
                '401': { 'class': BadRequest, 'msg': 'Illegal parameter' },
                '402': { 'class': ExchangeNotAvailable, 'msg': 'System error' },
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

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        let response = await this.privateGetBalances (params);
        let result = { 'info': response['data'] };
        let balances = response['data'];
        for (let i = 0; i < balances.length; i++) {
            let balance = balances[i];
            let currency = balance['name'];
            if (currency in this.currencies_by_id)
                currency = this.currencies_by_id[currency]['code'];
            let account = {
                'free': parseFloat (balance['balance']),
                'used': parseFloat (balance['frozen']),
                'total': 0.0,
            };
            account['total'] = this.sum (account['free'], account['used']);
            result[currency] = account;
        }
        return this.parseBalance (result);
    }

    handleErrors (code, reason, url, method, headers, body, response) {
        const exceptions = this.exceptions;
        const bilaxyCode = this.safeString (response, 'code');
        if (bilaxyCode in exceptions) {
            const ExceptionClass = exceptions[bilaxyCode]['class'];
            const message = exceptions[bilaxyCode]['msg'];
            throw new ExceptionClass (this.id + ' ' + message);
        }
    }

    async fetchOrder (id, symbol = undefined, params = {}) {
        if (symbol === undefined) {
            throw new ArgumentsRequired (this.id + ' fetchOrder requires a symbol argument');
        }
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'id': parseInt (id),
        };
        const response = await this.privateGetTradeView (this.extend (request, params));
        return this.parseOrder (response, market);
    }

    async fetchOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        if (symbol === undefined) {
            throw new ArgumentsRequired (this.id + ' fetchOrders requires a symbol argument');
        }
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'symbol': market['info']['symbol'],
            'type': 0, // => All orders
        };
        if (since !== undefined) {
            request['since'] = since;
        }
        const response = await this.privateGetTradeList (this.extend (request, params));
        return this.parseOrders (response['data'], market, since, limit);
    }

    async fetchOpenOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        const openParams = { 'type': 1 }; // 1 => Pending orders
        return await this.fetchOrders (symbol, since, limit, this.extend (openParams, params));
    }

    async fetchClosedOrders (symbol = undefined, since = undefined, limit = undefined, params = {}) {
        const orders = await this.fetchOrders (symbol, since, limit, params);
        return this.filterBy (orders, 'status', 3); // 3 => Traded completely
    }

    async cancelOrder (id, symbol = undefined, params = {}) {
        if (symbol === undefined) {
            throw new ArgumentsRequired (this.id + ' cancelOrder requires a symbol argument');
        }
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'id': parseInt (id),
        };
        const response = await this.privatePostCancelTrade (this.extend (request, params));
        const order = await this.privateGetTradeView ({ 'id': response['data'] });
        return this.parseOrder (order['data'], market);
    }

    parseOrderStatus (status) {
        const statusString = this.numberToString (status);
        const statuses = {
            '1': 'open',
            '2': 'open',
            '3': 'closed',
            '4': 'canceled',
        };
        return this.safeString (statuses, statusString, statusString);
    }

    parseOrder (order, market = undefined) {
        const status = this.parseOrderStatus (this.safeString (order, 'status'));
        let symbol = undefined;
        if (market) {
            symbol = market['symbol'];
        }
        let timestamp = undefined;
        let datetime = this.safeString (order, 'datetime');
        if (datetime) {
            timestamp = this.parse8601 (datetime);
        }
        const price = this.safeFloat (order, 'price');
        const amount = this.safeFloat (order, 'amount');
        const remaining = this.safeFloat (order, 'left_amount');
        let cost = undefined;
        let filled = undefined;
        if (remaining !== undefined) {
            if (amount !== undefined) {
                filled = amount - remaining;
                if (this.options['parseOrderToPrecision']) {
                    filled = parseFloat (this.amountToPrecision (symbol, filled));
                }
                filled = Math.max (filled, 0.0);
            }
            if ((price !== undefined) && (filled !== undefined)) {
                cost = price * filled;
            }
        }
        const id = this.safeString (order, 'id');
        const type = 'limit'; // Bilaxy has only limit orders
        let side = this.safeString (order, 'type');
        if (side !== undefined) {
            side = side.toLowerCase ();
        }
        let fee = undefined;
        let trades = undefined;
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': this.iso8601 (timestamp),
            'lastTradeTimestamp': undefined,
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
        };
    }

    async createOrder (symbol, type, side, amount, price = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        if (price === undefined) {
            throw new InvalidOrder (this.id + ' createOrder method requires a price argument');
        }
        const request = {
            'symbol': market['info']['symbol'],
            'amount': this.amountToPrecision (symbol, amount),
            'price': this.priceToPrecision (symbol, price),
            'type': side,
        };
        const response = await this.privatePostTrade (this.extend (request, params));
        const order = await this.privateGetTradeView ({ 'id': response['data'] });
        return this.parseOrder (order['data'], market);
    }

    async fetchDepositAddress (code, params = {}) {
        const balance = await this.fetchBalance ();
        await this.loadMarkets ();
        const currency = this.currency (code);
        let symbol = this.filterBy (balance['info'], 'name', currency['id']);
        if (symbol.length !== 1) {
            throw new ExchangeError (this.id + ' could not find currency with code ' + code);
        }
        symbol = symbol[0]['symbol'];
        const request = {
            'symbol': symbol,
        };
        const response = await this.privateGetCoinAddress (this.extend (request, params));
        const address = this.safeString (response, 'data');
        this.checkAddress (address);
        return {
            'currency': code,
            'address': address,
            'tag': undefined,
            'info': response,
        };
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
            const sorted = this.encode (this.urlencode (this.keysort (this.extend ({
                'key': this.apiKey,
                'secret': this.secret,
            }, params))));
            const signature = this.hash (sorted, 'sha1');
            const query = this.urlencode (this.keysort (this.extend ({
                'key': this.apiKey,
                'sign': signature,
            }, params)));
            // console.log ('params:', params, 'sorted:', sorted, 'query:', query);
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
