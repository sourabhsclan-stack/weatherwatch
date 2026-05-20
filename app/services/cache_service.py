import redis
import json
import os
from typing import Optional

class CacheService:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        try:
            self.client = redis.from_url(redis_url)
            self.client.ping()
            self.connected = True
            print("✅ Redis connected successfully")
        except Exception as e:
            # If Redis fails — app still works without cache
            # This is called graceful degradation
            self.connected = False
            print(f"⚠️ Redis not available: {e}")

    def get(self, key: str) -> Optional[dict]:
        if not self.connected:
            return None
        try:
            data = self.client.get(key)
            if data:
                print(f"✅ Cache HIT for key: {key}")
                return json.loads(data)
            print(f"❌ Cache MISS for key: {key}")
            return None
        except Exception as e:
            print(f"⚠️ Cache get error: {e}")
            return None

    def set(self, key: str, value: dict, ttl: int = 600):
        if not self.connected:
            return
        try:
            self.client.setex(key, ttl, json.dumps(value))
            print(f"✅ Cached key: {key} for {ttl} seconds")
        except Exception as e:
            print(f"⚠️ Cache set error: {e}")

# Single instance shared across the app
cache = CacheService()