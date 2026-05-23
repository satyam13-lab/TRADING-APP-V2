from broker.zerodha.instruments import (
    DEFAULT_INDEX_INSTRUMENTS,
    ZerodhaInstrumentRegistry,
    load_watchlist_tokens
)


NIFTY_50_TOKEN = DEFAULT_INDEX_INSTRUMENTS["NIFTY"]["instrument_token"]

BANKNIFTY_TOKEN = DEFAULT_INDEX_INSTRUMENTS["BANKNIFTY"]["instrument_token"]

WATCHLIST = load_watchlist_tokens()


__all__ = [
    "BANKNIFTY_TOKEN",
    "NIFTY_50_TOKEN",
    "WATCHLIST",
    "ZerodhaInstrumentRegistry"
]
