import dbm
import pickle
from typing import Any

db = dbm.open("db", "c")


def db_getter(name: str, fields: list[tuple[str, int, Any]]) -> Any:
    """Generate a __getattr__ for a database value.
    Each field is a field name, a version number, and a default value."""
    for field in fields:
        if field[0] == name:
            res = db.get(f"{field[0]}:{field[1]}")
            if res is None:
                return field[2]
            else:
                return pickle.loads(res)

    raise AttributeError


def db_setter(name: str, value: Any, fields: list[tuple[str, int]]):
    for field in fields:
        if field[0] == name:
            db[f"{field[0]}:{field[1]}"] = pickle.dumps(value)

    raise AttributeError


class DbUser:
    def __init__(self, id: int):
        self.boons: list[str] = []
        self.curses: list[str] = []
        self.discord_id = id

    def __getattr__(self, name):
        return db_getter(name, [("boons", 1, []), ("curses", 1, [])])

    def __setattr__(self, name: str, value: Any):
        db_setter(name, value, [("boons", 1), ("curses", 1)])
