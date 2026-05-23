from kiteconnect import KiteConnect

from config.settings import settings
from broker.zerodha.session_manager import SessionManager


class ZerodhaAuth:

    def __init__(self):

        self.kite = KiteConnect(
            api_key=settings.KITE_API_KEY
        )

    def get_login_url(self):

        return self.kite.login_url()

    def generate_session(self, request_token):

        try:

            session_data = self.kite.generate_session(
                request_token=request_token,
                api_secret=settings.KITE_API_SECRET
            )

            access_token = session_data["access_token"]

            self.kite.set_access_token(access_token)

            SessionManager.save_session(session_data)

            return {
                "status": True,
                "data": session_data
            }

        except Exception as e:

            return {
                "status": False,
                "error": str(e)
            }