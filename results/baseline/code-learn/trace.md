### Human
The test suite of the `inventory` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
[{'arguments': '{"path":"workspace"}', 'call_id': 'call_aPgYQP8HokOBRXqzAR3KW2IT', 'name': 'ls', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811034b087d086d0bce231361b4e', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/inventory/', '/workspace/tests/']

### Assistant
[{'arguments': '{"path":"workspace/inventory"}', 'call_id': 'call_yC4qugsDWHXudhSnwlbAO0ZD', 'name': 'ls', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac481132f6087d0a3374fb6d44cdcce', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace/inventory"}

### Tool result
['/workspace/inventory/__init__.py', '/workspace/inventory/export.py', '/workspace/inventory/pricing.py', '/workspace/inventory/report.py']

### Assistant
[{'arguments': '{"file_path":"workspace/inventory/export.py","offset":0,"limit":300}', 'call_id': 'call_nehDdY75x5pyu4dndcwhcGn6', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811857d087d0abd81fe4f2a0bff2', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/inventory/pricing.py","offset":0,"limit":300}', 'call_id': 'call_hKveldlal7RiXIWZeW4QZ7Iy', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811857e487d0bb544637cc7a417b', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/inventory/report.py","offset":0,"limit":300}', 'call_id': 'call_3xYrIeW8XfQFDeGXkJKu84h3', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811857ec87d0bf4510598bc1f5d5', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/inventory/__init__.py","offset":0,"limit":200}', 'call_id': 'call_D1WIS4oItSeVRofmRnLW1xlO', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811857f487d0a8bfd47c3c7651f6', 'status': 'completed'}, {'arguments': '{"path":"workspace/tests"}', 'call_id': 'call_zWFE2jvur6NxvdNq8443s9Pq', 'name': 'ls', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811857fc87d0aa783475ec846e46', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/inventory/export.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/inventory/pricing.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/inventory/report.py", "offset": 0, "limit": 300}

### Tool call: read_file
{"file_path": "workspace/inventory/__init__.py", "offset": 0, "limit": 200}

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
@@ lines 1-12 of 12 @@
"""Export helpers."""
from .pricing import parse_price


def to_csv_row(item):
    """Format one item as a CSV row: name,price,qty (price with 2 decimals).

    A name that contains a comma or a double quote is wrapped in double quotes,
    and every double quote inside it is doubled (RFC 4180).
    """
    price = parse_price(item["price"])
    return f'{item["name"]},{price:.2f},{item["qty"]}'

### Tool result
@@ lines 1-25 of 25 @@
"""Price utilities for the inventory package."""
from decimal import Decimal


def parse_price(text):
    """Convert a price string to a Decimal.

    Supported formats:
      "$1,299.50" -> Decimal("1299.50")
      "  12 "     -> Decimal("12")
      "1299.5"    -> Decimal("1299.5")
      "(12.00)"   -> Decimal("-12.00")   # accounting style: parentheses mean negative
    """
    cleaned = text.strip().replace("$", "")
    return Decimal(cleaned)


def apply_discount(price, percent):
    """Return `price` after a percentage discount.

    The result is a Decimal rounded to 2 decimal places using the
    commercial rule "round half up" (0.005 -> 0.01).
    """
    discounted = price * (100 - percent) / 100
    return discounted.quantize(Decimal("0.01"))

### Tool result
@@ lines 1-25 of 25 @@
"""Inventory reports."""
from decimal import Decimal

from .pricing import apply_discount, parse_price


def total_value(items):
    """Total value of `items` after per-item discounts.

    Each item is a dict: {"name": str, "price": str, "qty": int, "discount": percent (optional)}.
    """
    total = Decimal("0")
    for item in items:
        price = parse_price(item["price"])
        price = apply_discount(price, item.get("discount", 0))
        total += price * item["qty"]
    return total


def low_stock(items, threshold=5):
    """Names of the items whose quantity is strictly below `threshold`.

    The names are sorted alphabetically, ignoring case.
    """
    return [item["name"] for item in items if item["qty"] <= threshold]

### Tool result
@@ lines 1-1 @@
System reminder: File exists but has empty contents

### Tool result
['/workspace/tests/test_report.py']

### Assistant
[{'arguments': '{"file_path":"workspace/tests/test_report.py","offset":0,"limit":300}', 'call_id': 'call_ELXmMjakrytdU7AFC4MVuBrp', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4811b9d1887d0a12f254cf34c9451', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/tests/test_report.py", "offset": 0, "limit": 300}

### Tool result
@@ lines 1-32 of 32 @@
from decimal import Decimal

from inventory.export import to_csv_row
from inventory.pricing import apply_discount
from inventory.report import low_stock, total_value


def test_total_value_plain():
    items = [{"name": "pen", "price": "$2.50", "qty": 4}]
    assert total_value(items) == Decimal("10.00")


def test_total_value_thousands_separator():
    items = [{"name": "laptop", "price": "$1,299.50", "qty": 2}]
    assert total_value(items) == Decimal("2599.00")


def test_discount_rounding_half_up():
    assert apply_discount(Decimal("10.05"), 10) == Decimal("9.05")


def test_total_value_with_discount():
    items = [{"name": "desk", "price": "100.00", "qty": 1, "discount": 15}]
    assert total_value(items) == Decimal("85.00")


def test_low_stock_basic():
    assert low_stock([{"name": "pen", "qty": 2}, {"name": "ink", "qty": 9}]) == ["pen"]


def test_csv_row_plain_name():
    assert to_csv_row({"name": "pen", "price": "2.5", "qty": 4}) == "pen,2.50,4"

### Assistant
[{'id': 'rs_036317a28109edf6016ac48120240c87d08f839287e6494885', 'summary': [], 'type': 'reasoning', 'content': [], 'encrypted_content': 'gAAAAABqxIEhbAO2Gy8b82p7Wrst0BxSBWUGb4geb9on921a5zYRjD9XRfOwzBw3RJYoRhtwnP1OzMlhq8-IRW8Q7Osxd71_ahycKS5Por0vcYXa_dtr5SDf8w5fPPID6xl1qhOVPVb0PRAzMEvG17HyO7xDb2qxW7JYWKZxKui9hiHZYE08ayqTPOut6xjK7DlO2rKQ9Qhgac_xE5LbYV1wlxI1-prKL3qScdYBV9AhM4i15G4_tNqGPSNbAWK_IR3k2JSZA6f02ND2u4BkOpe-JAGBA9-bkqCX95JimVF6pfcHXu5uPYZo23c6qxwaz4I5i__LCNQnbOqCpYJli6dh5-jXJ6c0RPKm8gXOhwNmw9J9M6uTzdm-pzSQ8_gER8kzmnjMuRERVMXmJHM_CoqCJUcDeYQSnRau-4KsB_GxByf0i1EgqkqnOHGHmc2Z_W2YvuunR148ONV9bkOK6kBDp7c4EKoNpOMAr4Hjub-oP2qFW99Sz4kSOxmu0I_r7tWuDAZ7jrjTLeeQvM7EJ41nBhL1Aq4hO4PQ5yPzb5YSGDDOKUn4xF6B8mAm2heM_Cx3oC5o-BtgOQCu36fluEjZaSQitULEukts280jcWE0cFFGJrVtMIaKQmQuI7YNCLSR295RQZAl7hG3jv99axx5sbAggy6WGCuwyCgY2xL1iIgwbkIDN-1wJvV6BunLMVxECH2PZB_b99EbXWODq2i0HqXB4eSB4BkkGutEZcOaeAhbfgVMlptiMDo2ojLOdBPLouGvs3thT5-4uFre5YXlRDqzSsj6D0I3WzrpqY4Y9bTqfKpHPxs3UyfkGNNT58DjQjiUTCryQ-lnNkin3i03jcHnCMLGMEUj0bfdgVsOmN3YOJoRHm0wGcbrG9-bmwZeRD7gmlZJeU5tbaz-dp-YAOOPUWDHiJb1rW_X4pgEL86Xyek2bxUjYhQ1bdjgGVq5CERdsIst6BEUhTEn-f0wOKD4AV8YulIq9GQ3xDIMD9f6KYu4pYXHsPUyJ4C9O3zExjWk9S9tcLRg5hNXwqFWtL7pB-dcLPRHGpXvxGCSEB3cgm1SQpgh-pNZL70Gm_rrEqfcmjy-KjqGz5mZjO-qh0p6AvQdaDvOe-eHTe2G_bSxGzBqW8IF2Uf6x-NchcmQ13PInxXSCVy08naPZOv7nr26Kel2QKUrVriWNqCP9Zbv2Ru3PepyndugPQNvy3OigTgP1GF8RdVuPmMgRZCHDd965D_dkFrzjUOx658IK4ZXneJU4nv8v-MLNCqqU2TX-ruSzWAwDT6eLm-ZbPYuxd8GnyvyUZdAGp0eR_gWLDr6eE_TZnF5P5UKBEbLwr_yoAXL-9AZqTt_F6

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "from decimal import Decimal", "new_string": "from decimal import Decimal, ROUND_HALF_UP", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Assistant
[{'arguments': '{"file_path":"workspace/inventory/pricing.py","old_string":"    cleaned = text.strip().replace(\\"$\\", \\"\\")\\n    return Decimal(cleaned)","new_string":"    cleaned = text.strip()\\n    negative = cleaned.startswith(\\"(\\") and cleaned.endswith(\\")\\")\\n    if negative:\\n        cleaned = cleaned[1:-1].strip()\\n    cleaned = cleaned.replace(\\"$\\", \\"\\").replace(\\",\\", \\"\\").strip()\\n    value = Decimal(cleaned)\\n    return -value if negative else value","replace_all":false}', 'call_id': 'call_iO4aOtVqx7dQFIc49HJMcrMq', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac48126911887d0bdb0dc75f1f461b8', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    cleaned = text.strip().replace(\"$\", \"\")\n    return Decimal(cleaned)", "new_string": "    cleaned = text.strip()\n    negative = cleaned.startswith(\"(\") and cleaned.endswith(\")\")\n    if negative:\n        cleaned = cleaned[1:-1].strip()\n    cleaned = cleaned.replace(\"$\", \"\").replace(\",\", \"\").strip()\n    value = Decimal(cleaned)\n    return -value if negative else value", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Assistant
[{'arguments': '{"file_path":"workspace/inventory/pricing.py","old_string":"    discounted = price * (100 - percent) / 100\\n    return discounted.quantize(Decimal(\\"0.01\\"))","new_string":"    price = Decimal(str(price))\\n    percent = Decimal(str(percent))\\n    discounted = price * (Decimal(\\"100\\") - percent) / Decimal(\\"100\\")\\n    return discounted.quantize(Decimal(\\"0.01\\"), rounding=ROUND_HALF_UP)","replace_all":false}', 'call_id': 'call_fUKwn3Cql7j2YJYUSldGgJ0i', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4812b424087d0ba82c8930fd07564', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/inventory/pricing.py", "old_string": "    discounted = price * (100 - percent) / 100\n    return discounted.quantize(Decimal(\"0.01\"))", "new_string": "    price = Decimal(str(price))\n    percent = Decimal(str(percent))\n    discounted = price * (Decimal(\"100\") - percent) / Decimal(\"100\")\n    return discounted.quantize(Decimal(\"0.01\"), rounding=ROUND_HALF_UP)", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/pricing.py'

### Assistant
[{'arguments': '{"file_path":"workspace/inventory/export.py","old_string":"    price = parse_price(item[\\"price\\"])\\n    return f\'{item[\\"name\\"]},{price:.2f},{item[\\"qty\\"]}\'","new_string":"    price = parse_price(item[\\"price\\"])\\n    name = str(item[\\"name\\"])\\n    if \\",\\" in name or \'\\"\' in name:\\n        name = \'\\"\' + name.replace(\'\\"\', \'\\"\\"\') + \'\\"\'\\n    return f\'{name},{price:.2f},{item[\\"qty\\"]}\'","replace_all":false}', 'call_id': 'call_PUXjh9y7L4WJdXmv1T6zWCTA', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac481308ecc87d0a290f3f177e72e28', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/inventory/export.py", "old_string": "    price = parse_price(item[\"price\"])\n    return f'{item[\"name\"]},{price:.2f},{item[\"qty\"]}'", "new_string": "    price = parse_price(item[\"price\"])\n    name = str(item[\"name\"])\n    if \",\" in name or '\"' in name:\n        name = '\"' + name.replace('\"', '\"\"') + '\"'\n    return f'{name},{price:.2f},{item[\"qty\"]}'", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/export.py'

### Assistant
[{'arguments': '{"file_path":"workspace/inventory/report.py","old_string":"    return [item[\\"name\\"] for item in items if item[\\"qty\\"] <= threshold]","new_string":"    names = [item[\\"name\\"] for item in items if item[\\"qty\\"] < threshold]\\n    return sorted(names, key=str.casefold)","replace_all":false}', 'call_id': 'call_9ykOxN7BGb0zBoldvAmw2DsO', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac481370e6887d0a7bf9c61d791e273', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/inventory/report.py", "old_string": "    return [item[\"name\"] for item in items if item[\"qty\"] <= threshold]", "new_string": "    names = [item[\"name\"] for item in items if item[\"qty\"] < threshold]\n    return sorted(names, key=str.casefold)", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/inventory/report.py'

### Assistant
[{'arguments': '{"command":"python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_WjzTjzItDHXU5KVUbs1ppgoS', 'name': 'execute', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac4813cb55087d0ae18ebc1fbed216e', 'status': 'completed'}]

### Tool call: execute
{"command": "python -m pytest -q workspace/tests", "timeout": 120}

### Tool result

==================================== ERRORS ====================================
_______________ ERROR collecting workspace/tests/test_report.py ________________
ImportError while importing test module '/tmp/day20-lrzkdydg/workspace/tests/test_report.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/local/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/tests/test_report.py:3: in <module>
    from inventory.export import to_csv_row
E   ModuleNotFoundError: No module named 'inventory'
=========================== short test summary info ============================
ERROR workspace/tests/test_report.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.17s

Exit code: 2
[Command failed with exit code 2]

### Assistant
[{'arguments': '{"command":"PYTHONPATH=workspace python -m pytest -q workspace/tests","timeout":120}', 'call_id': 'call_yWDJX5MJhdLyFIS7CjWzzof5', 'name': 'execute', 'type': 'function_call', 'id': 'fc_036317a28109edf6016ac48142877487d0888de5a5a5ccd64b', 'status': 'completed'}]

### Tool call: execute
{"command": "PYTHONPATH=workspace python -m pytest -q workspace/tests", "timeout": 120}

### Tool result
......                                                                   [100%]
6 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'Updated `pricing.py` to parse comma-separated and accounting-style prices and round discounts half up. Updated `export.py` to escape CSV names, and `report.py` to use a strict low-stock threshold and sort names case-insensitively. All 6 tests pass.', 'annotations': [], 'id': 'msg_036317a28109edf6016ac48147bbc087d0b08ec47ddedbd743', 'phase': 'final_answer'}]