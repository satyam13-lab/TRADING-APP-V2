from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    KITE_API_KEY = os.getenv("KITE_API_KEY")
    KITE_API_SECRET = os.getenv("KITE_API_SECRET")
    REDIRECT_URL = os.getenv("REDIRECT_URL")


settings = Settings()