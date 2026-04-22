"""Couche de persistance JSON pour documents, logs et métadonnées."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class JSONStore:
    """Stockage JSON minimal avec verrou fichier."""

    def __init__(self, name: str):
        self.path = DATA_DIR / f"{name}.json"
        self._cache: list[dict] = []
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as fh:
                    self._cache = json.load(fh)
            except (json.JSONDecodeError, OSError):
                self._cache = []
        else:
            self._cache = []

    def _save(self) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(self._cache, fh, ensure_ascii=False, indent=2)

    def append(self, record: dict) -> None:
        self._cache.append(record)
        self._save()

    def replace_all(self, records: List[dict]) -> None:
        self._cache = list(records)
        self._save()

    def read_all(self) -> List[dict]:
        return list(self._cache)

    def clear(self) -> None:
        self._cache = []
        self._save()


class AuditLogger:
    """Journal d'audit des événements de sécurité."""

    def __init__(self):
        self.store = JSONStore("audit_log")

    def log(self, event: str, details: Dict[str, Any]) -> None:
        import datetime
        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event": event,
            "details": details,
        }
        self.store.append(record)

    def read(self) -> List[dict]:
        return self.store.read_all()


class DocumentStore:
    """Stockage persistant des documents RAG."""

    def __init__(self, user_id: str = "global"):
        self.user_id = user_id
        self.store = JSONStore(f"documents_{user_id}")

    def add(self, doc_id: str, content: str, metadata: dict | None = None) -> None:
        records = self.store.read_all()
        records = [r for r in records if r["id"] != doc_id]
        records.append({"id": doc_id, "content": content, "metadata": metadata or {}})
        self.store.replace_all(records)

    def read_all(self) -> List[dict]:
        return self.store.read_all()

    def clear(self) -> None:
        self.store.clear()

    def delete(self, doc_id: str) -> None:
        records = [r for r in self.store.read_all() if r["id"] != doc_id]
        self.store.replace_all(records)


class UserStore:
    """Stockage des utilisateurs autorisés pour les outils sensibles."""

    def __init__(self):
        self.store = JSONStore("authorized_users")

    def add(self, user_id: str) -> None:
        records = self.store.read_all()
        if user_id not in {r["user_id"] for r in records}:
            records.append({"user_id": user_id})
            self.store.replace_all(records)

    def contains(self, user_id: str) -> bool:
        return any(r["user_id"] == user_id for r in self.store.read_all())

    def clear(self) -> None:
        self.store.clear()


def get_audit_logger() -> AuditLogger:
    return AuditLogger()


def get_document_store(user_id: str = "global") -> DocumentStore:
    return DocumentStore(user_id)


def get_user_store() -> UserStore:
    return UserStore()
