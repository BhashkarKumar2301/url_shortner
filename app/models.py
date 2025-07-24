# models.py
import threading
from datetime import datetime

class URLStore:
    def __init__(self):
        self.store = {}  # short_code -> { url, created_at, clicks }
        self.lock = threading.Lock()

    def save_url(self, short_code, long_url):
        with self.lock:
            self.store[short_code] = {
                "url": long_url,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "clicks": 0
            }

    def get_url_data(self, short_code):
        with self.lock:
            return self.store.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.store:
                self.store[short_code]["clicks"] += 1

    def exists(self, short_code):
        with self.lock:
            return short_code in self.store
