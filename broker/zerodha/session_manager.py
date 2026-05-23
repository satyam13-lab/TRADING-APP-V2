import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


ROOT_DIR = Path(__file__).resolve().parent.parent.parent

MARKET_TIMEZONE = ZoneInfo("Asia/Kolkata")


class SessionManager:

    SESSION_FILE = (
        ROOT_DIR / "data" / "cache" / "session.json"
    )

    @classmethod
    def save_session(
        cls,
        session_data
    ):

        try:

            cls.SESSION_FILE.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            payload = {

                "access_token": session_data.get(
                    "access_token"
                ),

                "user_name": session_data.get(
                    "user_name"
                ),

                "user_id": session_data.get(
                    "user_id"
                ),

                "email": session_data.get(
                    "email"
                ),

                "login_time": datetime.now(
                    MARKET_TIMEZONE
                ).isoformat()
            }

            print(
                "\nSaving Zerodha session metadata"
            )

            with open(
                cls.SESSION_FILE,
                "w"
            ) as f:

                json.dump(
                    payload,
                    f,
                    indent=4
                )

            print(
                "\nSession saved successfully"
            )

            return True

        except Exception as e:

            print(
                "\nSESSION SAVE ERROR:"
            )

            print(str(e))

            return False

    @classmethod
    def load_session(cls):

        try:

            if not cls.SESSION_FILE.exists():

                print(
                    "\nSession file does not exist"
                )

                return None

            with open(
                cls.SESSION_FILE,
                "r"
            ) as f:

                data = json.load(f)

            if not data.get(
                "access_token"
            ):

                print(
                    "\nInvalid session file"
                )

                return None

            if cls._is_session_expired(data):

                print(
                    "\nSession expired for current trading date"
                )

                cls.clear_session()

                return None

            print(
                "\nSession loaded successfully"
            )

            return data

        except Exception as e:

            print(
                "\nSESSION LOAD ERROR:"
            )

            print(str(e))

            return None

    @classmethod
    def clear_session(cls):

        try:

            if cls.SESSION_FILE.exists():

                cls.SESSION_FILE.unlink()

                print(
                    "\nSession cleared successfully"
                )

        except Exception as e:

            print(
                "\nSESSION CLEAR ERROR:"
            )

            print(str(e))

    @classmethod
    def get_access_token(cls):

        session = cls.load_session()

        if session:

            return session.get(
                "access_token"
            )

        return None

    @classmethod
    def _is_session_expired(cls, session_data):

        login_time = session_data.get(
            "login_time"
        )

        if not login_time:

            return True

        try:

            parsed_login_time = datetime.fromisoformat(
                login_time
            )

            if parsed_login_time.tzinfo is None:

                parsed_login_time = parsed_login_time.replace(
                    tzinfo=MARKET_TIMEZONE
                )

            return (
                parsed_login_time.astimezone(
                    MARKET_TIMEZONE
                ).date()
                != datetime.now(
                    MARKET_TIMEZONE
                ).date()
            )

        except ValueError:

            return True
