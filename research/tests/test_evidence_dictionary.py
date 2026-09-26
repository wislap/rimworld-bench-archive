from programmatic.evidence_dictionary import encode, decode


def test_lossless_subjects_scope_nulls_and_reserved_keys():
    common = {"scope": {"actor": "pawn-1", "user": "pawn-2"}, "unknown": None, "limitations": ["unknown"] * 60}
    value = [{"id": "pawn-1", "value": common}, {"id": "pawn-2", "value": common},
             {"$ref": "literal", "$object": {"$ref": "also literal"}}, [False, 0, "", [], {}]]
    packed = encode(value)
    assert packed["shared_values"]
    assert decode(packed) == value


def test_nested_shared_values_remain_lossless():
    child = {"x": "long definition " * 100}
    parent = {"one": child, "two": child}
    value = [parent, parent, child]
    packed = encode(value)
    assert decode(packed) == value
