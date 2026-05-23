import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from market_data.candles import CandleBuilder
from market_data.service import MarketDataService
from market_data.storage import DuckDBMarketDataStore, ParquetCandleStore


class MarketDataEngineTests(unittest.TestCase):
    def test_candle_builder_finalizes_on_minute_rollover(self):
        builder = CandleBuilder()
        start = datetime(2026, 5, 24, 9, 15, 10)

        self.assertEqual(
            builder.ingest_tick(
                {
                    "instrument_token": 256265,
                    "last_price": 100,
                    "volume": 1000,
                    "exchange_timestamp": start
                }
            ),
            []
        )

        self.assertEqual(
            builder.ingest_tick(
                {
                    "instrument_token": 256265,
                    "last_price": 105,
                    "volume": 1020,
                    "exchange_timestamp": start + timedelta(seconds=20)
                }
            ),
            []
        )

        finalized = builder.ingest_tick(
            {
                "instrument_token": 256265,
                "last_price": 103,
                "volume": 1030,
                "exchange_timestamp": start + timedelta(minutes=1)
            }
        )

        self.assertEqual(len(finalized), 1)
        candle = finalized[0]
        self.assertEqual(candle.open, 100)
        self.assertEqual(candle.high, 105)
        self.assertEqual(candle.low, 100)
        self.assertEqual(candle.close, 105)
        self.assertEqual(candle.volume, 20)

    def test_parquet_store_round_trip(self):
        builder = CandleBuilder()
        start = datetime(2026, 5, 24, 9, 15)
        builder.ingest_tick(
            {
                "instrument_token": 260105,
                "last_price": 50000,
                "volume": 100,
                "exchange_timestamp": start
            }
        )
        candles = builder.ingest_tick(
            {
                "instrument_token": 260105,
                "last_price": 50010,
                "volume": 110,
                "exchange_timestamp": start + timedelta(minutes=1)
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            store = ParquetCandleStore(
                root=Path(temp_dir)
            )
            written = store.write_candles(candles)
            frame = store.read_candles(260105)

            self.assertEqual(written, 1)
            self.assertEqual(len(frame), 1)
            self.assertEqual(float(frame.iloc[0]["close"]), 50000.0)

    def test_market_data_service_persists_finalized_candle(self):
        start = datetime(2026, 5, 24, 9, 15)

        with tempfile.TemporaryDirectory() as temp_dir:
            parquet_root = Path(temp_dir) / "parquet"
            db_path = Path(temp_dir) / "trading.duckdb"
            service = MarketDataService(
                candle_builder=CandleBuilder(),
                candle_store=ParquetCandleStore(
                    root=parquet_root
                ),
                duckdb_store=DuckDBMarketDataStore(
                    db_path=db_path,
                    parquet_root=parquet_root
                )
            )

            service.ingest_tick(
                {
                    "instrument_token": 256265,
                    "last_price": 22000,
                    "volume": 100,
                    "timestamp": start,
                    "exchange_timestamp": start
                }
            )
            finalized = service.ingest_tick(
                {
                    "instrument_token": 256265,
                    "last_price": 22010,
                    "volume": 105,
                    "timestamp": start + timedelta(minutes=1),
                    "exchange_timestamp": start + timedelta(minutes=1)
                }
            )
            history = service.candle_history(
                256265,
                limit=10
            )

            self.assertEqual(len(finalized), 1)
            self.assertEqual(len(history), 1)


if __name__ == "__main__":
    unittest.main()
