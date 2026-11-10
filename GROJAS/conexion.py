"""Conexión centralizada a la base SQLite del proyecto."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ecotech.db"


def conectar():
    """Abre una conexión con claves foráneas y timeout habilitados."""
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db
