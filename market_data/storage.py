from pathlib import Path

import duckdb
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parent.parent
PARQUET_ROOT = ROOT_DIR / "data" / "parquet" / "candles"
DUCKDB_PATH = ROOT_DIR / "database" / "duckdb" / "trading.duckdb"


class ParquetCandleStore:
    def __init__(
        self,
        root: Path = PARQUET_ROOT
    ):
        self.root = root

    def write_candles(self, candles):
        rows = [
            candle.to_dict()
            for candle in candles
        ]

        if not rows:
            return 0

        frame = pd.DataFrame(rows)
        frame["date"] = pd.to_datetime(
            frame["timestamp"]
        ).dt.date.astype(str)

        written = 0

        for (instrument_token, date), group in frame.groupby(
            [
                "instrument_token",
                "date"
            ]
        ):
            path = self._path_for(
                int(instrument_token),
                str(date)
            )
            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            output = group.drop(
                columns=["date"]
            )

            if path.exists():
                existing = pd.read_parquet(path)
                output = pd.concat(
                    [
                        existing,
                        output
                    ],
                    ignore_index=True
                )
                output = output.drop_duplicates(
                    subset=[
                        "instrument_token",
                        "timestamp"
                    ],
                    keep="last"
                )
                output = output.sort_values(
                    "timestamp"
                )

            output.to_parquet(
                path,
                index=False
            )
            written += len(group)

        return written

    def read_candles(
        self,
        instrument_token: int,
        start=None,
        end=None
    ) -> pd.DataFrame:
        paths = list(
            (self.root / f"instrument_token={int(instrument_token)}")
            .glob("date=*/candles.parquet")
        )

        if not paths:
            return pd.DataFrame()

        frame = pd.concat(
            [
                pd.read_parquet(path)
                for path in paths
            ],
            ignore_index=True
        )
        frame["timestamp"] = pd.to_datetime(
            frame["timestamp"]
        )

        if start is not None:
            frame = frame[
                frame["timestamp"] >= pd.Timestamp(start)
            ]

        if end is not None:
            frame = frame[
                frame["timestamp"] <= pd.Timestamp(end)
            ]

        return frame.sort_values(
            "timestamp"
        ).reset_index(
            drop=True
        )

    def _path_for(
        self,
        instrument_token: int,
        date: str
    ) -> Path:
        return (
            self.root
            / f"instrument_token={instrument_token}"
            / f"date={date}"
            / "candles.parquet"
        )


class DuckDBMarketDataStore:
    def __init__(
        self,
        db_path: Path = DUCKDB_PATH,
        parquet_root: Path = PARQUET_ROOT
    ):
        self.db_path = db_path
        self.parquet_root = parquet_root

    def query_candles(
        self,
        instrument_token: int,
        limit: int = 500
    ) -> pd.DataFrame:
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        pattern = (
            self.parquet_root
            / f"instrument_token={int(instrument_token)}"
            / "date=*"
            / "candles.parquet"
        )

        with duckdb.connect(str(self.db_path)) as connection:
            return connection.execute(
                """
                SELECT *
                FROM read_parquet(?)
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                [
                    str(pattern),
                    int(limit)
                ]
            ).fetchdf()

