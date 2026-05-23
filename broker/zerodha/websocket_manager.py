import sys
from pathlib import Path
from datetime import datetime
from threading import Lock

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from kiteconnect import KiteTicker

from config.settings import settings

from broker.zerodha.market_data_handler import (
    MarketDataHandler
)

from broker.zerodha.instrument_manager import (
    WATCHLIST
)


class ZerodhaWebSocket:

    def __init__(self, access_token):

        self.kws = KiteTicker(
            settings.KITE_API_KEY,
            access_token
        )

        self.connected = False

        self.tick_count = 0

        self.last_tick_at = None

        self.last_error = None

        self.watchlist = list(WATCHLIST)

        self._state_lock = Lock()

        self.setup_callbacks()

    def setup_callbacks(self):

        self.kws.on_connect = self.on_connect

        self.kws.on_ticks = self.on_ticks

        self.kws.on_close = self.on_close

        self.kws.on_error = self.on_error

    def on_connect(self, ws, response):

        with self._state_lock:

            self.connected = True

        ws.subscribe(
            self.watchlist
        )

        ws.set_mode(
            ws.MODE_FULL,
            self.watchlist
        )

        print(
            "WebSocket Connected"
        )

    def on_ticks(self, ws, ticks):

        with self._state_lock:

            self.tick_count += len(ticks)

            self.last_tick_at = datetime.now()

        for tick in ticks:

            MarketDataHandler.update_tick(
                tick
            )

    def on_close(self, ws, code, reason):

        with self._state_lock:

            self.connected = False

            self.last_error = str(reason)

        print(
            "WebSocket Closed"
        )

    def on_error(self, ws, code, reason):

        with self._state_lock:

            self.connected = False

            self.last_error = str(reason)

        print(
            f"WebSocket Error: {reason}"
        )

    def connect(self):

        self.kws.connect(
            threaded=True
        )

    def subscribe(self, tokens):

        clean_tokens = [
            int(token)
            for token in tokens
        ]

        with self._state_lock:

            self.watchlist = sorted(
                set(
                    self.watchlist + clean_tokens
                )
            )

        if self.connected:

            self.kws.subscribe(
                clean_tokens
            )

            self.kws.set_mode(
                self.kws.MODE_FULL,
                clean_tokens
            )

    def unsubscribe(self, tokens):

        clean_tokens = [
            int(token)
            for token in tokens
        ]

        with self._state_lock:

            self.watchlist = [
                token
                for token in self.watchlist
                if token not in clean_tokens
            ]

        if self.connected:

            self.kws.unsubscribe(
                clean_tokens
            )

    def close(self):

        with self._state_lock:

            self.connected = False

        self.kws.close()

    def health(self):

        with self._state_lock:

            return {
                "connected": self.connected,
                "tick_count": self.tick_count,
                "last_tick_at": self.last_tick_at,
                "last_error": self.last_error,
                "subscriptions": list(self.watchlist)
            }
