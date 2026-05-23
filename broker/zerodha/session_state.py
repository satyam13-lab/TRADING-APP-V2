from dataclasses import dataclass
from enum import Enum
from typing import Optional

from broker.zerodha.session_manager import SessionManager


class BrokerSessionState(str, Enum):
    MISSING = "missing"
    SAVED = "saved"
    VERIFIED = "verified"
    EXPIRED = "expired"
    INVALID = "invalid"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class SessionStatus:
    state: BrokerSessionState
    is_usable: bool
    user_name: Optional[str] = None
    user_id: Optional[str] = None
    error: Optional[str] = None


def get_session_status(auth=None) -> SessionStatus:
    session = SessionManager.load_session()

    if not session:
        return SessionStatus(
            state=BrokerSessionState.MISSING,
            is_usable=False,
            error="No local Zerodha session"
        )

    if auth is None:
        return SessionStatus(
            state=BrokerSessionState.SAVED,
            is_usable=True,
            user_name=session.get("user_name"),
            user_id=session.get("user_id")
        )

    validation = auth.validate_session(
        session.get("access_token")
    )

    if validation.get("status"):
        return SessionStatus(
            state=BrokerSessionState.VERIFIED,
            is_usable=True,
            user_name=session.get("user_name"),
            user_id=session.get("user_id")
        )

    return SessionStatus(
        state=BrokerSessionState.UNVERIFIED,
        is_usable=False,
        user_name=session.get("user_name"),
        user_id=session.get("user_id"),
        error=validation.get("error")
    )
