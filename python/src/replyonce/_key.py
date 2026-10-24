"""Keys and canonical hashing, byte-compatible with the TypeScript package."""

from __future__ import annotations

import dataclasses
import datetime as _dt
import hashlib
import json
import math
import re
from typing import Any

MISSING: Any = object()
"""Sentinel for "no payload" (distinct from a ``None`` payload, which hashes as JSON null)."""


def _sort_key(k: str) -> bytes:
    # JavaScript sorts object keys by UTF-16 code units.
    return k.encode("utf-16-be")


def _iso(value: _dt.datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=_dt.timezone.utc)
    value = value.astimezone(_dt.timezone.utc)
    return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"


def _normalize(value: Any, seen: set[int]) -> Any:
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0 else "-Infinity"
        return int(value) if value.is_integer() else value
    if isinstance(value, _dt.datetime):
        return _iso(value)
    if isinstance(value, _dt.date):
        return _iso(_dt.datetime(value.year, value.month, value.day, tzinfo=_dt.timezone.utc))
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        value = dataclasses.asdict(value)
    elif hasattr(value, "model_dump") and callable(value.model_dump):
        value = value.model_dump()
    if id(value) in seen:
        raise TypeError("replyonce: cannot hash a circular payload")
    if isinstance(value, (list, tuple)):
        seen.add(id(value))
        out = [_normalize(v, seen) for v in value]
        seen.discard(id(value))
        return out
    if isinstance(value, dict):
        seen.add(id(value))
        items = sorted(((str(k), v) for k, v in value.items()), key=lambda kv: _sort_key(kv[0]))
        obj = {k: _normalize(v, seen) for k, v in items}
        seen.discard(id(value))
        return obj
    raise TypeError(f"replyonce: cannot hash a payload of type {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Deterministic JSON: keys sorted, no whitespace. Matches the TypeScript ``canonicalJson``."""
    return json.dumps(_normalize(value, set()), separators=(",", ":"), ensure_ascii=False, sort_keys=False)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_payload(payload: Any) -> str:
    return sha256_hex(canonical_json(payload))[:32]


_SAFE_INTENT = re.compile(r"^[A-Za-z0-9_.:-]{1,100}$")


def effect_key(intent: str, payload: Any = MISSING) -> str:
    """Ledger key for an intent plus the business identity of the payload."""
    if not isinstance(intent, str) or not _SAFE_INTENT.match(intent):
        raise TypeError(f"replyonce: intent must match {_SAFE_INTENT.pattern} (got {intent!r})")
    return intent if payload is MISSING else f"{intent}:{hash_payload(payload)}"


def provider_idempotency_key(scope: str, key: str) -> str:
    """Stable idempotency key to hand to a provider (Stripe-style ``Idempotency-Key``)."""
    return "ro_" + sha256_hex(f"{scope}\u0000{key}")[:40]
