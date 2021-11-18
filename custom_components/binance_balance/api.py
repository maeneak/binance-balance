"""Sample API Client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout
from binance import AsyncClient

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class BinanceBalanceApiClient:
    def __init__(self, api_key: str, api_secret: str, tld: str) -> None:
        """Sample API Client."""
        self._api_key = api_key
        self._api_secret = api_secret
        self.tld = tld
        self._session = None

    async def async_setup_client(self) -> AsyncClient:
        return await AsyncClient.create(self._api_key, self._api_secret, tld=self.tld)

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        if not self._session:
            self._session = await self.async_setup_client()
        try:
            async with async_timeout.timeout(TIMEOUT):
                return await self.api_wrapper()
        except asyncio.TimeoutError as exception:
            _LOGGER.error("Timeout error fetching information from Binance")
        except (KeyError, TypeError) as exception:
            _LOGGER.error("Timeout parsing fetching information from Binance")
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error("Timeout fetching fetching information from Binance")
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)

    async def api_wrapper(self) -> dict:
        """Get information from the API."""
        account = await self._session.get_account()
        tickers = await self._session.get_ticker()
        balances = {
            b["asset"]: float(b["free"]) + float(b["locked"])
            for b in account["balances"]
        }
        in_btc = self.getTickerMapIn("BTC", tickers)
        in_bnb = self.getTickerMapIn("BNB", tickers)
        in_usdt = self.getTickerMapIn("USDT", tickers)
        btc_usdt = 0.0
        for ticker in tickers:
            if ticker["symbol"] == "BTCUSDT":
                btc_usdt = float(ticker["lastPrice"])

        # Calculate balances in BTC, and 24-hour % changes.
        balances_in_btc = {}
        for k, v in balances.items():
            if k == "BTC":
                balances_in_btc[k] = {"$": v}
            elif k == "USDT":
                balances_in_btc[k] = {"$": v * (1 / in_usdt["BTC"]["$"])}
            elif in_btc.get(k):
                balances_in_btc[k] = {"$": v * in_btc[k]["$"]}
            elif not in_btc.get(k) and in_bnb.get(k):
                balances_in_btc[k] = {"$": v * in_bnb[k]["$"] * in_btc["BNB"]["$"]}

        relevant_balances_in_btc = {
            k: v for k, v in balances_in_btc.items() if v["$"] > 0.0001
        }
        return round(
            sum(d["$"] for d in relevant_balances_in_btc.values() if d) * btc_usdt, 2
        )

    def getTickerMapIn(self, symbol, tickers):
        return {
            t["symbol"][: -len(symbol)]: {
                "$": float(t["lastPrice"]),
                "%": float(t["priceChangePercent"]),
            }
            for t in tickers
            if t["symbol"][-len(symbol) :] == symbol
        }
