import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

try:
    import yaml
except ImportError:
    yaml = None


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "instruments.yaml"
INSTRUMENT_CACHE_FILE = ROOT_DIR / "data" / "cache" / "zerodha_instruments.csv"

DEFAULT_INDEX_INSTRUMENTS = {
    "NIFTY": {
        "tradingsymbol": "NIFTY 50",
        "exchange": "NSE",
        "instrument_token": 256265
    },
    "BANKNIFTY": {
        "tradingsymbol": "NIFTY BANK",
        "exchange": "NSE",
        "instrument_token": 260105
    }
}


def _load_instrument_config():
    if yaml is None or not CONFIG_FILE.exists():
        return {}

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        return yaml.safe_load(file) or {}


@dataclass(frozen=True)
class ZerodhaInstrument:
    instrument_token: int
    tradingsymbol: str
    exchange: str
    name: str = ""
    segment: str = ""
    instrument_type: str = ""
    lot_size: int = 1
    tick_size: float = 0.05

    @classmethod
    def from_dict(cls, row):
        return cls(
            instrument_token=int(row["instrument_token"]),
            tradingsymbol=str(row.get("tradingsymbol") or row.get("symbol")),
            exchange=str(row.get("exchange") or ""),
            name=str(row.get("name") or ""),
            segment=str(row.get("segment") or ""),
            instrument_type=str(row.get("instrument_type") or ""),
            lot_size=int(float(row.get("lot_size") or 1)),
            tick_size=float(row.get("tick_size") or 0.05)
        )


class ZerodhaInstrumentRegistry:
    def __init__(
        self,
        cache_file: Path = INSTRUMENT_CACHE_FILE
    ):
        self.cache_file = cache_file
        self._instruments_by_token = {}
        self._instruments_by_key = {}
        self._load_defaults()
        self.load_cached()

    def _load_defaults(self):
        for item in DEFAULT_INDEX_INSTRUMENTS.values():
            self._add(
                ZerodhaInstrument(
                    instrument_token=item["instrument_token"],
                    tradingsymbol=item["tradingsymbol"],
                    exchange=item["exchange"],
                    segment=item["exchange"],
                    instrument_type="INDEX"
                )
            )

    def _add(self, instrument: ZerodhaInstrument):
        key = self._key(
            instrument.exchange,
            instrument.tradingsymbol
        )
        self._instruments_by_token[instrument.instrument_token] = instrument
        self._instruments_by_key[key] = instrument

    @staticmethod
    def _key(exchange: str, tradingsymbol: str) -> str:
        return f"{exchange}:{tradingsymbol}".upper()

    def refresh_from_kite(self, kite, exchanges: Optional[Iterable[str]] = None):
        rows = []
        target_exchanges = list(exchanges or ["NSE", "NFO", "MCX"])

        for exchange in target_exchanges:
            rows.extend(
                kite.instruments(exchange)
            )

        self.cache_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not rows:
            return 0

        fieldnames = sorted(
            {
                key
                for row in rows
                for key in row.keys()
            }
        )

        with open(
            self.cache_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )
            writer.writeheader()
            writer.writerows(rows)

        self.load_cached()
        return len(rows)

    def load_cached(self):
        if not self.cache_file.exists():
            return 0

        count = 0

        with open(
            self.cache_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    self._add(
                        ZerodhaInstrument.from_dict(row)
                    )
                    count += 1
                except (KeyError, TypeError, ValueError):
                    continue

        return count

    def get_by_token(self, instrument_token: int) -> Optional[ZerodhaInstrument]:
        return self._instruments_by_token.get(
            int(instrument_token)
        )

    def find(
        self,
        tradingsymbol: str,
        exchange: str = "NSE"
    ) -> Optional[ZerodhaInstrument]:
        return self._instruments_by_key.get(
            self._key(
                exchange,
                tradingsymbol
            )
        )

    def token_for(
        self,
        tradingsymbol: str,
        exchange: str = "NSE"
    ) -> Optional[int]:
        instrument = self.find(
            tradingsymbol,
            exchange
        )

        if not instrument:
            return None

        return instrument.instrument_token


def load_watchlist_tokens() -> list[int]:
    registry = ZerodhaInstrumentRegistry()

    watchlist = []

    config = _load_instrument_config()

    index_items = {
        item.get("alias"): {
            "tradingsymbol": item.get("symbol"),
            "exchange": item.get("exchange", "NSE"),
            "instrument_token": item.get("instrument_token")
        }
        for item in config.get("indices", [])
        if item.get("alias")
    }

    configured_aliases = (
        config.get("watchlist", {})
        .get("indices", [])
    )

    if configured_aliases:
        source_items = [
            index_items.get(alias)
            or DEFAULT_INDEX_INSTRUMENTS.get(alias)
            for alias in configured_aliases
        ]
    else:
        source_items = DEFAULT_INDEX_INSTRUMENTS.values()

    for item in source_items:
        if not item:
            continue

        instrument = registry.find(
            item["tradingsymbol"],
            item["exchange"]
        )

        if instrument:
            watchlist.append(
                instrument.instrument_token
            )

        elif item.get("instrument_token"):
            watchlist.append(
                int(
                    item["instrument_token"]
                )
            )

    return watchlist
