"""S1b Chinese display label -> canonical code (deterministic). Single source: s1b_label_map.json (same folder).

normalize(): NFKC, bar variants -> '|', all whitespace removed.  to_code(field, value) returns the canonical code,
or None when the value is not a known label of that field (the caller then treats the raw value as invalid).
"""
from __future__ import annotations

import json
import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(HERE, "s1b_label_map.json")
BARS = "|\uff5c\u2502\u2503\u01c0\uffe8"
FIELDS = ("Q1", "Q2", "Q3", "Q4", "ATTESTATION")

with open(MAP_PATH, encoding="utf-8") as _f:
    _RAW = json.load(_f)


def normalize(s):
    s = unicodedata.normalize("NFKC", "" if s is None else str(s))
    s = "".join("|" if ch in BARS else ch for ch in s)
    return "".join(ch for ch in s if not ch.isspace())


def options(field):
    """Display labels in drop-down order."""
    return [lab for lab, _ in _RAW["fields"][field]]


def codes(field):
    return [code for _, code in _RAW["fields"][field]]


def table(field):
    """normalized label -> code."""
    return {normalize(lab): code for lab, code in _RAW["fields"][field]}


def to_code(field, value):
    if value is None or str(value).strip() == "":
        return ""
    return table(field).get(normalize(value))
