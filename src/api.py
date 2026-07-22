"""Thin wrapper around urllib with sane timeouts and JSON handling."""

import json
import urllib.error
import urllib.request

DEFAULT_TIMEOUT = 10  # seconds, got bitten by hanging requests before


class ApiError(Exception):
    def __init__(self, status, body):
        super().__init__(f"HTTP {status}: {body[:200]}")
        self.status = status
        self.body = body


def get(url, params=None, headers=None):
    if params:
        url = url + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(url, headers=headers or {})
    return _do(req)


def post(url, data, headers=None):
    payload = json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=payload, method="POST",
        headers={"Content-Type": "application/json", **(headers or {})},
    )
    return _do(req)


def _do(req):
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            body = resp.read().decode()
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, body
    except urllib.error.HTTPError as err:
        raise ApiError(err.code, err.read().decode()) from err
