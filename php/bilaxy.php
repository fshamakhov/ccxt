<?php

namespace ccxt;

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

use Exception as Exception; // a common import

class bilaxy extends Exchange {

    public function describe () {
        return array_replace_recursive (parent::describe (), array (
            'id' => 'bilaxy',
            'name' => 'Bilaxy',
            'countries' => ['CN'], // Japan, Malta
            'rateLimit' => 500,
            'has' => array (
                'fetchDepositAddress' => true,
                'createLimitOrder' => true,
                'createMarketOrder' => false,
                'createOrder' => true,
                'fetchBalance' => true,
                'fetchBidsAsks' => true,
                'fetchClosedOrders' => true,
                'fetchOpenOrders' => true,
                'fetchOrder' => true,
                'fetchOrders' => true,
                'fetchTickers' => true,
            ),
            'urls' => array (
                'logo' => 'https://bilaxy.com/dist/images/logo.png',
                'api' => array (
                    'web' => 'https://bilaxy.com',
                    'public' => 'https://api.bilaxy.com/v1',
                    'private' => 'https://api.bilaxy.com/v1',
                    'v1' => 'https://api.bilaxy.com/v1',
                    'v2' => 'https://bilaxy.com/api/v2',
                ),
                'www' => 'https://bilaxy.com',
                'doc' => 'https://bilaxy.com/api',
            ),
            'api' => array (
                'public' => array (
                    'get' => array (
                        'depth',
                        'coins',
                        'orders',
                        'ticker',
                        'tickers',
                    ),
                ),
                'private' => array (
                    'get' => array (
                        'balances',
                        'coin_address',
                        'trade_list',
                        'trade_view',
                    ),
                    'post' => array (
                        'cancel_trade',
                        'trade',
                    ),
                ),
                'v2' => array (
                    'get' => array (
                        'market/depth',
                        'market/coins',
                        'market/orders',
                    ),
                ),
            ),
            'fees' => array (
                'trading' => array (
                    'tierBased' => false,
                    'percentage' => true,
                    'taker' => 0.0015,
                    'maker' => 0.0015,
                ),
            ),
            'bilaxySymbols' => array(),
            'commonCurrencies' => array (
                'CPT' => 'Contents Protocol',
                'CRE' => 'Carry',
                'EMB' => 'Emblem',
                'SFT' => 'SportsFix',
                'SMT' => 'Smathium',
            ),
            'exceptions' => array (
                '101' => array( 'class' => '\\ccxt\\ArgumentsRequired', 'msg' => 'The required parameters cannot be empty' ),
                '102' => array( 'class' => '\\ccxt\\AuthenticationError', 'msg' => 'API key dose not exist' ),
                '103' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'API is no longer used' ),
                '104' => array( 'class' => '\\ccxt\\PermissionDenied', 'msg' => 'Permissions closed' ),
                '105' => array( 'class' => '\\ccxt\\PermissionDenied', 'msg' => 'Insufficient authority' ),
                '106' => array( 'class' => '\\ccxt\\AuthenticationError', 'msg' => 'Signature mismatch' ),
                '201' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'The asset does not exist' ),
                '202' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'The asset cannot be deposit or withdraw' ),
                '203' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'The asset is not yet allocated to the wallet address' ),
                '204' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'Failed to cancel the order' ),
                '205' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'The transaction amount must not be less than 0.0001' ),
                '206' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'The transaction price must not be less than 0.0001' ),
                '-100' => array( 'class' => '\\ccxt\\ExchangeError', 'msg' => 'The transaction is lock' ),
                '208' => array( 'class' => '\\ccxt\\InsufficientFunds', 'msg' => 'Insufficient base currency balance' ),
                '209' => array( 'class' => '\\ccxt\\AuthenticationError', 'msg' => 'The transaction password is error' ),
                '210' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'The transaction price is not within the limit price' ),
                '-4' => array( 'class' => '\\ccxt\\InsufficientFunds', 'msg' => 'Insufficient currency balance' ),
                '212' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'The maximum amount of the transaction is limited' ),
                '213' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'The minimum total amount of the transaction is limited' ),
                '401' => array( 'class' => '\\ccxt\\BadRequest', 'msg' => 'Illegal parameter' ),
                '402' => array( 'class' => '\\ccxt\\ExchangeNotAvailable', 'msg' => 'System error' ),
            ),
        ));
    }

    public function fetch_markets ($params = array ()) {
        $response = $this->publicGetCoins ();
        $markets = $response['data'];
        $result = array();
        for ($i = 0; $i < count ($markets); $i++) {
            $market = $markets[$i];
            $id = $market['name'] . $market['group'];
            $baseId = $market['name'];
            $quoteId = $market['group'];
            $base = $this->common_currency_code($baseId);
            $quote = $this->common_currency_code($quoteId);
            $symbol = $base . '/' . $quote;
            $precision = array (
                'base' => $market['priceDecimals'],
                'quote' => $market['priceDecimals'],
                'amount' => $market['priceDecimals'],
                'price' => $market['priceDecimals'],
            );
            $active = true;
            $this->bilaxySymbols[$symbol] = $market['symbol'];
            $entry = array (
                'id' => $id,
                'symbol' => $symbol,
                'base' => $base,
                'quote' => $quote,
                'baseId' => $baseId,
                'quoteId' => $quoteId,
                'info' => $market,
                'active' => $active,
                'precision' => $precision,
                'limits' => array (
                    'amount' => array (
                        'min' => null,
                        'max' => null,
                    ),
                    'price' => array (
                        'min' => null,
                        'max' => null,
                    ),
                    'cost' => array (
                        'min' => 0.01,
                        'max' => null,
                    ),
                ),
            );
            $result[] = $entry;
        }
        return $result;
    }

    public function get_bilaxy_symbol ($symbol) {
        if ($this->bilaxySymbols === null) {
            throw new ExchangeError($this->id . ' markets not loaded');
        }
        if ((gettype ($symbol) === 'string') && (is_array($this->bilaxySymbols) && array_key_exists($symbol, $this->bilaxySymbols))) {
            return $this->bilaxySymbols[$symbol];
        }
        throw new ExchangeError($this->id . ' does not have market $symbol ' . $symbol);
    }

    public function get_symbol_from_bilaxy ($symbol) {
        if ($this->bilaxySymbols === null) {
            throw new ExchangeError($this->id . ' markets not loaded');
        }
        $keys = is_array($this->bilaxySymbols) ? array_keys($this->bilaxySymbols) : array();
        for ($i = 0; $i < count ($keys); $i++) {
            $id = $keys[$i];
            if ($this->bilaxySymbols[$id] === $symbol) {
                return $id;
            }
        }
        throw new ExchangeError($this->id . ' does not have market symbol');
    }

    public function fetch_order_book ($symbol, $limit = null, $params = array ()) {
        $bilaxy_symbol = $this->get_bilaxy_symbol ($symbol);
        $request = array (
            'symbol' => $bilaxy_symbol,
        );
        $response = $this->publicGetDepth (array_merge ($request, $params));
        return $this->parse_order_book($response['data']);
    }

    public function parse_ticker ($symbol, $ticker, $market = null) {
        $last = $this->safe_float($ticker, 'last');
        return array (
            'symbol' => $symbol,
            'timestamp' => null,
            'datetime' => null,
            'high' => $this->safe_float($ticker, 'high'),
            'low' => $this->safe_float($ticker, 'low'),
            'bid' => $this->safe_float($ticker, 'buy'),
            'bidVolume' => $this->safe_float($ticker, 'vol'),
            'ask' => $this->safe_float($ticker, 'sell'),
            'askVolume' => $this->safe_float($ticker, 'vol'),
            'vwap' => null,
            'open' => null,
            'close' => $last,
            'last' => $last,
            'previousClose' => null,
            'change' => null,
            'percentage' => null,
            'average' => null,
            'baseVolume' => null,
            'quoteVolume' => null,
            'info' => $ticker,
        );
    }

    public function fetch_ticker ($symbol, $params = array ()) {
        $bilaxy_symbol = $this->get_bilaxy_symbol ($symbol);
        $response = $this->publicGetTicker (array_merge (array (
            'symbol' => $bilaxy_symbol,
        ), $params));
        $this->load_markets();
        $market = $this->market ($symbol);
        return $this->parse_ticker($symbol, $response['data'], $market);
    }

    public function parse_tickers ($rawTickers, $symbols = null) {
        $this->load_markets();
        $tickers = array();
        for ($i = 0; $i < count ($rawTickers); $i++) {
            $symbol = $this->get_symbol_from_bilaxy ($rawTickers[$i]['symbol']);
            $market = $this->market ($symbol);
            $tickers[] = $this->parse_ticker($symbol, $rawTickers[$i], $market);
        }
        return $this->filter_by_array($tickers, 'symbol', $symbols);
    }

    public function fetch_tickers ($symbols = null, $params = array ()) {
        $this->load_markets();
        $rawTickers = $this->publicGetTickers ($params);
        return $this->parse_tickers ($rawTickers['data'], $symbols);
    }

    public function parse_trade ($trade, $market = null) {
        $timestamp = $this->safe_integer($trade, 'date');
        $price = $this->safe_float($trade, 'price');
        $amount = $this->safe_float($trade, 'count');
        $id = $this->safe_string($trade, 'id');
        $side = $this->safe_string($trade, 'type');
        $cost = $this->safe_float($trade, 'amount');
        $symbol = null;
        if ($market !== null) {
            $symbol = $market['symbol'];
        }
        return array (
            'info' => $trade,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'symbol' => $symbol,
            'id' => $id,
            'order' => null,
            'type' => null,
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
        );
    }

    public function fetch_trades ($symbol, $since = null, $limit = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'symbol' => $market['info']['symbol'],
        );
        if ($limit !== null) {
            $request['size'] = $limit; // default = 100, maximum = 000
        }
        $response = $this->publicGetOrders (array_merge ($request, $params));
        return $this->parse_trades($response['data'], $market, null, $limit);
    }

    public function fetch_balance ($params = array ()) {
        $this->load_markets();
        $response = $this->privateGetBalances ($params);
        $result = array( 'info' => $response['data'] );
        $balances = $response['data'];
        for ($i = 0; $i < count ($balances); $i++) {
            $balance = $balances[$i];
            $currency = $balance['name'];
            if (is_array($this->currencies_by_id) && array_key_exists($currency, $this->currencies_by_id)) {
                $currency = $this->currencies_by_id[$currency]['code'];
            }
            $account = array (
                'free' => floatval ($balance['balance']),
                'used' => floatval ($balance['frozen']),
                'total' => 0.0,
            );
            $account['total'] = $this->sum ($account['free'], $account['used']);
            $result[$currency] = $account;
        }
        return $this->parse_balance($result);
    }

    public function handle_errors ($code, $reason, $url, $method, $headers, $body, $response) {
        $exceptions = $this->exceptions;
        $bilaxyCode = $this->safe_string($response, 'code');
        if (is_array($exceptions) && array_key_exists($bilaxyCode, $exceptions)) {
            $ExceptionClass = $exceptions[$bilaxyCode]['class'];
            $message = $exceptions[$bilaxyCode]['msg'];
            throw new $ExceptionClass($this->id . ' ' . $message);
        }
    }

    public function fetch_order ($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' fetchOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'id' => intval ($id),
        );
        $response = $this->privateGetTradeView (array_merge ($request, $params));
        return $this->parse_order($response, $market);
    }

    public function fetch_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' fetchOrders requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'symbol' => $market['info']['symbol'],
            'type' => 0, // => All orders
        );
        if ($since !== null) {
            $request['since'] = $since;
        }
        $response = $this->privateGetTradeList (array_merge ($request, $params));
        return $this->parse_orders($response['data'], $market, $since, $limit);
    }

    public function fetch_open_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        $openParams = array( 'type' => 1 ); // 1 => Pending orders
        return $this->fetch_orders($symbol, $since, $limit, array_merge ($openParams, $params));
    }

    public function fetch_closed_orders ($symbol = null, $since = null, $limit = null, $params = array ()) {
        $orders = $this->fetch_orders($symbol, $since, $limit, $params);
        return $this->filter_by($orders, 'status', 3); // 3 => Traded completely
    }

    public function cancel_order ($id, $symbol = null, $params = array ()) {
        if ($symbol === null) {
            throw new ArgumentsRequired($this->id . ' cancelOrder requires a $symbol argument');
        }
        $this->load_markets();
        $market = $this->market ($symbol);
        $request = array (
            'id' => intval ($id),
        );
        $response = $this->privatePostCancelTrade (array_merge ($request, $params));
        $order = $this->privateGetTradeView (array( 'id' => $response['data'] ));
        return $this->parse_order($order['data'], $market);
    }

    public function parse_order_status ($status) {
        $statusString = $this->number_to_string($status);
        $statuses = array (
            '1' => 'open',
            '2' => 'open',
            '3' => 'closed',
            '4' => 'canceled',
        );
        return $this->safe_string($statuses, $statusString, $statusString);
    }

    public function parse_order ($order, $market = null) {
        $status = $this->parse_order_status($this->safe_string($order, 'status'));
        $symbol = null;
        if ($market) {
            $symbol = $market['symbol'];
        }
        $timestamp = null;
        $datetime = $this->safe_string($order, 'datetime');
        if ($datetime) {
            $timestamp = $this->parse8601 ($datetime);
        }
        $price = $this->safe_float($order, 'price');
        $amount = $this->safe_float($order, 'amount');
        $remaining = $this->safe_float($order, 'left_amount');
        $cost = null;
        $filled = null;
        if ($remaining !== null) {
            if ($amount !== null) {
                $filled = $amount - $remaining;
                if ($this->options['parseOrderToPrecision']) {
                    $filled = floatval ($this->amount_to_precision($symbol, $filled));
                }
                $filled = max ($filled, 0.0);
            }
            if (($price !== null) && ($filled !== null)) {
                $cost = $price * $filled;
            }
        }
        $id = $this->safe_string($order, 'id');
        $type = 'limit'; // Bilaxy has only limit orders
        $side = $this->safe_string($order, 'type');
        if ($side !== null) {
            $side = strtolower($side);
        }
        $fee = null;
        $trades = null;
        return array (
            'info' => $order,
            'id' => $id,
            'timestamp' => $timestamp,
            'datetime' => $this->iso8601 ($timestamp),
            'lastTradeTimestamp' => null,
            'symbol' => $symbol,
            'type' => $type,
            'side' => $side,
            'price' => $price,
            'amount' => $amount,
            'cost' => $cost,
            'filled' => $filled,
            'remaining' => $remaining,
            'status' => $status,
            'fee' => $fee,
            'trades' => $trades,
        );
    }

    public function create_order ($symbol, $type, $side, $amount, $price = null, $params = array ()) {
        $this->load_markets();
        $market = $this->market ($symbol);
        if ($price === null) {
            throw new InvalidOrder($this->id . ' createOrder method requires a $price argument');
        }
        $request = array (
            'symbol' => $market['info']['symbol'],
            'amount' => $this->amount_to_precision($symbol, $amount),
            'price' => $this->price_to_precision($symbol, $price),
            'type' => $side,
        );
        $response = $this->privatePostTrade (array_merge ($request, $params));
        $order = $this->privateGetTradeView (array( 'id' => $response['data'] ));
        return $this->parse_order($order['data'], $market);
    }

    public function fetch_deposit_address ($code, $params = array ()) {
        $balance = $this->fetch_balance ();
        $this->load_markets();
        $currency = $this->currency ($code);
        $symbol = $this->filter_by($balance['info'], 'name', $currency['id']);
        if (strlen ($symbol) !== 1) {
            throw new ExchangeError($this->id . ' could not find $currency with $code ' . $code);
        }
        $symbol = $symbol[0]['symbol'];
        $request = array (
            'symbol' => $symbol,
        );
        $response = $this->privateGetCoinAddress (array_merge ($request, $params));
        $address = $this->safe_string($response, 'data');
        $this->check_address($address);
        return array (
            'currency' => $code,
            'address' => $address,
            'tag' => null,
            'info' => $response,
        );
    }

    public function sign ($path, $api = 'public', $method = 'GET', $params = array (), $headers = null, $body = null) {
        $url = $this->urls['api'][$api];
        $url .= '/' . $path;
        if (($api === 'public') || ($api === 'v2')) {
            if ($params) {
                $url .= '?' . $this->urlencode ($params);
            }
            if ($api === 'v2') {
                $headers = array( 'accept' => 'application/json' );
            }
        } else {
            $this->check_required_credentials();
            $sorted = $this->encode ($this->urlencode ($this->keysort (array_merge (array (
                'key' => $this->apiKey,
                'secret' => $this->secret,
            ), $params))));
            $signature = $this->hash ($sorted, 'sha1');
            $query = $this->urlencode ($this->keysort (array_merge (array (
                'key' => $this->apiKey,
                'sign' => $signature,
            ), $params)));
            // var_dump ('params:', $params, 'sorted:', $sorted, 'query:', $query);
            if ($method === 'GET') {
                $url .= '?' . $query;
            } else {
                $body = $query;
                $headers = array( 'Content-Type' => 'application/x-www-form-urlencoded' );
            }
        }
        return array( 'url' => $url, 'method' => $method, 'body' => $body, 'headers' => $headers );
    }
}
