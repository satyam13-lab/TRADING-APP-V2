from datetime import datetime
from threading import Lock

from market_data.candles import CandleBuilder
from market_data.storage import DuckDBMarketDataStore, ParquetCandleStore


class MarketDataService:
    def __init__(
        self,
        candle_builder=None,
        candle_store=None,
        duckdb_store=None
    ):
        self.candle_builder = candle_builder or CandleBuilder()
        self.candle_store = candle_store or ParquetCandleStore()
        self.duckdb_store = duckdb_store or DuckDBMarketDataStore()
        self._latest_ticks = {}
        self._latest_final_candles = {}
        self._lock = Lock()

    def ingest_tick(self, tick: dict):
        instrument_token = tick.get("instrument_token")

        if instrument_token is not None:
            with self._lock:
                self._latest_ticks[int(instrument_token)] = tick.copy()

        finalized = self.candle_builder.ingest_tick(tick)

        if finalized:
            self.candle_store.write_candles(
                finalized
            )

            with self._lock:
                for candle in finalized:
                    self._latest_final_candles[
                        candle.instrument_token
                    ] = candle

        return finalized

    def latest_tick(self, instrument_token: int):
        with self._lock:
            tick = self._latest_ticks.get(
                int(instrument_token)
            )

            if tick is None:
                return None

            return tick.copy()

    def latest_candle(self, instrument_token: int):
        open_candles = {
            candle.instrument_token: candle
            for candle in self.candle_builder.get_open_candles()
        }

        candle = open_candles.get(
            int(instrument_token)
        )

        if candle:
            return candle

        with self._lock:
            return self._latest_final_candles.get(
                int(instrument_token)
            )

    def candle_history(
        self,
        instrument_token: int,
        limit: int = 500
    ):
        try:
            return self.duckdb_store.query_candles(
                instrument_token,
                limit=limit
            )
        except Exception:
            return self.candle_store.read_candles(
                instrument_token
            ).tail(limit)

    def is_stale(
        self,
        instrument_token: int,
        max_age_seconds: int = 10
    ) -> bool:
        tick = self.latest_tick(
            instrument_token
        )

        if not tick:
            return True

        timestamp = tick.get(
            "timestamp"
        )

        if not isinstance(timestamp, datetime):
            return True

        age = (
            datetime.now() - timestamp
        ).total_seconds()

        return age > max_age_seconds


market_data_service = MarketDataService()
