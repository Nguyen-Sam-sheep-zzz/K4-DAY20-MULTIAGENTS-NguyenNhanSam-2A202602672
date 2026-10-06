### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Assistant
[{'arguments': '{"path":"workspace"}', 'call_id': 'call_48EaYpSmzR8xw50LbhpMdPAc', 'name': 'ls', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4bfcf68d887d094f32c8e555f4659', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Assistant
[{'arguments': '{"description":"Inspect workspace/bookings and tests, identify defects vs docstrings and conventions. Do not edit. Report precise files and test strategy.","subagent_type":"explorer"}', 'call_id': 'call_c39fdDMjiuF510hs271gMR3i', 'name': 'task', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4bfd1c43887d09d48d448694c5072', 'status': 'completed'}]

### Tool call: task
{"description": "Inspect workspace/bookings and tests, identify defects vs docstrings and conventions. Do not edit. Report precise files and test strategy.", "subagent_type": "explorer"}

### Tool result
## Findings

- **`workspace/bookings/timeutil.py` — `parse_duration` is incomplete.** Its docstring promises `1h30m`, `2h`, `45m`, `1:30`, bare minute values, and surrounding-whitespace handling. The implementation accepts only the `HhMm` form, so the documented forms other than `1h30m` fail. This is the root cause of the `total_minutes` test failure for `"2h"`; `workspace/bookings/schedule.py` delegates parsing to this shared function.
- **`workspace/bookings/billing.py` — rounding contradicts its docstring.** The docstring says partial blocks round up, but `round()` uses nearest-even rounding. For example, 20 minutes with 15-minute blocks returns 1 instead of 2, causing the billing test failure. The docstring also requires negative minutes to raise `ValueError`, but the implementation does not enforce that.
- **`workspace/bookings/schedule.py` — `add_slot` shares mutable state across calls.** Its docstring explicitly requires independent results, but the default list is mutated and reused. The existing single-call test does not expose this; test sequential calls and verify both returned lists remain independent.
- **`workspace/bookings/calendar_export.py` — edge behavior is unspecified and untested.** `slot_end` adds duration directly, so results can exceed 1440 minutes. The short docstring does not say whether this should wrap to the next day or be returned as an absolute minute count; clarify the expected convention before treating it as a defect.

## Test strategy / veri

### Assistant
[{'arguments': '{"path":"workspace/bookings"}', 'call_id': 'call_jL4zfJaWrxmPkiQr4nKhRfm5', 'name': 'ls', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c001582c87d08dfcf1eef0feb871', 'status': 'completed'}]

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/timeutil.py","offset":0,"limit":200}', 'call_id': 'call_tC8lfbERdjXh1f92JlfCqZJC', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c006abc887d0b289331aeb05daa3', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/billing.py","offset":0,"limit":200}', 'call_id': 'call_yrQLD0RtcZon2UOGpDMxH40J', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c006abec87d0a13f54387a1d240d', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/schedule.py","offset":0,"limit":200}', 'call_id': 'call_3Q2hNnBNjPEBMpogyEHjO84P', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c006abfc87d0af1c815d8583fffa', 'status': 'completed'}, {'arguments': '{"file_path":"workspace/bookings/calendar_export.py","offset":0,"limit":200}', 'call_id': 'call_bmmg0ZXMuSEi3KAlN9FR6gI0', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c006ac0c87d0b85e758e0f0aec89', 'status': 'completed'}, {'arguments': '{"pattern":"*.py","path":"workspace/tests"}', 'call_id': 'call_sYLqwmiyZi2mEwHhYVuE9gG7', 'name': 'glob', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c006ac1887d0b3984216bbd340f2', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py", "offset": 0, "limit": 200}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py", "offset": 0, "limit": 200}

### Tool call: glob
{"pattern": "*.py", "path": "workspace/tests"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
['/workspace/tests/test_bookings.py']

### Assistant
[{'arguments': '{"file_path":"workspace/tests/test_bookings.py","offset":0,"limit":200}', 'call_id': 'call_8MKpVhw2VY511XP84NqfnVAy', 'name': 'read_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c0094d2887d0a66c1d85c1228821', 'status': 'completed'}]

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py", "offset": 0, "limit": 200}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/timeutil.py","content":"\\"\\"\\"Time helpers for the bookings package.\\"\\"\\"\\nimport re\\n\\n\\n_DURATION_RE = re.compile(r\\"(?:(\\\\d+)h)?(?:(\\\\d+)m)?\\")\\n\\n\\ndef parse_duration(text):\\n    \\"\\"\\"Convert a duration string to whole minutes (int).\\n\\n    Supported formats:\\n      \\"1h30m\\" -> 90\\n      \\"2h\\"    -> 120\\n      \\"45m\\"   -> 45\\n      \\"1:30\\"  -> 90\\n      \\"45\\"    -> 45    # a bare number means minutes\\n    Surrounding whitespace is ignored.\\n    \\"\\"\\"\\n    if not isinstance(text, str):\\n        raise ValueError(f\\"bad duration: {text!r}\\")\\n\\n    value = text.strip()\\n    if not value:\\n        raise ValueError(f\\"bad duration: {text!r}\\")\\n\\n    clock_match = re.fullmatch(r\\"(\\\\d+):(\\\\d{1,2})\\", value)\\n    if clock_match:\\n        hours, minutes = map(int, clock_match.groups())\\n        if minutes >= 60:\\n            raise ValueError(f\\"bad duration: {text!r}\\")\\n        return hours * 60 + minutes\\n\\n    hour_minute_match = re.fullmatch(r\\"(\\\\d+)h(\\\\d+)m\\", value)\\n    if hour_minute_match:\\n        hours, minutes = map(int, hour_minute_match.groups())\\n        return hours * 60 + minutes\\n\\n    hour_match = re.fullmatch(r\\"(\\\\d+)h\\", value)\\n    if hour_match:\\n        return int(hour_match.group(1)) * 60\\n\\n    minute_match = re.fullmatch(r\\"(\\\\d+)m\\", value)\\n    if minute_match:\\n        return int(minute_match.gro

### Tool call: write_file
{"file_path": "workspace/bookings/timeutil.py", "content": "\"\"\"Time helpers for the bookings package.\"\"\"\nimport re\n\n\n_DURATION_RE = re.compile(r\"(?:(\\d+)h)?(?:(\\d+)m)?\")\n\n\ndef parse_duration(text):\n    \"\"\"Convert a duration string to whole minutes (int).\n\n    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    if not isinstance(text, str):\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    value = text.strip()\n    if not value:\n        raise ValueError(f\"bad duration: {text!r}\")\n\n    clock_match = re.fullmatch(r\"(\\d+):(\\d{1,2})\", value)\n    if clock_match:\n        hours, minutes = map(int, clock_match.groups())\n        if minutes >= 60:\n            raise ValueError(f\"bad duration: {text!r}\")\n        return hours * 60 + minutes\n\n    hour_minute_match = re.fullmatch(r\"(\\d+)h(\\d+)m\", value)\n    if hour_minute_match:\n        hours, minutes = map(int, hour_minute_match.groups())\n        return hours * 60 + minutes\n\n    hour_match = re.fullmatch(r\"(\\d+)h\", value)\n    if hour_match:\n        return int(hour_match.group(1)) * 60\n\n    minute_match = re.fullmatch(r\"(\\d+)m\", value)\n    if minute_match:\n        return int(minute_match.group(1))\n\n    if re.fullmatch(r\"\\d+\", value):\n        return int(value)\n\n    raise ValueError(f\"bad dur

### Tool result
Updated file /workspace/bookings/timeutil.py

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/billing.py","old_string":"    return round(minutes / block)\\n","new_string":"    if minutes < 0:\\n        raise ValueError(\\"minutes must be >= 0\\")\\n    if block <= 0:\\n        raise ValueError(\\"block must be > 0\\")\\n    return (minutes + block - 1) // block\\n","replace_all":false}', 'call_id': 'call_fI2zfd07BrINNi8DqKpMZ0wi', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c0177a5887d09855686b03c4bf8b', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    return round(minutes / block)\n", "new_string": "    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    if block <= 0:\n        raise ValueError(\"block must be > 0\")\n    return (minutes + block - 1) // block\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/schedule.py","old_string":"def add_slot(slot, slots=[]):\\n","new_string":"def add_slot(slot, slots=None):\\n","replace_all":false}', 'call_id': 'call_phHRbZtqi1Nogag4AGUxECIk', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c01cb48487d09200e39c6ae6c19e', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "def add_slot(slot, slots=[]):\n", "new_string": "def add_slot(slot, slots=None):\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Assistant
[{'arguments': '{"file_path":"workspace/bookings/schedule.py","old_string":"    slots.append(slot)\\n    return slots\\n","new_string":"    result = [] if slots is None else list(slots)\\n    result.append(slot)\\n    return result\\n","replace_all":false}', 'call_id': 'call_uNI0V7KT1yy9DHSW4GFVUlFk', 'name': 'edit_file', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c02015c087d085240aeec9510c20', 'status': 'completed'}]

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "old_string": "    slots.append(slot)\n    return slots\n", "new_string": "    result = [] if slots is None else list(slots)\n    result.append(slot)\n    return result\n", "replace_all": false}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Assistant
[{'arguments': '{"command":"python -m pytest workspace/tests -q","timeout":120}', 'call_id': 'call_5Y46Xu4KrwHqyBhv23M4Bht0', 'name': 'execute', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c023cf8087d0947bc1f0620d6ea6', 'status': 'completed'}]

### Tool call: execute
{"command": "python -m pytest workspace/tests -q", "timeout": 120}

### Tool result

==================================== ERRORS ====================================
______________ ERROR collecting workspace/tests/test_bookings.py _______________
ImportError while importing test module '/tmp/day20-d1kbjfah/workspace/tests/test_bookings.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/local/lib/python3.12/importlib/__init__.py:90: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/tests/test_bookings.py:1: in <module>
    from bookings.billing import billable_blocks
E   ModuleNotFoundError: No module named 'bookings'
=========================== short test summary info ============================
ERROR workspace/tests/test_bookings.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.10s

Exit code: 2
[Command failed with exit code 2]

### Assistant
[{'arguments': '{"command":"cd workspace && python -m pytest tests -q","timeout":120}', 'call_id': 'call_rGMM9aFhDXtt5IF0zlIfCkA5', 'name': 'execute', 'type': 'function_call', 'id': 'fc_0af2222ad5d067cd016ac4c027736887d085c8d0281b6188f8', 'status': 'completed'}]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q", "timeout": 120}

### Tool result
...                                                                      [100%]
3 passed in 0.01s

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'Fixed duration parsing to support every documented format, changed billing to round partial blocks up and reject negative minutes, and made `add_slot` return an independent list on each call. The test suite passes.', 'annotations': [], 'id': 'msg_0af2222ad5d067cd016ac4c02ac6e887d0830ac8eddbde129e', 'phase': 'final_answer'}]