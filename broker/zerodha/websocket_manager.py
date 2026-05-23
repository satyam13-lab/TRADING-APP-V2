import sys
from pathlib import Path

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

        self.setup_callbacks()

    def setup_callbacks(self):

        self.kws.on_connect = self.on_connect

        self.kws.on_ticks = self.on_ticks

        self.kws.on_close = self.on_close

        self.kws.on_error = self.on_error

    def on_connect(self, ws, response):

        self.connected = True

        ws.subscribe(WATCHLIST)

        ws.set_mode(
            ws.MODE_FULL,
            WATCHLIST
        )

        print(
            "WebSocket Connected"
        )

    def on_ticks(self, ws, ticks):

        self.tick_count += len(ticks)

        for tick in ticks:

            MarketDataHandler.update_tick(
                tick
            )

    def on_close(self, ws, code, reason):

        self.connected = False

        print(
            "WebSocket Closed"
        )

    def on_error(self, ws, code, reason):

        self.connected = False

        print(
            f"WebSocket Error: {reason}"
        )

    def connect(self):

        self.kws.connect(
            threaded=True
        )

    def close(self):

        self.kws.close()