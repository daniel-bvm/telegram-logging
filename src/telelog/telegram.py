import httpx
from typing import Callable
import os
from io import StringIO
import sys
import asyncio

TELEGRAM_ROOM = os.getenv("TELEGRAM_ROOM")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_POST_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_ROOM}"
MESSAGE_LENGTH_LIMIT = 4096

class _stream_capture(object):
    async def __aenter__(self):
        return self.__enter__()
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        return self.__exit__(exc_type, exc_value, traceback)

class _stdout_capture(_stream_capture):
    def __init__(self) -> None:
        self.io = StringIO()

    def __enter__(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.io
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.old_stdout
        return self.io.getvalue()

class _stderr_capture(_stream_capture):
    def __init__(self) -> None:
        self.io = StringIO()

    def __enter__(self):
        self.old_stderr = sys.stderr
        sys.stderr = self.io
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stderr = self.old_stderr
        return self.io.getvalue()

def _silent_logging_decorator(func: Callable):
    def wrapper(*args, **kwargs):
        with _stdout_capture(), _stderr_capture():
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return False
        
    async def awrapper(*args, **kwargs):
        async with _stdout_capture(), _stderr_capture():
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                return False

    return wrapper if not asyncio.iscoroutinefunction(func) else awrapper

@_silent_logging_decorator
def log(message: str, fmt: str = "HTML"):

    resp = httpx.post(
        TELEGRAM_POST_URL,
        json={
            "text": message,
            "parse_mode": fmt,
            "disable_notification": True,
        }
    )

    return resp.status_code == 200

@_silent_logging_decorator
async def alog(message: str, fmt: str = "HTML"):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            TELEGRAM_POST_URL,
            json={
                "text": message,
                "parse_mode": fmt,
                "disable_notification": True,
            }
        )
        
    return resp.status_code == 200
