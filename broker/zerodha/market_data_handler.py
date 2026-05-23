from collections import defaultdict
from datetime import datetime


class MarketDataHandler:

    live_data = defaultdict(dict)

    @classmethod
    def update_tick(cls, tick):

        instrument_token = tick.get(
            "instrument_token"
        )

        cls.live_data[instrument_token] = {

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

    @classmethod
    def get_data(cls):

        return dict(cls.live_data)