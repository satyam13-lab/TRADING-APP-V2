from dataclasses import asdict, dataclass
from datetime import datetime
from threading import Lock
from typing import Optional


@dataclass
class Candle:
    instrument_token: int
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int = 0
    oi: Optional[int] = None

    def to_dict(self):
        return asdict(self)


class CandleBuilder:
    def __init__(self):
        self._current = {}
        self._last_cumulative_volume = {}
        self._lock = Lock()

    def ingest_tick(self, tick: dict) -> list[Candle]:
        instrument_token = tick.get("instrument_token")
        last_price = tick.get("last_price")

        if instrument_token is None or last_price is None:
            return []

        instrument_token = int(instrument_token)
        price = float(last_price)
        tick_time = self._tick_time(tick)
        bucket = tick_time.replace(
            second=0,
            microsecond=0
        )
        volume_delta = self._volume_delta(
            instrument_token,
            tick.get("volume")
        )

        with self._lock:
            current = self._current.get(instrument_token)

            if current is None:
                self._current[instrument_token] = self._new_candle(
                    instrument_token,
                    bucket,
                    price,
                    volume_delta,
                    tick.get("oi")
                )
                return []

            if bucket > current.timestamp:
                finalized = current
                self._current[instrument_token] = self._new_candle(
                    instrument_token,
                    bucket,
                    price,
                    volume_delta,
                    tick.get("oi")
                )
                return [finalized]

            if bucket < current.timestamp:
                return []

            current.high = max(
                current.high,
                price
            )
            current.low = min(
                current.low,
                price
            )
            current.close = price
            current.volume += volume_delta
            current.oi = tick.get(
                "oi",
                current.oi
            )

            return []

    def get_open_candles(self) -> list[Candle]:
        with self._lock:
            return list(
                self._current.values()
            )

    @staticmethod
    def _new_candle(
        instrument_token: int,
        timestamp: datetime,
        price: float,
        volume: int,
        oi: Optional[int]
    ) -> Candle:
        return Candle(
            instrument_token=instrument_token,
            timestamp=timestamp,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=volume,
            oi=oi
        )

    @staticmethod
    def _tick_time(tick: dict) -> datetime:
        timestamp = (
            tick.get("exchange_timestamp")
            or tick.get("timestamp")
            or datetime.now()
        )

        if isinstance(timestamp, datetime):
            return timestamp

        return datetime.fromisoformat(
            str(timestamp)
        )

    def _volume_delta(
        self,
        instrument_token: int,
        cumulative_volume
    ) -> int:
        if cumulative_volume is None:
            return 0

        cumulative_volume = int(cumulative_volume)
        previous_volume = self._last_cumulative_volume.get(
            instrument_token
        )
        self._last_cumulative_volume[instrument_token] = cumulative_volume

        if previous_volume is None:
            return 0

        return max(
            0,
            cumulative_volume - previous_volume
        )

