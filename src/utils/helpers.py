from __future__ import annotations

import json
import csv
import uuid
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any, Iterable, Optional, Dict, List


class UtilsError(Exception):
    """Grunnfeil for utils-modulen."""
    
class DataLoadError(UtilsError):
    """Feil ved lasting av data."""
    
class DataSaveError(UtilsError):
    """Feil ved lagring av data."""
    
class ValidationError(UtilsError):
    """Feil ved validering av data."""
    
#Fil- og banehjelp

def ensure_dir(path: str | Path) -> Path:
    """Sikrer at en katalog eksisterer."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def load_json(path: str | Path, default: Any = None) -> Any:
    """
    Leser JSON fra fil. Returnerer `default` hvis filen ikke finnes (ingen feil).
    Kaster DataLoadError ved annen IO/JSON-feil.
    """
    p = Path(path)
    if not p.exists():
        return default
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise DataLoadError(f"Kunne ikke lese JSON fra {p}: {e}") from e
    
def save_json(path: str | Path, data: ANy, pretty: bool = True) -> None:
    """Lagrer data som JSON. Oppretter mapper automatisk.
    Kaster DataSaveError ved IO/JSON-feil.
    """
    p = Path(path)
    ensure_dir(p.parent)
    try:
        with p.open("w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, ensure_ascii=False, indent = 2)
            else:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    except Exception as e:
        raise DataSaveError(f"Kunne ikke lagre JSON til {p}: {e}") from e

def load_csv(path: str | Path) -> List[Dict[str, str]]:
    """
    Leser CSV med header. Returnerer liste av dicts (kolonnenavn -> verdi).
    Kaster DataLoadError ved feil.
    """
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception as e:
        raise DataLoadError(f"Kunne ikke lese CSV fra {p}: {e}") from e
    
def save_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    """
    Lagrer liste av dicts som CSV. Kolonnenavn tas fra første rad.
    Kaster DataSaveError ved feil.
    """
    rows = list(rows)
    if not rows:
        raise DataSaveError("Kan ikke lagre tom CSV (ingen rader).")
    p = Path(path)
    ensure_dir(p.parent)
    fieldnames = list(rows[0].keys())
    try:
        with p.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    except Exception as e:
        raise DataSaveError(f"Kunne ikke lagre CSV til {p}: {e}") from e
    

                