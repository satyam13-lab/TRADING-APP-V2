from datetime import datetime
from threading import Lock


class MarketDataHandler:

    live_data = {}

    _lock = Lock()

    @classmethod
    def update_tick(cls, tick):

        instrument_token = tick.get(
            "instrument_token"
        )

        if instrument_token is None:

            return

        snapshot = {

            "last_price": tick.get(
                "last_price"
            ),

            "volume": tick.get(
                "volume"
            ),

            "oi": tick.get(
                "oi"
            ),

            "timestamp": datetime.now()
        }

        with cls._lock:

            cls.live_data[instrument_token] = snapshot

    @classmethod
    def get_data(cls):

        with cls._lock:

            return {
                token: values.copy()
                for token, values in cls.live_data.items()
            }
