'use strict';

//  ---------------------------------------------------------------------------

const { ExchangeError, InvalidOrder } = require ('./base/errors');
const Exchange = require ('./base/Exchange');
//  ---------------------------------------------------------------------------

module.exports = class idex extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'idex',
            'name': 'Idex',
            'countries': [ 'JP', 'MT' ], // Japan, Malta
            'rateLimit': 500,
            'has': {
                'createLimitOrder': false,
                'createMarketOrder': false,
                'fetchTickers': true,
                'withdraw': true,
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
                        'returnTicker', // "market": "ETH_SAN"
                        'returnCurrencies',
                        'return24Volume',
                        'returnOrderBook', // "market": "ETH_AURA", "count": 1
                    ],
                    'post': [
                        'returnTicker', // "market": "ETH_SAN"
                        'returnCurrencies',
                        'return24Volume',
                        'returnOrderBook', // "market": "ETH_AURA", "count": 1
                        'returnContractAddress',
                        'returnTradeHistory', // "market": "ETH_AURA", "address": "0x2dbdcec64db33e673140fbd0ceef610a273b84db", "start": 5000, "end": 10000, "sort": "desc", "count": 10, "cursor": "1000"
                    ],
                },
                'private': {
                    'post': [
                        'returnBalances', // "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208",
                        'returnCompleteBalances', // "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
                        'returnDepositsWithdrawals', // "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208", "start": 0, "end": 0
                        'returnOpenOrders', // "market": "ETH_AURA", "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208", "count": 10, "cursor": "2228127"
                        'returnOrderStatus', // "orderHash": "0x22a9ba7f8dd37ed24ae327b14a8a941b0eb072d60e54bcf24640c2af819fc7ec"
                        'returnOrderTrades', // "orderHash": "0x22a9ba7f8dd37ed24ae327b14a8a941b0eb072d60e54bcf24640c2af819fc7ec"
                        'returnNextNonce', // "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
                        'order', // https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-order-payload.js
                        'cancel', // https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-cancel-payload.js
                        'trade', // https://github.com/AuroraDAO/idex-api-docs/blob/master/scripts/generate-trade-payload.js
                        'withdraw',
                    ],
                },
            },
            'requiredCredentials': {
                'apiKey': false,
                'secret': false,
                'uid': false,
                'login': false,
                'password': false,
                'twofa': false, // 2-factor authentication (one-time password key)
                'privateKey': true, // a "0x"-prefixed hexstring private key for a wallet
                'walletAddress': true, // the wallet address "0x"-prefixed hexstring
                'token': false, // reserved for HTTP auth in some cases,
                'idexContractAddress': true,
            },
            'fees': {
                'trading': {
                    'tierBased': false,
                    'percentage': true,
                    'taker': 0.002,
                    'maker': 0.001,
                },
            },
            'idexContractAddress': undefined,
            'commonCurrencies': {
                'ACC': 'Accelerator',
                'AIC': 'AKAI',
                'AMB': 'Amber',
                'BIO': 'BioCrypt',
                'BLUE': 'Ethereum Blue',
                'BST': 'Blocksquare Token',
                'BTT': 'Blocktrade Token',
                'CAT2': 'BitClave',
                'CCC': 'Container Crypto Coin',
                'CRE': 'Carry',
                'CST': 'Cryptosolartech',
                'EXO': 'EXOLOVER',
                'GBX': 'Globitex',
                'GENE': 'Gene Source Code Chain',
                'GET': 'GET Protocol',
                'GET2': 'GET',
                'IPL': 'InsurePal',
                'NTK2': 'NetKoin',
                'ONE': 'Menlo One',
                'ONG': 'SoMee.Social',
                'PDX': 'PdxToken',
                'PRO': 'ProChain',
                'PRO2': 'PRO',
                'SAT': 'Satisfaction Token',
                'SET': 'Swytch Energy Token',
                'SMT': 'Sun Money Token',
                'TFT': 'Travelling Free Token',
                'VNT': 'Vanta Network',
                'WCT': 'Wealth Chain Token',
            },
            'currencyAddresses': undefined,
            'enableLastResponseHeaders': true,
            'requiresWeb3': true,
        });
    }

    async fetchContractAddress () {
        const response = await this.publicPostReturnContractAddress ();
        if ('address' in response) {
            this.idexContractAddress = response['address'];
        }
    }

    getCurrency (currency = '') {
        if (currency in this.currencyAddresses) {
            return this.extend ({ 'symbol': currency }, this.currencyAddresses[currency]);
        }
        throw new ExchangeError ('Exchange ' + this.id + 'currency ' + currency + ' not found');
    }

    async fetchMarkets (params = {}) {
        this.currencyAddresses = await this.publicGetReturnCurrencies (params);
        let response = await this.publicGetReturnTicker ();
        await this.fetchContractAddress ();
        let symbols = Object.keys (response);
        let result = [];
        for (let i = 0; i < symbols.length; i++) {
            let id = symbols[i];
            let market = response[id];
            let ids = id.split ('_');
            let baseId = ids[1].toUpperCase ();
            let quoteId = ids[0].toUpperCase ();
            let baseCurrency = this.getCurrency (baseId);
            let quoteCurrency = this.getCurrency (quoteId);
            let base = this.commonCurrencyCode (baseId);
            let quote = this.commonCurrencyCode (quoteId);
            let symbol = base + '/' + quote;
            let precision = {
                'base': baseCurrency['decimals'],
                'quote': quoteCurrency['decimals'],
            };
            let active = true;
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
                        'min': 0.15,
                        'max': undefined,
                    },
                },
            };
            result.push (entry);
        }
        return result;
    }

    async fetchOrderBook (symbol, limit = undefined, params = {}) {
        if (limit === undefined) {
            limit = 100;
        }
        await this.loadMarkets ();
        let market = this.market (symbol);
        let request = {
            'market': market['id'],
            'count': limit,
        };
        let orderbook = await this.publicGetReturnOrderBook (this.extend (request, params));
        return this.parseOrderBook (orderbook, undefined, 'bids', 'asks', 'price', 'amount');
    }

    parseTicker (symbol, ticker, market = undefined) {
        let last = this.safeFloat (ticker, 'last');
        return {
            'symbol': symbol,
            'timestamp': undefined,
            'datetime': undefined,
            'high': this.safeFloat (ticker, 'high'),
            'low': this.safeFloat (ticker, 'low'),
            'bid': this.safeFloat (ticker, 'highestBid'),
            'bidVolume': undefined,
            'ask': this.safeFloat (ticker, 'lowestAsk'),
            'askVolume': undefined,
            'vwap': undefined,
            'open': undefined,
            'close': last,
            'last': last,
            'previousClose': undefined,
            'change': undefined,
            'percentage': this.safeFloat (ticker, 'percentChange'),
            'average': undefined,
            'baseVolume': this.safeFloat (ticker, 'baseVolume'),
            'quoteVolume': this.safeFloat (ticker, 'quoteVolume'),
            'info': ticker,
        };
    }

    async fetchTicker (symbol, params = {}) {
        await this.loadMarkets ();
        let market = this.market (symbol);
        let request = {
            'market': market['id'],
        };
        let response = await this.publicGetReturnTicker (this.extend (request, params));
        return this.parseTicker (symbol, response, market);
    }

    async parseTickers (rawTickers, symbols = undefined) {
        await this.loadMarkets ();
        let keys = Object.keys (rawTickers);
        let tickers = [];
        for (let i = 0; i < keys.length; i++) {
            let id = keys[i];
            let ids = id.split ('_');
            let baseId = ids[1].toUpperCase ();
            let quoteId = ids[0].toUpperCase ();
            let base = this.commonCurrencyCode (baseId);
            let quote = this.commonCurrencyCode (quoteId);
            let symbol = base + '/' + quote;
            let market = this.market (symbol);
            tickers.push (this.parseTicker (symbol, rawTickers[id], market));
        }
        return this.filterByArray (tickers, 'symbol', symbols);
    }

    async fetchTickers (symbols = undefined, params = {}) {
        await this.loadMarkets ();
        let rawTickers = await this.publicGetReturnTicker (params);
        return await this.parseTickers (rawTickers, symbols);
    }

    parseTrade (trade, market = undefined) {
        const id = this.safeString (trade, 'uuid');
        const timestamp = this.safeString (trade, 'timestamp');
        const datetime = this.safeString (trade, 'date');
        let symbol = undefined;
        if (market !== undefined) {
            symbol = market['symbol'];
        }
        const order = this.safeString (trade, 'tid');
        let type = this.safeString (trade, 'type');
        if (type) {
            type = type.toLowerCase ();
        }
        const side = undefined;
        const price = this.safeFloat (trade, 'price');
        const amount = this.safeFloat (trade, 'amount');
        const cost = this.safeFloat (trade, 'total');
        return {
            'info': trade,
            'id': id,
            'timestamp': timestamp,
            'datetime': datetime,
            'symbol': symbol,
            'order': order,
            'type': type,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': cost,
        };
    }

    async fetchBalance (params = {}) {
        await this.loadMarkets ();
        const request = { 'address': this.walletAddress };
        let response = await this.privatePostReturnCompleteBalances (this.extend (request, params));
        let result = { 'info': response };
        const currencies = Object.keys (response);
        for (let i = 0; i < currencies.length; i++) {
            const currency = currencies[i];
            const balance = response[currency];
            let account = {
                'free': parseFloat (balance['available']),
                'used': parseFloat (balance['onOrders']),
                'total': 0,
            };
            account['total'] = this.sum (account['free'], account['used']);
            result[currency] = account;
        }
        return this.parseBalance (result);
    }

    async fetchTrades (symbol, since = undefined, limit = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        const request = {
            'market': market['id'],
        };
        if (since !== undefined) {
            request['start'] = since;
        }
        if (limit !== undefined) {
            request['count'] = limit; // default = 10, maximum = 100
        }
        const response = await this.publicPostReturnTradeHistory (this.extend (request, params));
        return this.parseTrades (response, market, since, limit);
    }

    parseOrder (order, market = undefined) {
        const status = undefined;
        const symbol = this.findSymbol (this.safeString (order, 'market'), market);
        let timestamp = undefined;
        let datetime = undefined;
        if ('timestamp' in order) {
            timestamp = this.safeInteger (order, 'timestamp');
        } else if ('date' in order) {
            datetime = this.safeString (order, 'date');
            timestamp = this.parse8601 (datetime);
        }
        let price = this.safeFloat (order, 'price');
        const amount = this.safeFloat (order, 'amount');
        const filled = undefined;
        let remaining = undefined;
        let cost = this.safeFloat (order, 'total');
        const id = this.safeString (order, 'orderHash');
        let type = undefined;
        let side = this.safeString (order, 'type');
        if (side !== undefined) {
            side = side.toLowerCase ();
        }
        let fee = undefined;
        return {
            'info': order,
            'id': id,
            'timestamp': timestamp,
            'datetime': datetime,
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
        };
    }

    getSignedRequestParams (args, raw) {
        const salted = this.hashMessage (raw).slice (2); // according to example salted message should be without leading 0x substring
        const vrs = this.signHash (salted, this.privateKey);
        const request = this.extend (args, vrs);
        return request;
    }

    async idexOrder (base, quote, side, amount, price, nonce, params = {}) {
        const amountFloat = parseFloat (amount);
        const priceFloat = parseFloat (price);
        let tokenBuy = undefined;
        let tokenSell = undefined;
        let amountBuy = undefined;
        let amountSell = undefined;
        if (side === 'buy') {
            tokenBuy = base['address'];
            tokenSell = quote['address'];
            amountBuy = this.toWei (amount);
            amountSell = this.toWei (amountFloat * priceFloat);
        } else if (side === 'sell') {
            tokenBuy = quote['address'];
            tokenSell = base['address'];
            amountBuy = this.toWei (amountFloat * priceFloat);
            amountSell = this.toWei (amount);
        } else {
            throw new InvalidOrder (this.id + ' invalid value for side: ' + side);
        }
        let expires = 10000;
        if ('expires' in params) {
            expires = params['expires'];
        }
        const args = {
            'tokenBuy': tokenBuy,
            'amountBuy': amountBuy,
            'tokenSell': tokenSell,
            'amountSell': amountSell,
            'address': this.walletAddress,
            'nonce': nonce,
            'expires': expires,
        };
        const raw = this.soliditySha3 ([
            this.idexContractAddress,
            args['tokenBuy'],
            args['amountBuy'],
            args['tokenSell'],
            args['amountSell'],
            args['expires'],
            args['nonce'],
            args['address'],
        ]);
        const request = this.getSignedRequestParams (args, raw);
        return await this.privatePostOrder (request);
    }

    prepareOrderForTrade (orderAmount, openOrder, nonce) {
        const args = {
            'orderHash': openOrder['orderHash'],
            'amount': this.toWei (orderAmount),
            'nonce': nonce,
            'address': this.walletAddress,
        };
        const raw = this.soliditySha3 ([
            args['orderHash'],
            args['amount'],
            args['address'],
            args['nonce'],
        ]);
        const request = this.getSignedRequestParams (args, raw);
        // console.log ('args: ', args, 'raw: ', raw, 'request: ', request);
        return request;
    }

    async idexTrade (base, quote, side, amount, nonce, params = {}) {
        const amountFloat = parseFloat (amount);
        const symbol = base['symbol'] + '/' + quote['symbol'];
        let market = this.market (symbol);
        const request = {
            'market': market['id'],
            'count': 100,
        };
        const orderbook = await this.publicGetReturnOrderBook (request);
        let orderbookKey = undefined;
        if (side === 'buy') {
            orderbookKey = 'asks';
        } else if (side === 'sell') {
            orderbookKey = 'bids';
        } else {
            throw new InvalidOrder (this.id + ' invalid side value: ' + side);
        }
        let totalAmount = 0;
        let orders = [];
        for (let i = 0; i < orderbook[orderbookKey].length; i++) {
            if (totalAmount >= amountFloat) {
                break;
            }
            let openOrder = orderbook[orderbookKey][i];
            let orderAmount = this.safeFloat (openOrder, 'amount');
            if (orderAmount === undefined) {
                continue;
            }
            if (totalAmount + orderAmount > amount) {
                orderAmount = totalAmount - amount;
            }
            totalAmount += orderAmount;
            const newOrder = this.prepareOrderForTrade (orderAmount, openOrder, nonce);
            orders.push (newOrder);
        }
        console.log ('totalAmount: ', totalAmount);
        // return await this.privatePostTrade (orders);
    }

    async fetchNextNonce () {
        let nonce = undefined;
        const nonceResponse = await this.privatePostReturnNextNonce ({ 'address': this.walletAddress });
        if ('nonce' in nonceResponse) {
            nonce = nonceResponse['nonce'];
        }
        return nonce;
    }

    async createOrder (symbol, type, side, amount, price = undefined, params = {}) {
        await this.loadMarkets ();
        const market = this.market (symbol);
        // the next 5 lines are added to support for testing orders
        const nonce = await this.fetchNextNonce ();
        let currencies = symbol.split ('/');
        const base = this.getCurrency (currencies[0]);
        const quote = this.getCurrency (currencies[1]);
        const uppercaseType = type.toUpperCase ();
        let response = undefined;
        let result = undefined;
        if ((uppercaseType === 'LIMIT') && (price !== undefined)) {
            response = await this.idexOrder (base, quote, side, amount, price, nonce, params);
            result = this.parseOrder (response, market);
        } else if (uppercaseType === 'MARKET') {
            response = await this.idexTrade (base, quote, side, amount, nonce, params);
            result = [];
            for (let i = 0; i < response.length; i++) {
                const order = this.parseOrder (response[i], market);
                result.push (order);
            }
        } else {
            throw new InvalidOrder (this.id + ' Invalid order type: ' + type);
        }
        return result;
    }

    async cancelOrder (orderHash, symbol = undefined, params = {}) {
        const nonce = await this.fetchNextNonce ();
        const args = {
            'orderHash': orderHash,
            'nonce': nonce,
            'address': this.walletAddress,
        };
        const raw = this.soliditySha3 ([
            args.orderHash,
            args.nonce,
        ]);
        const salted = this.hashMessage (raw);
        const vrs = this.signMessage (salted, this.privateKey);
        return await this.privatePostCancel (this.extend (args, vrs));
    }

    async withdraw (code, amount, address = undefined, tag = undefined, params = {}) {
        if (address !== undefined) {
            this.checkAddress (address);
        }
        const currency = this.getCurrency (code);
        let withdrawAddress = undefined;
        if (address !== undefined) {
            withdrawAddress = address;
        } else {
            withdrawAddress = this.walletAddress;
        }
        const nonce = await this.fetchNextNonce ();
        const args = {
            'address': withdrawAddress,
            'amount': this.toWei (amount),
            'token': currency['address'],
            'nonce': nonce,
        };
        const raw = this.soliditySha3 ([
            this.idexContractAddress,
            args['token'],
            args['amount'],
            args['address'],
            args['nonce'],
        ]);
        const request = this.getSignedRequestParams (args, raw);
        return await this.privatePostWithdraw (request);
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'][api];
        url += '/' + path;
        if (method === 'GET') {
            if (Object.keys (params).length)
                url += '?' + this.urlencode (params);
        } else {
            headers = { 'Content-Type': 'application/json' };
            if (api !== 'public') {
                this.checkRequiredCredentials ();
            }
            body = this.json (params);
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }

    handleErrors (code, reason, url, method, headers, body, response) {
        if (body.length > 0) {
            if (body[0] === '{') {
                const error = this.safeString (response, 'error');
                if (error) {
                    throw new ExchangeError (this.id + ' ' + error);
                }
            }
        }
    }
};
