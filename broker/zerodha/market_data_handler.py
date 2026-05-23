from datetime import datetime
from threading import Lock


class MarketDataHandler:

    live_data = {}

    _lock = Lock()

    @classmethod
    def update_tick(cls, tick):

        snapshot = cls.normalize_tick(
            tick
        )

        if snapshot is None:

            return

        instrument_token = snapshot[
            "instrument_token"
        ]

        with cls._lock:

            cls.live_data[instrument_token] = snapshot

    @classmethod
    def normalize_tick(cls, tick):

        instrument_token = tick.get(
            "instrument_token"
        )

        if instrument_token is None:

            return None

        return {

            "instrument_token": instrument_token,

            "last_price": tick.get(
                "last_price"
            ),

            "volume": tick.get(
                "volume"
            ),

            "oi": tick.get(
                "oi"
            ),

            "depth": tick.get(
                "depth"
            ),

            "exchange_timestamp": tick.get(
                "exchange_timestamp"
            ),

            "timestamp": datetime.now()
        }

    @classmethod
    def get_data(cls):

        with cls._lock:

            return {
                token: values.copy()
                for token, values in cls.live_data.items()
            }
