import json
import random
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

MANAGER_FILE = Path(__file__).resolve().parent / "managers.json"
LEGACY_MANAGER_FILE = Path("managers.json")


def _safe_load_json(path: Path):
    try:
        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return {}
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return {}


def _ensure_manager_store():
    if not MANAGER_FILE.exists():
        MANAGER_FILE.write_text("{}", encoding="utf-8")


def load_managers():
    _ensure_manager_store()

    primary = _safe_load_json(MANAGER_FILE)
    if primary:
        return primary

    if LEGACY_MANAGER_FILE.exists() and LEGACY_MANAGER_FILE.resolve() != MANAGER_FILE.resolve():
        legacy = _safe_load_json(LEGACY_MANAGER_FILE)
        if legacy:
            save_managers(legacy)
            return legacy

    MANAGER_FILE.write_text("{}", encoding="utf-8")
    return {}


def save_managers(data):
    _ensure_manager_store()
    MANAGER_FILE.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
