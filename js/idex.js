'use strict';

//  ---------------------------------------------------------------------------

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
        });
    }

    sign (path, api = 'public', method = 'GET', params = {}, headers = undefined, body = undefined) {
        let url = this.urls['api'][api];
        url += '/' + path;
        if (method === 'GET') {
            if (Object.keys (params).length)
                url += '?' + this.urlencode (params);
        } else {
            headers['Content-Type'] = 'application/json';
            if (api === 'public') {
                body = this.json (params);
            } else {
                this.checkRequiredCredentials ();
                // TODO: sign private request
            }
        }
        return { 'url': url, 'method': method, 'body': body, 'headers': headers };
    }
};
