"""Lossless repeated-value dictionary for a presentation experiment.

No game fields are selected, interpreted, ranked or discarded. Decode must
recover the exact input JSON, including nulls, limits and binding metadata.
"""
from collections import Counter
import json


def _key(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def encode(value, minimum_chars=200):
    counts = Counter()

    def count(node):
        if isinstance(node, (dict, list, str)):
            key = _key(node)
            if len(key) >= minimum_chars:
                counts[key] += 1
        if isinstance(node, dict):
            for child in node.values():
                count(child)
        elif isinstance(node, list):
            for child in node:
                count(child)

    count(value)
    shared, names = {}, {}

    def children(node):
        if isinstance(node, dict):
            result = {k: walk(v) for k, v in node.items()}
            # Unambiguous escaping of native data with reserved keys.
            return {"$object": result} if "$ref" in result or "$object" in result else result
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    def walk(node):
        key = _key(node)
        if counts[key] > 1:
            if key not in names:
                name = f"value_{len(names) + 1}"
                names[key] = name
                shared[name] = children(node)
            return {"$ref": names[key]}
        return children(node)

    records = walk(value)
    return {"encoding": "shared_json_values_v1", "shared_values": shared, "records": records}


def decode(encoded):
    if encoded.get("encoding") != "shared_json_values_v1":
        raise ValueError("Unknown evidence encoding")
    active = set()

    def walk(node):
        if isinstance(node, dict):
            if set(node) == {"$ref"}:
                name = node["$ref"]
                if name in active:
                    raise ValueError("Cyclic evidence reference")
                active.add(name)
                result = walk(encoded["shared_values"][name])
                active.remove(name)
                return result
            if set(node) == {"$object"}:
                return {k: walk(v) for k, v in node["$object"].items()}
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    return walk(encoded["records"])


GUIDANCE = """The evidence uses a lossless shared-value dictionary to avoid repetition.
Read records as the original observations. Anywhere {\"$ref\":\"value_N\"} occurs,
substitute shared_values.value_N at that exact position; nested references work
the same way. {\"$object\":{...}} escapes a native object with reserved keys.
No fact was removed: identities, actor/recipient context, units, coverage and
unknowns are preserved. Shared definitions do not change a record's subject.
"""
