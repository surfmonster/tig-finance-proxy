import hashlib
import json
from typing import Dict, Any

one_day_seconds = 60 * 60 * 24


def dict_hash(d: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}

    hstr = ''
    itms = sorted(d.items())
    for k, v in itms:
        hstr += f'{k}:{v}>'
    dhash.update(hstr.encode("utf-8"))
    return dhash.hexdigest()


def to_float(i):
    ans = float(i)
    return ans
