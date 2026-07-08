"""Small helpers I keep re-writing in every project, so now they live here."""

import time
from datetime import datetime, timezone


def slugify(text: str) -> str:
    out = []
    for ch in text.strip().lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def retry(fn, attempts=3, delay=0.5, exceptions=(Exception,)):
    last_err = None
    for _ in range(attempts):
        try:
            return fn()
        except exceptions as err:
            last_err = err
            time.sleep(delay)
    raise last_err


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"
