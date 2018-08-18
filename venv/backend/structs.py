from typing import Dict

class AlgorithmError(Exception):
    pass


class Person:
    def __init__(self, name: str):
        self._name = name
        self._prefs = {}

    def get_name(self) -> str:
        return self._name

    def set_prefs(self, prefs: Dict[Session, int]):
        self._prefs = prefs

    def get_pref(self, session):
        return self._prefs[session]


class Session:
    def __init__(self, id_: str):
        self._id = id_

    def get_id(self):
        return self._id