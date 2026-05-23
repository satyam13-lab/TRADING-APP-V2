import tempfile
import unittest
from pathlib import Path

from broker.zerodha.instruments import (
    ZerodhaInstrumentRegistry,
    load_watchlist_tokens
)
from broker.zerodha.market_data_handler import MarketDataHandler
from broker.zerodha.orders import (
    OrderRequest,
    OrderSide,
    OrderType,
    ZerodhaOrderManager
)


class ZerodhaPhase2Tests(unittest.TestCase):
    def test_default_watchlist_contains_core_indices(self):
        tokens = load_watchlist_tokens()

        self.assertIn(256265, tokens)
        self.assertIn(260105, tokens)

    def test_instrument_registry_loads_cached_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = Path(temp_dir) / "instruments.csv"
            cache_file.write_text(
                (
                    "instrument_token,tradingsymbol,exchange,name,segment,"
                    "instrument_type,lot_size,tick_size\n"
                    "12345,RELIANCE,NSE,RELIANCE,NSE,EQ,1,0.05\n"
                ),
                encoding="utf-8"
            )

            registry = ZerodhaInstrumentRegistry(
                cache_file=cache_file
            )

            self.assertEqual(
                registry.token_for("RELIANCE", "NSE"),
                12345
            )

    def test_market_data_normalizes_tick(self):
        normalized = MarketDataHandler.normalize_tick(
            {
                "instrument_token": 256265,
                "last_price": 22500.5,
                "volume": 1000,
                "oi": 10
            }
        )

        self.assertEqual(
            normalized["instrument_token"],
            256265
        )
        self.assertEqual(
            normalized["last_price"],
            22500.5
        )

    def test_paper_order_manager_blocks_invalid_quantity(self):
        manager = ZerodhaOrderManager()

        with self.assertRaises(ValueError):
            manager.place_order(
                OrderRequest(
                    exchange="NSE",
                    tradingsymbol="RELIANCE",
                    side=OrderSide.BUY,
                    quantity=0
                )
            )

    def test_paper_order_manager_places_order(self):
        manager = ZerodhaOrderManager()
        order_id = manager.place_order(
            OrderRequest(
                exchange="NSE",
                tradingsymbol="RELIANCE",
                side=OrderSide.BUY,
                quantity=1,
                order_type=OrderType.MARKET
            )
        )

        order = manager.get_order(order_id)

        self.assertEqual(
            order["status"],
            "COMPLETE"
        )
        self.assertEqual(
            order["mode"],
            "paper"
        )


if __name__ == "__main__":
    unittest.main()
