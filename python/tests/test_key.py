import datetime as dt

import pytest

from replyonce import MISSING, canonical_json, effect_key, hash_payload, provider_idempotency_key

# Produced by the TypeScript package; Python must match byte for byte so both can share a store.
VECTORS = [
    ("reply", {"inReplyTo": "m1"}, '{"inReplyTo":"m1"}', "reply:b04f28335dc09bfd27ea14b2c7d5f4c3"),
    (
        "refund",
        {"order": "A-1001", "cents": 2500, "meta": {"b": [1, 2.5, True, None], "a": "é✓"}},
        '{"cents":2500,"meta":{"a":"é✓","b":[1,2.5,true,null]},"order":"A-1001"}',
        "refund:bffeea21f62d1cb45428c9574c926847",
    ),
    ("x", [3, "three", {"z": 1, "y": {"k": "v"}}], '[3,"three",{"y":{"k":"v"},"z":1}]', "x:02dd8cf162968cbb8ebec1c4dfad5430"),
    (
        "x",
        {"at": dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc), "n": 1.0, "big": 12345678901},
        '{"at":"2026-01-01T00:00:00.000Z","big":12345678901,"n":1}',
        "x:578a211449377e723fbdd7fbf2dbb389",
    ),
    ("x", None, "null", "x:74234e98afe7498fb5daf1f36ac2d78a"),
]


@pytest.mark.parametrize("intent,payload,canonical,key", VECTORS)
def test_matches_typescript(intent, payload, canonical, key):
    assert canonical_json(payload) == canonical
    assert effect_key(intent, payload) == key


def test_no_payload_and_provider_key_match_typescript():
    assert effect_key("reply") == "reply"
    assert effect_key("reply", MISSING) == "reply"
    assert provider_idempotency_key("conv-1", "refund:abc") == "ro_1387614e87a828dd8b7faf70276f1dce87f7ee1d"


def test_key_order_does_not_matter():
    assert hash_payload({"a": 1, "b": 2}) == hash_payload({"b": 2, "a": 1})


def test_rejects_bad_input():
    a: dict = {}
    a["self"] = a
    with pytest.raises(TypeError, match="circular"):
        hash_payload(a)
    with pytest.raises(TypeError, match="intent"):
        effect_key("has space", {})
