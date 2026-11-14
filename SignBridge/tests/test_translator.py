from signbridge.translator import format_glosses

def test_empty_glosses():
    assert format_glosses([]) == ""

def test_formats_glosses():
    assert format_glosses(["HELLO", "THANK_YOU"]) == "Hello THANK_YOU."

def test_ignores_blank_values():
    assert format_glosses(["", "WATER"]) == "Water."
