'use strict';

//  ---------------------------------------------------------------------------

const { ExchangeError } = require ('./base/errors');
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
                'fetchDepositAddress': false,
                'CORS': false,
                'fetchBidsAsks': true,
                'fetchTickers': true,
                'fetchOHLCV': false,
                'fetchMyTrades': false,
                'fetchOrder': true,
                'fetchOrders': false,
                'fetchOpenOrders': true,
                'fetchClosedOrders': true,
                'withdraw': false,
                'fetchFundingFees': false,
                'fetchDeposits': false,
                'fetchWithdrawals': false,
                'fetchTransactions': false,
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
                        'returnTradeHistory', // "market": "ETH_AURA", "address": "0x2dbdcec64db33e673140fbd0ceef610a273b84db", "start": 5000, "end": 10000, "sort": "desc", "count": 10, "cursor": "1000"
                        'returnContractAddress', // "address": "0x2a0c0dbecc7e4d658f48e01e3fa353f44050c208"
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
        });
    }

    getCurrency (currency = '') {
        if (currency in this.currencyAddresses) {
            return this.currencyAddresses[currency];
        }
        throw new ExchangeError ('Exchange ' + this.id + 'currency ' + currency + ' not found');
    }

    async fetchMarkets (params = {}) {
        this.currencyAddresses = await this.publicGetReturnCurrencies (params);
        let response = await this.publicGetReturnTicker ();
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
        let order_book = await this.publicGetReturnOrderBook (this.extend (request, params));
        return this.parseOrderBook (order_book, undefined, 'bids', 'asks', 'price', 'amount');
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

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'][api];
        url += '/' + path;
        if (method === 'GET') {
            if (Object.keys (params).length)
                url += '?' + this.urlencode (params);
        } else {
            headers['Content-Type'] = 'application/json';
            if (api !== 'public') {
                this.checkRequiredCredentials ();
            }
            body = this.json (params);
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }
};
